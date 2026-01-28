"""
Evaluate current context and context policy on samples with async and concurrent execution.
"""

import asyncio
import json
import sys
import logging
import importlib.util
from typing import Callable, Dict, List, Any
from env.base import Sample
from env import get_environment
from pydantic import BaseModel, Field
import traceback
from pathlib import Path
from mce.llm_client import LLMClient
from mce.utils import compute_avg_metrics

from dotenv import load_dotenv

load_dotenv(override=True)

logger = logging.getLogger(__name__)

MAX_CONCURRENCY = 30


async def generic_generator_prompt(sample: Sample, playbook_context: str) -> str:
    """Generate a simple prompt for the task."""
    prompt = f"""You are an expert domain problem solver.

Task Context:
{sample.context}

Instructional Context:
{playbook_context}

Question: {sample.question}

You MUST respond with a valid JSON object containing exactly two fields:
1. "reasoning": Your step-by-step analysis (string)
2. "final_answer": Your concise final answer (string)
"""
    return prompt


class GeneratorSchema(BaseModel):
    """Unified schema for Generator output."""

    reasoning: str = Field(description="Your step-by-step analysis and calculations")
    final_answer: str = Field(description="Your concise final answer")


def load_retrieval_function(iter_dir: Path) -> Callable[[str], str]:
    """
    Dynamically load retrieval function from an iteration directory.

    Args:
        iter_dir: Iteration directory containing retrieve_context.py
    
    Returns:
        The retrieval_function callable
    
    Raises:
        FileNotFoundError: If retrieve_context.py doesn't exist
        AttributeError: If retrieval_function is not found in the module
        Exception: For other import errors
    """
    retrieve_script = iter_dir / "retrieve_context.py"
    
    if not retrieve_script.exists():
        raise FileNotFoundError(f"retrieve_context.py not found in {iter_dir}")
    
    # Load the module dynamically
    spec = importlib.util.spec_from_file_location("retrieve_context", retrieve_script)
    if spec is None or spec.loader is None:
        raise Exception(f"Could not load module spec from {retrieve_script}")
    
    module = importlib.util.module_from_spec(spec)
    
    # Add iter_dir to sys.path temporarily so imports work
    sys.path.insert(0, str(iter_dir))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(str(iter_dir))
    
    if not hasattr(module, 'retrieval_function'):
        raise AttributeError(f"retrieval_function not found in {retrieve_script}")
    
    retrieval_function = getattr(module, 'retrieval_function')
    
    if not callable(retrieval_function):
        raise TypeError(f"retrieval_function in {retrieve_script} is not callable")
    
    return retrieval_function


async def batch_solve(
    retrieval_function: Callable,
    samples: List[Sample],
    env: str,
    llm,
) -> Dict[str, Any]:
    """
    Evaluate samples with direct question-answer mapping.
    
    Args:
        retrieval_function: Function to retrieve context for a given question
        samples: List of Sample objects to evaluate
        env: Environment name for evaluation logic
        llm: LLM client instance to use for evaluation
    
    Returns:
        Dictionary with evaluation results including summary, errors, and failures
    """
    environment = get_environment(env)
    
    # Evaluate samples concurrently with semaphore for rate limiting
    semaphore = asyncio.Semaphore(MAX_CONCURRENCY)
    completed_count = 0
    total_count = len(samples)
    
    async def solve_single(sample: Sample) -> Dict[str, Any]:
        """
        Evaluate a single sample.
        
        Returns a nested structure with all fields:
        {
            "sample": {id, question, context, ground_truth, ...extras},
            "llm_output": {all fields from generator schema},
            "evaluation": {playbook_context, feedback, metrics}
        }
        """
        nonlocal completed_count
        async with semaphore:
            # Retrieve context for this question
            try:
                playbook_context = retrieval_function(sample.question) if retrieval_function else ""
            except Exception as e:
                playbook_context = ""
                logger.error(f"Error retrieving context for sample {sample.id}: {e}")

            context_length = len(playbook_context)
    
            # Generate prompt using environment-specific method
            prompt = await environment.get_generator_prompt(sample, playbook_context)
            # Generate answer with structured output parsing (timeout handled in LLM client)
            generator_output = await llm.ainvoke(
                prompt,
                parse_function=environment.parse_structured_output
            )
            final_answer = generator_output.final_answer
            # Evaluate using environment
            result = await environment.aevaluate(sample, final_answer)
            
            completed_count += 1
            print(f"\rProgress: {completed_count}/{total_count} ({completed_count/total_count*100:.1f}%) [Context: {context_length} chars]", end="", flush=True)
            
            # Return nested structure with all fields
            return {
                "sample": sample.to_dict(),
                "llm_output": generator_output.model_dump() if hasattr(generator_output, 'model_dump') else {"final_answer": str(generator_output)},
                "evaluation": {
                    "playbook_context": playbook_context,
                    "feedback": result.feedback,
                    "metrics": result.metrics,
                }
            }
    
    # Run all evaluations concurrently
    logger.info(f"Processing {total_count} samples with max concurrency of {MAX_CONCURRENCY}...")
    results = await asyncio.gather(*[solve_single(sample) for sample in samples])
    
    # Separate evaluation errors (program failures) and successful evaluations
    eval_errors = [r for r in results if "error" in r]
    successful = [r for r in results if "error" not in r]
    
    # Compute average metrics
    avg_metrics = compute_avg_metrics(successful)
    
    primary_metric_name = environment.get_primary_metric_name()
    primary_metric_value = avg_metrics.get(primary_metric_name, 0.0)
    
    # Calculate statistics
    avg_context_length = sum(
        len(r.get("evaluation", {}).get("playbook_context", "")) 
        for r in successful
    ) / len(successful) if successful else 0
    
    # Return evaluation results - just metrics and all instances
    log_data = {
        "summary": {
            "metrics": avg_metrics,  # All metrics averaged
            "primary_metric": primary_metric_name,  # Which metric is primary
            "primary_metric_value": primary_metric_value,  # Primary metric value
            "total": len(results),
            "errors": len(eval_errors),  # Program failures
            "avg_context_length": int(avg_context_length),
            "environment": env,
        },
        "errors": eval_errors,  # Program failures (structurally different)
        "results": successful,  # All successful results - caller can filter as needed
    }
    
    # Log summary
    logger.info(f"Evaluation Summary:")
    logger.info(f"  Primary Metric ({primary_metric_name}): {primary_metric_value:.2%}")
    logger.info(f"  Total: {len(results)} ({len(successful)} successful, {len(eval_errors)} errors)")
    logger.info(f"  Avg Context Length: {int(avg_context_length)} chars")

    return log_data


