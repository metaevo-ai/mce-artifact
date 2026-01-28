"""
Meta-agent implementation using Claude Agent SDK.

The meta-agent generates and evolves skills for the base-level context learning agent.
"""

import asyncio
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from claude_agent_sdk import query, ClaudeAgentOptions, ClaudeSDKClient
import os
import json
import re
from functools import partial

from mce.logging_utils import log_message, setup_logger
from mce.prompts.meta_agent import build_meta_agent_prompt
from mce.utils import cleanup_irrelevant_files

from dotenv import load_dotenv

load_dotenv(override=True)


def _verify_meta_agent_outputs(
    iter_dir: Path,
    logger: logging.Logger,
) -> Dict[str, Any]:
    """
    Verify that meta-agent generated required files and read them.
    
    Args:
        iter_dir: Iteration directory
        logger: Logger instance
        
    Returns:
        Dictionary with success status and skill_md
    """
    skills_dir = iter_dir / ".claude" / "skills" / "learning-context"
    skill_file = skills_dir / "SKILL.md"
    
    if not skill_file.exists():
        logger.error(f"Meta-agent did not generate SKILL.md at {skill_file}")
        return {
            'success': False,
            'error': f"Meta-agent did not generate SKILL.md at {skill_file}",
            'skill_md': None,
        }
    
    skill_md = skill_file.read_text()
    
    logger.info(f"✓ Generated SKILL.md ({len(skill_md)} chars)")
    
    return {
        'success': True,
        'skill_md': skill_md,
        'error': None
    }


async def _meta_agent_permission_handler(
    tool_name: str,
    input_data: dict,
    context: dict,
    iter_dir: Path,
):
    """
    Permission handler for meta-agent with skill database access.
    
    The meta-agent can:
    - Read files anywhere in workspace_base (for skill database inspection)
    - Write/Edit files ONLY in current iter_dir/.claude/skills/ and INITIAL_PROMPT.md
    """
    workspace_base = iter_dir.parent.resolve()
    iter_dir = iter_dir.resolve()

    # Define allowed tools
    allowed_tools = ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "Task", "TaskOutput", "ExitPlanMode", "TodoWrite", "KillShell", "EnterPlanMode"]
    
    # Check if tool is in allowed list
    if tool_name not in allowed_tools:
        return {
            "behavior": "deny",
            "message": f"Tool '{tool_name}' is not allowed. Allowed tools: {', '.join(allowed_tools)}",
            "interrupt": False  # Don't interrupt, just deny
        }
    
    # Tools that involve file paths
    file_tools = ["Read", "Write", "Edit", "Glob", "Grep"]
    
    if tool_name in file_tools:
        # Get the file path from (file_path for write and read; path for glob and grep)
        file_path = input_data.get("file_path") or input_data.get("path")
        
        if file_path:
            # Resolve the absolute path
            if not Path(file_path).is_absolute():
                resolved_path = (workspace_base / file_path).resolve()
            else:
                resolved_path = Path(file_path).resolve()
            
            # For read operations, allow anywhere in workspace_base
            if tool_name in ["Read", "Glob", "Grep"]:
                try:
                    resolved_path.relative_to(workspace_base)
                    return {"behavior": "allow", "updatedInput": input_data}
                except ValueError:
                    return {
                        "behavior": "deny",
                        "message": f"Access denied: Read operations restricted to workspace ({workspace_base})",
                        "interrupt": True
                    }
            
            # For write/edit operations, only allow in current skill dir
            if tool_name in ["Write", "Edit"]:
                skills_dir = iter_dir / ".claude" / "skills"
                
                # Allow writing to .claude/skills/ only
                try:
                    resolved_path.relative_to(skills_dir)
                    return {"behavior": "allow", "updatedInput": input_data}
                except ValueError:
                    return {
                        "behavior": "deny",
                        "message": f"Access denied: Write operations restricted to {skills_dir}",
                        "interrupt": True
                    }

    # Allow the operation
    return {
        "behavior": "allow",
        "updatedInput": input_data
    }


