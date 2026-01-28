"""
Base-agent implementation using Claude Agent SDK.

The base-agent learns task-specific context from training data using skills
provided by the meta-agent.
"""

import os
import asyncio
import subprocess
import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from functools import partial
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions
)

from mce.logging_utils import setup_logger, log_message
from mce.prompts.base_agent import build_base_agent_prompt
from mce.utils import cleanup_irrelevant_files

from dotenv import load_dotenv
load_dotenv(override=True)


def _verify_base_agent_outputs(
    iter_dir: Path,
    logger: logging.Logger,
    message_count: int = 0,
    evolve_retrieval: bool = False,
) -> Dict[str, Any]:
    """
    Verify that base-agent generated required files.
    
    Args:
        iter_dir: Iteration directory
        logger: Logger instance
        message_count: Number of messages processed (0 for E2B)
        evolve_retrieval: Whether retrieval evolution is enabled
        
    Returns:
        Dictionary with success status and file paths
    """
    retrieve_context_file = iter_dir / "retrieve_context.py"
    context_dir = iter_dir / "context"
    
    # Only check retrieve_context.py if evolve_retrieval is enabled
    if evolve_retrieval:
        if not retrieve_context_file.exists():
            logger.error(f"Base-agent did not generate retrieve_context.py at {retrieve_context_file}")
            return {
                'success': False,
                'error': f"Base-agent did not generate retrieve_context.py at {retrieve_context_file}",
                'message_count': message_count
            }
        logger.info(f"✓ Generated retrieve_context.py")
    else:
        logger.info(f"✓ Retrieval function will be auto-generated (evolve_retrieval=False)")
    
    if not context_dir.exists() or not any(context_dir.iterdir()):
        logger.warning(f"⚠️⚠️⚠️Context directory is empty or missing at {context_dir}")
    
    logger.info(f"✓ Generated context files in {context_dir}")
    
    return {
        'success': True,
        'error': None,
        'message_count': message_count,
        'retrieve_context_path': str(retrieve_context_file) if evolve_retrieval else None,
        'context_dir': str(context_dir)
    }

async def base_agent_permission_handler(
    tool_name: str,
    input_data: dict,
    context: dict,
    iter_dir: Path,
):
    """
    Permission handler for base-agent to restrict operations.
    
    Ensures the agent:
    1. Only uses allowed tools
    2. Can only read/write files within its iteration directory (no access to other iterations)
    """

    # Define allowed tools
    allowed_tools = ["Skill", "Read", "Write", "Edit", "Bash", "Glob", "Grep", "Task", "TaskOutput", "ExitPlanMode", "TodoWrite", "KillShell", "EnterPlanMode"]
    
    # Check if tool is in allowed list
    if tool_name not in allowed_tools:
        return {
            "behavior": "deny",
            "message": f"Tool '{tool_name}' is not allowed. Allowed tools: {', '.join(allowed_tools)}",
            "interrupt": False
        }
    
    iter_dir = iter_dir.resolve()
    
    # Tools that involve file paths
    file_tools = ["Read", "Write", "Edit", "Glob", "Grep"]

    if tool_name in file_tools:
        file_path = input_data.get("file_path") or input_data.get("path")
        if file_path:
            # Resolve the absolute path (relative to iter_dir since that's the cwd)
            if not Path(file_path).is_absolute():
                resolved_path = (iter_dir / file_path).resolve()
            else:
                resolved_path = Path(file_path).resolve()
            
            # All file operations restricted to iter_dir only
            try:
                resolved_path.relative_to(iter_dir)
            except ValueError:
                return {
                    "behavior": "deny",
                    "message": f"Access denied: All file operations restricted to current iteration directory ({iter_dir})",
                    "interrupt": True
                }
            
            # Prevent writing/editing files in utils/ directory
            if tool_name in ["Write", "Edit"]:
                try:
                    utils_dir = (iter_dir / "utils").resolve()
                    resolved_path.relative_to(utils_dir)
                    return {
                        "behavior": "deny",
                        "message": f"Access denied: Cannot write or edit utility functions in utils/ directory",
                        "interrupt": True
                    }
                except ValueError:
                    # File is not in utils/, allow the operation
                    pass
            
            return {"behavior": "allow", "updatedInput": input_data}
    
    # Allow the operation
    return {
        "behavior": "allow",
        "updatedInput": input_data
    }


