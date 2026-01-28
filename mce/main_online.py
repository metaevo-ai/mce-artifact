"""
MCE Online Mode: Direct learning from test data without meta-agent.
"""

import os
import json
import asyncio
import argparse
import logging
import shutil
from pathlib import Path

from mce.utils import ignore_pycache, compute_avg_metrics
from mce.eval import batch_solve, load_retrieval_function
from mce.logging_utils import setup_logger, setup_run_logger
from mce.base_agent import run_base_agent
from mce.llm_client import LLMClient
from env import get_environment, get_task_instruction
from dotenv import load_dotenv

load_dotenv(override=True)


RETRIEVAL_FUNCTION_BASELINE = '''def retrieval_function(question: str) -> str:
    """Simple retrieval - returns all context concatenated."""
    from pathlib import Path
    context_dir = Path(__file__).parent / "context"
    all_context = []
    for file in sorted(context_dir.rglob("*.md")):
        all_context.append(file.read_text())
    return "\\n\\n".join(all_context) if all_context else ""
'''


def setup_sub_iteration_workspace(
    workspace_base: Path,
    sub_iter: int,
    skill_path: str = None,
    prev_sub_folder: Path = None,
    logger: logging.Logger = None,
) -> Path:
    """
    Setup workspace for a sub-iteration (batch).
    
    Args:
        workspace_base: Base workspace directory (e.g., workspace/finer_online)
        sub_iter: Sub-iteration number (batch index)
        skill_path: Optional path to skill directory to copy (for first sub-iter only)
        prev_sub_folder: Previous sub-iteration folder to copy from
        logger: Logger instance
    
    Returns:
        Path to created sub-iteration directory
    """
    if logger is None:
        logger = logging.getLogger(__name__)
    
    workspace_base = Path(workspace_base)
    sub_iter_folder = workspace_base / f"iter1_sub{sub_iter}"
    
    # Create sub-iteration folder structure
    sub_iter_folder.mkdir(parents=True, exist_ok=True)
    logger.info(f"✅ Created sub-iteration folder: {sub_iter_folder}")
    
    # First sub-iteration: copy skills if provided
    if sub_iter == 0 and skill_path:
        skill_path = Path(skill_path)
        if not skill_path.exists():
            logger.warning(f"⚠️  Skill path not found: {skill_path}")
        else:
            target_skills = sub_iter_folder / ".claude" / "skills"
            target_skills.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(skill_path, target_skills, ignore=ignore_pycache, dirs_exist_ok=True)
            logger.info(f"✅ Copied skills from {skill_path}")
    
    # Subsequent sub-iterations: copy from previous sub-iteration
    if prev_sub_folder:
        # Copy skills
        prev_skills = prev_sub_folder / ".claude" / "skills"
        if prev_skills.exists():
            target_skills = sub_iter_folder / ".claude" / "skills"
            target_skills.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(prev_skills, target_skills, ignore=ignore_pycache, dirs_exist_ok=True)
            logger.info(f"✅ Copied skills from {prev_sub_folder.name}")
        
        # Copy context
        prev_context = prev_sub_folder / "context"
        if prev_context.exists():
            target_context = sub_iter_folder / "context"
            shutil.copytree(prev_context, target_context, ignore=ignore_pycache, dirs_exist_ok=True)
            logger.info(f"✅ Copied context from {prev_sub_folder.name}")
        
        # Copy retrieval function
        prev_retrieve = prev_sub_folder / "retrieve_context.py"
        if prev_retrieve.exists():
            target_retrieve = sub_iter_folder / "retrieve_context.py"
            shutil.copy2(prev_retrieve, target_retrieve)
            logger.info(f"✅ Copied retrieve_context.py from {prev_sub_folder.name}")
    else:
        # First sub-iteration: create empty context and baseline retrieval
        context_dir = sub_iter_folder / "context"
        context_dir.mkdir(exist_ok=True)
        logger.info(f"✅ Created context/ folder")
        
        retrieve_file = sub_iter_folder / "retrieve_context.py"
        retrieve_file.write_text(RETRIEVAL_FUNCTION_BASELINE)
        logger.info(f"✅ Initialized baseline retrieval function")
    
    # Copy workspace_utils to utils/
    project_root = workspace_base.parent.parent
    source_utils = project_root / "mce" / "workspace_utils"
    target_utils = sub_iter_folder / "utils"
    
    if source_utils.exists() and not target_utils.exists():
        def ignore_utils(directory, files):
            ignored = ignore_pycache(directory, files)
            # Always skip validate_base.py since we don't evolve retrieval
            if 'validate_base.py' in files:
                ignored.append('validate_base.py')
            return ignored
        
        shutil.copytree(source_utils, target_utils, ignore=ignore_utils)
        logger.info(f"✅ Copied workspace_utils/ to utils/")
    
    # Create data directory
    data_dir = sub_iter_folder / "data"
    data_dir.mkdir(exist_ok=True)
    
    return sub_iter_folder