async def run_meta_agent(
    iter_dir: Path,
    task_instruction: str,
    iteration: int,
    workspace_base: Path = None,
    run_dir: Path = None,
    e2b_sandbox_manager = None,
    evolve_retrieval: bool = False,
) -> Dict[str, Any]:
    """
    Run meta-agent to generate/evolve skills through agentic crossover.
    
    The meta-agent:
    1. Accesses the implicit skill database (workspace history of iterations)
    2. Analyzes previous iterations: (iter_i, design overview, validation acc)
    3. Performs agentic crossover on ideas and strategies
    4. Actively inspects detailed implementations when needed
    5. Generates new skills for the base-level agent
    
    Args:
        iter_dir: Iteration directory
        task_instruction: Task-specific instruction from env
        iteration: Current iteration number
        workspace_base: Base workspace directory (optional, derived from iter_dir if not provided)
        run_dir: Run directory for organized logging
        e2b_sandbox_manager: E2B sandbox manager (None = run locally)
        evolve_retrieval: Whether to evolve retrieval function
    """
    workspace_base = Path(iter_dir.parent) if workspace_base is None else Path(workspace_base)
    
    # Setup iteration-specific logger
    logger = setup_logger(
        name=f"meta_iter{iteration}",
        run_dir=run_dir,
        agent_type="meta",
        iteration=iteration,
        minimal_console=True
    )
    
    # Run meta-agent using Claude Agent SDK
    allowed_tools = ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "Task", "TaskOutput", "ExitPlanMode", "TodoWrite", "KillShell", "EnterPlanMode"]
    
    # Build prompt based on execution environment
    if e2b_sandbox_manager:
        # Build prompt with E2B paths
        meta_prompt = build_meta_agent_prompt(
            task_instruction=task_instruction,
            iter_dir=f"/workspace/{iter_dir.name}",
            workspace_base="/workspace",
            evolve_retrieval=evolve_retrieval,
        )
    else:
        # Build prompt with local paths
        meta_prompt = build_meta_agent_prompt(
            task_instruction=task_instruction,
            iter_dir=str(iter_dir),
            workspace_base=str(workspace_base),
            evolve_retrieval=evolve_retrieval,
        )
    
    # Log the prompt
    logger.info("📝 META-AGENT PROMPT:")
    logger.info(f"\n{meta_prompt}\n")
    
    # Run agent in E2B sandbox if manager is provided
    if e2b_sandbox_manager:
        logger.info("🔒 Running agent in E2B sandbox")
        try:
            result = await e2b_sandbox_manager.run_agent(
                iter_dir=iter_dir,
                prompt=meta_prompt,
                allowed_tools=allowed_tools,
                timeout=1800,  # 30 minutes
                logger=logger,
            )
            
            if not result["success"]:
                logger.error(f"E2B sandbox execution failed: {result.get('stderr', 'Unknown error')}")
                return {
                    'success': False,
                    'error': f"E2B sandbox execution failed: {result.get('stderr', 'Unknown error')}",
                    'skill_md': None,
                }
            
            logger.info("✓ E2B sandbox execution completed")
            logger.info(f"  stdout: {result['stdout'][:500]}...")  # Log first 500 chars
            
            # Clean up irrelevant files
            cleanup_irrelevant_files(iter_dir, agent_type="meta", logger=logger)
            
            # Verify and read generated files
            return _verify_meta_agent_outputs(iter_dir, logger)

        except Exception as e:
            logger.error(f"E2B sandbox execution failed: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'skill_md': None,
            }
    
    # Original local execution path
    else:
        # Original local execution path
        options = ClaudeAgentOptions(
            cwd=str(workspace_base),  # Set to workspace base for skill database access
            allowed_tools=allowed_tools,
            can_use_tool=partial(
                _meta_agent_permission_handler, 
                iter_dir=iter_dir, 
            )
        )

    # Run agent with the meta-prompt
    async with ClaudeSDKClient(options=options) as client:
        message_count = 0
        await client.query(meta_prompt)
        async for message in client.receive_response():
            message_count += 1
            log_message(message, logger, minimal_console=True)
    
    logger.info(f"Meta-agent completed with {message_count} messages")

    # Clean up irrelevant files
    cleanup_irrelevant_files(iter_dir, agent_type="meta", logger=logger)

    # Verify and read generated files
    return _verify_meta_agent_outputs(iter_dir, logger)

if __name__ == "__main__":
    import argparse
    
    async def main():
        parser = argparse.ArgumentParser(description="Run meta-agent to generate/evolve skills")
        parser.add_argument("iter_dir", type=str, help="Iteration directory (e.g., workspace/finer/iter1)")
        parser.add_argument("--env", type=str, choices=["finer", "formula", "uspto"], default="finer", help="Environment type")
        parser.add_argument("--iteration", type=int, required=True, help="Iteration number")
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
        
        result = await run_meta_agent(
            iter_dir=iter_dir,
            task_instruction=task_instruction,
            iteration=args.iteration,
            workspace_base=workspace_base
        )
        
        if result['success']:
            print(f"\n✓ Meta-agent completed successfully")
            print(f"  Generated: {iter_dir}/.claude/skills/learning-context/SKILL.md")
        else:
            print(f"\n✗ Meta-agent failed: {result['error']}")
    
    asyncio.run(main())