async def run_base_agent(
    iter_dir: Path,
    task_instruction: str,
    workspace_base: Path = None,
    log_dir: str = "logs",
    run_dir: Path = None,
    iteration: int = None,
    e2b_sandbox_manager = None,
    initial_prompt: str = None,
    evolve_retrieval: bool = False,
) -> Dict[str, Any]:
    """
    Run base-agent to learn context.
    
    Args:
        iter_dir: Iteration directory
        task_instruction: Task-instruction from env
        workspace_base: Base workspace directory (optional, derived from iter_dir if not provided)
        log_dir: Directory for log files (default: "logs")
        run_dir: Run directory for organized logging
        iteration: Iteration number
        e2b_sandbox_manager: E2B sandbox manager (None = run locally)
        initial_prompt: Optional initial prompt (only for iter1 without seed context)
        evolve_retrieval: Whether to evolve retrieval function

    """
    # Extract sub_iteration from iter_dir path if present (e.g., iter1_sub0 -> sub_iter=0)
    sub_iteration = None
    iter_dir_name = Path(iter_dir).name
    if "_sub" in iter_dir_name:
        sub_iteration = int(iter_dir_name.split("_sub")[1])
    # Set up iteration-specific logger
    if run_dir and iteration is not None:
        logger = setup_logger(
            name=f"base_iter{iteration}_sub{sub_iteration}" if sub_iteration is not None else f"base_iter{iteration}",
            run_dir=run_dir,
            agent_type="base",
            iteration=iteration,
            sub_iteration=sub_iteration,
            minimal_console=True
        )
    else:
        logger = setup_logger(name="base_agent", log_dir=log_dir, console_colors=True)
    
    logger.info(f"\n🤖 BASE-AGENT: Learning context")
    logger.info(f"  Iteration directory: {iter_dir}")
    
    # Derive workspace_base if not provided
    if workspace_base is None:
        workspace_base = iter_dir.parent
    
    workspace_base = Path(workspace_base)  # Ensure it's a Path object
    
    # Configure options for base-agent with skills
    # Note: We explicitly restrict tools to prevent unwanted operations like WebSearch
    allowed_tools = ["Skill", "Read", "Write", "Edit", "Bash", "Glob", "Grep", "Task", "TaskOutput", "ExitPlanMode", "TodoWrite", "KillShell", "EnterPlanMode"]
    
    # Build prompt based on execution environment
    if e2b_sandbox_manager:
        # Build prompt with E2B paths
        full_prompt = build_base_agent_prompt(
            task_instruction=task_instruction,
            iter_dir=f"/workspace/{iter_dir.name}",
            workspace_base="/workspace",
            initial_prompt=initial_prompt,
            evolve_retrieval=evolve_retrieval,
        )
    else:
        # Build prompt with local paths
        full_prompt = build_base_agent_prompt(
            task_instruction=task_instruction,
            iter_dir=str(iter_dir),
            workspace_base=str(workspace_base),
            initial_prompt=initial_prompt,
            evolve_retrieval=evolve_retrieval,
        )
    
    # Log the prompt
    logger.info("\n" + "="*80)
    logger.info("📝 BASE-AGENT PROMPT")
    logger.info("="*80)
    logger.info(f"\n{full_prompt}\n")
    logger.info("="*80 + "\n")
    
    # Run agent in E2B sandbox if manager is provided
    if e2b_sandbox_manager:
        logger.info("🔒 Running agent in E2B sandbox")
        try:
            result = await e2b_sandbox_manager.run_agent(
                iter_dir=iter_dir,
                prompt=full_prompt,
                allowed_tools=allowed_tools,
                timeout=1800,  # 30 minutes
                logger=logger,
            )
            
            if not result["success"]:
                logger.error(f"E2B sandbox execution failed: {result.get('stderr', 'Unknown error')}")
                return {
                    'success': False,
                    'error': f"E2B sandbox execution failed: {result.get('stderr', 'Unknown error')}",
                    'message_count': 0
                }
            
            logger.info("✓ E2B sandbox execution completed")
            logger.info(f"  stdout: {result['stdout'][:500]}...")  # Log first 500 chars
            
            # Clean up irrelevant files
            cleanup_irrelevant_files(iter_dir, agent_type="base", logger=logger)
            
            # Verify that required files were created (they should be synced back)
            return _verify_base_agent_outputs(iter_dir, logger, message_count=0, evolve_retrieval=evolve_retrieval)

        except Exception as e:
            logger.error(f"E2B sandbox execution failed: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'message_count': 0
            }
    
    # Original local execution path
    options = ClaudeAgentOptions(
        cwd=str(iter_dir),  # Work at iter_dir level (data/ and utils/ are copied here)
        setting_sources=["project"],  # Load skills from .claude/skills/ only
        allowed_tools=allowed_tools,
        can_use_tool=partial(
            base_agent_permission_handler,
            iter_dir=iter_dir,
        )
    )
    
    logger.info(f"🔧 Allowed tools: {', '.join(allowed_tools)}")
    
    # Run base agent with streaming prompt
    async with ClaudeSDKClient(options=options) as client:
        message_count = 0
        await client.query(full_prompt)
        async for message in client.receive_response():
            message_count += 1
            log_message(message, logger, minimal_console=(run_dir is not None))
    logger.info(f"Base-agent completed with {message_count} messages")
    
    # Clean up irrelevant files
    cleanup_irrelevant_files(iter_dir, agent_type="base", logger=logger)
    
    # Verify that required files were created
    return _verify_base_agent_outputs(iter_dir, logger, message_count=message_count, evolve_retrieval=evolve_retrieval)