def find_last_completed_sub_iteration(workspace_base: Path, logger: logging.Logger = None) -> tuple[int, Path]:
    """
    Find the last completed sub-iteration in the workspace.
    
    Returns:
        Tuple of (last_sub_idx, last_sub_folder_path)
        Returns (-1, None) if no sub-iterations found
    """
    if logger is None:
        logger = logging.getLogger(__name__)
    
    workspace_base = Path(workspace_base)
    sub_iter_folders = list(workspace_base.glob("iter1_sub*"))
    
    if not sub_iter_folders:
        return -1, None
    
    # Sort numerically by extracting sub-iteration number (not lexicographically)
    sub_iter_folders.sort(key=lambda p: int(p.name.split("_sub")[1]))
    
    # Check each folder in reverse order to find the last one with training data
    for sub_folder in reversed(sub_iter_folders):
        # Extract sub-iteration number
        sub_idx = int(sub_folder.name.split("_sub")[1])
        
        # Check if this folder has training data (indicates completion)
        train_file = sub_folder / "data" / "train.json"
        if train_file.exists():
            logger.info(f"Found last completed sub-iteration: {sub_folder.name} (sub_idx={sub_idx})")
            return sub_idx, sub_folder
    
    return -1, None


async def run_online_iteration(
    workspace_base: Path,
    iteration: int,
    env_name: str,
    test_data_path: str,
    test_limit: int,
    train_batch_size: int,
    data_accumulation_limit: int,
    model: str,
    logger: logging.Logger,
    run_dir: Path,
    skill_path: str = None,
    e2b_sandbox_manager = None,
    continue_from_last: bool = False,
) -> dict:
    """
    Run a single online learning iteration with sub-iterations for each batch.
    
    Process test data in batches, with optional data accumulation.
    Each batch creates a sub-iteration directory.
    
    Args:
        workspace_base: Base workspace directory
        iteration: Iteration number
        env_name: Environment name
        test_data_path: Path to test data file
        test_limit: Total test samples to process
        train_batch_size: Samples per batch
        data_accumulation_limit: Max accumulated samples (0 = no limit, accumulate all)
        model: LLM model
        logger: Logger instance
        run_dir: Run directory for logging
        skill_path: Optional path to skill directory to copy
        e2b_sandbox_manager: E2B sandbox manager (None = run locally)
        continue_from_last: If True, continue from last completed sub-iteration
    
    Returns:
        Dictionary with iteration results
    """
    logger.info(f"\n🔄 ONLINE ITERATION {iteration}")
    task_instruction = get_task_instruction(env_name)
    env = get_environment(env_name)
    llm = LLMClient(model=model)
    
    # Load all test samples upfront
    test_samples = env.load_samples(path=test_data_path, limit=test_limit, random_sample=False)
    logger.info(f"📊 Loaded {len(test_samples)} test samples")
    
    # Calculate number of batches
    num_batches = (len(test_samples) + train_batch_size - 1) // train_batch_size
    
    logger.info(f"📊 Processing {num_batches} batches")
    logger.info(f"📊 Batch size: {train_batch_size}")
    logger.info(f"📊 Data accumulation limit: {data_accumulation_limit if data_accumulation_limit > 0 else 'unlimited'}")
    
    # Track cumulative statistics
    total_processed = 0
    accumulated_samples = []
    prev_sub_folder = None
    start_batch_idx = 0
    cumulative_metrics = {}
    
    # Check if continuing from last sub-iteration
    if continue_from_last:
        last_sub_idx, last_sub_folder = find_last_completed_sub_iteration(workspace_base, logger)
        
        if last_sub_idx >= 0:
            logger.info(f"\n🔄 CONTINUING from last completed sub-iteration: {last_sub_folder.name}")
            
            # Load previous training data to reconstruct accumulated samples and stats
            prev_sub_folder = last_sub_folder
            start_batch_idx = last_sub_idx + 1
            
            # Reconstruct accumulated samples from the last sub-iteration
            train_file = last_sub_folder / "data" / "train.json"
            with open(train_file, 'r', encoding='utf-8') as f:
                train_data = json.load(f)
            
            # Get accumulated size from the last sub-iteration
            accumulated_size = train_data.get("summary", {}).get("accumulated_size", 0)
            
            # Reconstruct accumulated samples by loading samples up to the last batch
            # Calculate how many samples were processed up to last_sub_idx
            samples_processed = (last_sub_idx + 1) * train_batch_size
            samples_processed = min(samples_processed, len(test_samples))
            
            # If accumulation limit is set, only keep the most recent samples
            if data_accumulation_limit > 0:
                start_idx = max(0, samples_processed - data_accumulation_limit)
                accumulated_samples = test_samples[start_idx:samples_processed]
            else:
                accumulated_samples = test_samples[:samples_processed]
            
            # Reconstruct batch history by reading all previous sub-iterations
            for prev_idx in range(last_sub_idx + 1):
                prev_folder = workspace_base / f"iter1_sub{prev_idx}"
                prev_train_file = prev_folder / "data" / "train.json"
                
                if prev_train_file.exists():
                    with open(prev_train_file, 'r', encoding='utf-8') as f:
                        prev_train_data = json.load(f)
                    
                    summary = prev_train_data.get("summary", {})
                    # Extract primary metric value using environment's primary metric name
                    primary_metric_name = env.get_primary_metric_name()
                    batch_metrics = summary.get("train_metrics", {})
                    
                    # Calculate batch range
                    batch_start = prev_idx * train_batch_size
                    batch_end = min(batch_start + train_batch_size, len(test_samples))
                    batch_size = batch_end - batch_start
                    
                    # Update cumulative stats
                    total_processed += batch_size
                    
                    # Accumulate metrics (all samples)
                    for metric_name, metric_value in batch_metrics.items():
                        if metric_name not in cumulative_metrics:
                            cumulative_metrics[metric_name] = 0.0
                        cumulative_metrics[metric_name] += metric_value * batch_size

            
            if start_batch_idx >= num_batches:
                logger.info(f"\n✅ All batches already completed! Nothing to continue.")

                return 
        else:
            logger.info(f"\n⚠️  No previous sub-iterations found. Starting from scratch.")
            continue_from_last = False
    
    # Process each batch in its own sub-iteration
    for batch_idx in range(start_batch_idx, num_batches):
        logger.info(f"\n{'='*60}")
        logger.info(f"📦 SUB-ITERATION 1.{batch_idx} (Batch {batch_idx + 1}/{num_batches})")
        logger.info(f"{'='*60}")
        
        # Create sub-iteration workspace
        # Only use skill_path if this is the very first sub-iteration (batch_idx == 0)
        # and we're not continuing (i.e., prev_sub_folder is None at start)
        use_skill_path = (batch_idx == 0 and not continue_from_last)
        
        sub_iter_folder = setup_sub_iteration_workspace(
            workspace_base=workspace_base,
            sub_iter=batch_idx,
            skill_path=skill_path if use_skill_path else None,
            prev_sub_folder=prev_sub_folder,
            logger=logger,
        )
        
        # Get current batch
        start_idx = batch_idx * train_batch_size
        end_idx = min(start_idx + train_batch_size, len(test_samples))
        current_batch = test_samples[start_idx:end_idx]
        
        # Accumulate data
        accumulated_samples.extend(current_batch)
        
        # Trim to accumulation limit (keep most recent)
        if data_accumulation_limit > 0 and len(accumulated_samples) > data_accumulation_limit:
            accumulated_samples = accumulated_samples[-data_accumulation_limit:]
        
        accumulated_size = len(accumulated_samples)
        logger.info(f"  📊 Current batch: [{start_idx}:{end_idx}] ({len(current_batch)} samples)")
        logger.info(f"  📊 Accumulated samples: {accumulated_size}")
        
        # Evaluate accumulated samples
        logger.info(f"\n📊 Evaluating accumulated samples...")
        
        # Write full retrieval
        retrieve_file = sub_iter_folder / "retrieve_context.py"
        retrieve_file.write_text(RETRIEVAL_FUNCTION_BASELINE)

        retrieval_fn = load_retrieval_function(sub_iter_folder)
        eval_data = await batch_solve(
            retrieval_function=retrieval_fn,
            samples=accumulated_samples,
            env=env_name,
            llm=llm,
        )
        eval_summary = eval_data["summary"]
        primary_metric_name = eval_summary["primary_metric"]
        primary_metric_value = eval_summary["primary_metric_value"]
        
        
        logger.info(f"  ✅ Batch {primary_metric_name} (all): {primary_metric_value:.2%}")
        
        # Track cumulative stats
        total_processed += len(current_batch)

        # Prepare training data for base-agent
        # Use environment's format_result_for_training to decide what fields to include
        batch_results = [
            env.format_result_for_training(item)
            for item in eval_data.get("results", [])
        ]
        
        train_data = {
            "summary": {
                "batch_idx": batch_idx,
                f"train_{primary_metric_name}": primary_metric_value,
                "train_metrics": eval_summary["metrics"],
            },
            "detailed_results": batch_results,
        }
        
        # Save training data for base-agent
        train_file = sub_iter_folder / "data" / "train.json"
        with open(train_file, 'w', encoding='utf-8') as f:
            json.dump(train_data, f, indent=2, ensure_ascii=False)
            
        
        # If it's the last sub-iteration, continue without running base-agent
        if batch_idx == num_batches - 1:
            continue
        
        # Run base-agent to learn from accumulated results
        logger.info(f"\n🤖 BASE-AGENT: Learning from batch {batch_idx}...")
        base_result = await run_base_agent(
            iter_dir=sub_iter_folder,
            task_instruction=task_instruction,
            workspace_base=workspace_base,
            run_dir=run_dir,
            iteration=iteration,
            e2b_sandbox_manager=e2b_sandbox_manager,
            evolve_retrieval=False,  # Never evolve retrieval in online mode
        )
        
        if not base_result['success']:
            raise Exception(f"Base-agent failed at batch {batch_idx}: {base_result['error']}")

        logger.info(f"✅ Base-agent completed for batch {batch_idx}")
        
        # Update prev_sub_folder for next iteration
        prev_sub_folder = sub_iter_folder

    return