async def main():
    """Standalone evaluation script for testing learned context from workspace folders."""
    import argparse
    import time
    from .logging_utils import setup_logger
    
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Evaluate learned context from a workspace folder"
    )
    parser.add_argument(
        "--iter_dir",
        type=str,
        default="",
        help="Path to the iteration directory (e.g., workspace/finer/iter0)"
    )
    parser.add_argument(
        "--env",
        type=str,
        default="finer",
        help="Environment type (default: finer)"
    )
    parser.add_argument(
        "--data",
        type=str,
        required=True,
        help="Path to data file"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=500,
        help="Number of samples to evaluate (default: 500)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="deepseek/deepseek-chat-v3.1",
        help="LLM model to use"
    )
    parser.add_argument(
        "--save-results-to",
        type=str,
        required=True,
        help="Directory to save results to"
    )
    
    args = parser.parse_args()
    
    # Setup logger
    eval_logger = setup_logger(name="eval", log_dir="logs", console_colors=True)
    
    # Resolve iteration directory path
    
    if args.iter_dir:
        iter_dir = Path(args.iter_dir).resolve()
        if not iter_dir.exists() or not iter_dir.is_dir():
            raise ValueError(f"Iteration directory error: {iter_dir}")
    else:
        iter_dir = None
    
    eval_logger.info("="*80)
    eval_logger.info("EVALUATION SETUP")
    eval_logger.info("="*80)
    eval_logger.info(f"Iteration directory: {iter_dir}")
    eval_logger.info(f"Environment: {args.env}")
    eval_logger.info(f"Data: {args.data}")
    eval_logger.info(f"Sample limit: {args.limit}")
    
    # Load retrieval function from iteration directory
    if iter_dir:
        eval_logger.info("Loading retrieval function...")
        retrieval_fn = load_retrieval_function(iter_dir)
        eval_logger.info(f"✓ Loaded retrieval_function from {iter_dir / 'retrieve_context.py'}")
    else:
        retrieval_fn = None
    # Load environment
    env_instance = get_environment(args.env)
    
    # Initialize LLM
    eval_logger.info(f"Initializing LLM: {args.model}")
    llm = LLMClient(model=args.model)
    eval_logger.info("✓ LLM initialized")
    
    # Run evaluation
    eval_logger.info("="*80)
    eval_logger.info("STARTING EVALUATION")
    eval_logger.info("="*80)
    
    # Load samples
    samples = env_instance.load_samples(path=args.data, limit=args.limit, random_sample=False)
    eval_logger.info(f"📦 Loaded {len(samples)} samples from: {args.data}")
    
    start_time = time.time()
    
    results = await batch_solve(
        retrieval_function=retrieval_fn if retrieval_fn else None,
        samples=samples,
        env=args.env,
        llm=llm,
    )
    
    elapsed = time.time() - start_time
    summary = results["summary"]

    print(f"✓ Completed: {summary['primary_metric']} ({summary['total']} samples) in {elapsed:.0f}s")
    
    # Save results
    save_dir = Path(args.save_results_to)
    save_dir.mkdir(parents=True, exist_ok=True)
    log_path = save_dir / "evaluation.json"
    
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    eval_logger.info(f"📁 Results saved to: {log_path}")
    eval_logger.info("="*80)
    
if __name__ == "__main__":
    asyncio.run(main())