if __name__ == "__main__":
    import argparse
    
    async def main():
        parser = argparse.ArgumentParser(description="Run base-agent to learn context")
        parser.add_argument("iter_dir", type=str, help="Iteration directory (e.g., workspace/finer/iter0)")
        parser.add_argument("--env", type=str, choices=["finer", "formula", "uspto"], default="finer", help="Environment type")
        parser.add_argument("--iteration", type=int, default=None, help="Iteration number")
        args = parser.parse_args()
        
        # Load task instruction based on environment
        if args.env == "finer":
            from env.finer.task_instruction import task_instruction
        elif args.env == "formula":
            from env.formula.task_instruction import task_instruction
        else:
            print(f"✗ Unknown environment: {args.env}")
            return
        
        iter_dir = Path(args.iter_dir).resolve()
        workspace_base = iter_dir.parent
        
        # Check for required files from meta-agent
        skill_path = iter_dir / ".claude" / "skills" / "learning-context" / "SKILL.md"
        
        if not skill_path.exists():
            print(f"✗ SKILL.md not found at {skill_path}")
            print("  Run meta-agent first to generate it.")
            return
        
        result = await run_base_agent(
            iter_dir=iter_dir,
            task_instruction=task_instruction,
            workspace_base=workspace_base,
            iteration=args.iteration
        )
        
        if result['success']:
            print(f"\n✓ Base-agent completed successfully")
            print(f"  Generated: {iter_dir}/retrieve_context.py")
            print(f"  Generated: {iter_dir}/context/")
        else:
            print(f"\n✗ Base-agent failed: {result['error']}")
    
    asyncio.run(main())