async def main():
    """Main entry point for online learning mode."""
    parser = argparse.ArgumentParser(
        description="Run MCE in online learning mode: learn directly from test data"
    )
    
    parser.add_argument(
        "--workspace",
        type=str,
        required=True,
        help="Path to workspace base directory (e.g., workspace/finer_online)"
    )
    parser.add_argument(
        "--env",
        type=str,
        required=True,
        help="Environment type"
    )
    parser.add_argument(
        "--test-data",
        type=str,
        required=True,
        help="Path to test data file"
    )
    parser.add_argument(
        "--test-limit",
        type=int,
        default=100,
        help="Total test samples to process (default: 100)"
    )
    parser.add_argument(
        "--train-batch-size",
        type=int,
        default=20,
        help="Samples per batch (default: 20)"
    )
    parser.add_argument(
        "--data-accumulation-limit",
        type=int,
        default=0,
        help="Max accumulated samples to keep (0 = unlimited, default: 0)"
    )
    parser.add_argument(
        "--skill-path",
        type=str,
        default=None,
        help="Optional path to skill directory to copy (e.g., path/to/.claude/skills)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="deepseek/deepseek-chat-v3.1",
        help="LLM model used in context eval (default: deepseek/deepseek-chat-v3.1)"
    )
    parser.add_argument(
        "--log-dir",
        type=str,
        default="logs",
        help="Directory for log files (default: logs)"
    )
    parser.add_argument(
        "--use-e2b",
        action="store_true",
        help="Run agents in E2B sandbox for isolation (requires E2B_API_KEY env var)"
    )
    parser.add_argument(
        "--continue-training",
        action="store_true",
        help="Continue training from the last completed sub-iteration in the workspace"
    )
    
    args = parser.parse_args()
    
    # Setup run directory for organized logging
    run_dir = setup_run_logger(log_base_dir=args.log_dir)
    
    # Setup main logger
    logger = setup_logger(
        name="mce_online",
        run_dir=run_dir,
        agent_type="run_summary",
        console_colors=True,
        minimal_console=False
    )
    
    # Print run start message
    timestamp = run_dir.name.replace("run_", "")
    print(f"[RUN {timestamp}] Starting MCE Online Mode")
    
    # Resolve workspace path
    workspace_base = Path(args.workspace).resolve()
    workspace_base.mkdir(parents=True, exist_ok=True)
    
    logger.info("\n🚀 MCE ONLINE LEARNING MODE")
    logger.info(f"  Workspace: {workspace_base}")
    logger.info(f"  Environment: {args.env}")
    logger.info(f"  Test data: {args.test_data}")
    logger.info(f"  Test samples: {args.test_limit}")
    logger.info(f"  Batch size: {args.train_batch_size}")
    logger.info(f"  Data accumulation limit: {args.data_accumulation_limit if args.data_accumulation_limit > 0 else 'unlimited'}")
    logger.info(f"  Skill path: {args.skill_path if args.skill_path else 'None (no initial skills)'}")
    logger.info(f"  Model: {args.model}")
    logger.info(f"  Use E2B sandbox: {args.use_e2b}")
    logger.info(f"  Continue training: {args.continue_training}")
    
    # Check E2B API key if using E2B
    if args.use_e2b:
        if not os.getenv("E2B_API_KEY"):
            logger.error("E2B_API_KEY environment variable is not set. Get your API key from https://e2b.dev")
            return
    
    # Initialize E2B sandbox manager (if using E2B)
    e2b_sandbox_manager = None
    if args.use_e2b:
        from mce.e2b_sandbox import E2BSandboxManager
        logger.info("🔒 Initializing E2B sandbox...")
        e2b_sandbox_manager = E2BSandboxManager(workspace_base, timeout=3600)  # 1 hour
        e2b_sandbox_manager.initialize()
    
    # Run online iteration (creates sub-iterations internally)
    try:
        await run_online_iteration(
            workspace_base=workspace_base,
            iteration=1,
            env_name=args.env,
            test_data_path=args.test_data,
            test_limit=args.test_limit,
            train_batch_size=args.train_batch_size,
            data_accumulation_limit=args.data_accumulation_limit,
            model=args.model,
            logger=logger,
            run_dir=run_dir,
            skill_path=args.skill_path,
            e2b_sandbox_manager=e2b_sandbox_manager,
            continue_from_last=args.continue_training,
        )
    finally:
        # Cleanup E2B sandbox
        if e2b_sandbox_manager:
            logger.info("🔒 Cleaning up E2B sandbox...")
            e2b_sandbox_manager.cleanup()

if __name__ == "__main__":
    asyncio.run(main())

