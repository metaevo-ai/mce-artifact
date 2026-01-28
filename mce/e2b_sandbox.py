"""
E2B Sandbox integration for running agents in isolated environments.

This module provides a sandbox wrapper that:
1. Runs agents in E2B cloud sandboxes (Firecracker micro-VMs)
2. Automatically syncs results back to local filesystem
3. Reuses sandbox instance across multiple agent runs for efficiency
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from e2b_code_interpreter import Sandbox
from e2b.sandbox.filesystem.filesystem import FileType


class E2BSandboxManager:
    """
    Manager for E2B sandbox lifecycle.
    """
    
    def __init__(self, workspace_base: Path, timeout: int = 3600):
        """
        Initialize sandbox manager.
        
        Args:
            workspace_base: Base workspace directory
            timeout: Sandbox timeout in seconds (default: 1 hour)
        """
        self.workspace_base = workspace_base
        self.timeout = timeout
        self.sandbox: Optional[Sandbox] = None
        self._initialized = False
    
    def initialize(self):
        """Initialize sandbox and upload workspace."""
        if self._initialized:
            return
        
        print("[E2B] Initializing sandbox...")
        self.sandbox = Sandbox.create(timeout=self.timeout)
        
        # Upload workspace
        print("[E2B] Uploading workspace...")
        self._upload_workspace()
        
        # Set environment variables
        # Collect environment variables to pass to sandbox (store as instance variable)
        self.env_vars = {
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY", ""),
            "ANTHROPIC_BASE_URL": os.getenv("ANTHROPIC_BASE_URL", ""),
            "ANTHROPIC_AUTH_TOKEN": os.getenv("ANTHROPIC_AUTH_TOKEN", ""),
            "OPENROUTER_API_KEY": os.getenv("OPENROUTER_API_KEY", ""),
            "OPENROUTER_API_BASE": os.getenv("OPENROUTER_API_BASE", ""),
            "ANTHROPIC_DEFAULT_SONNET_MODEL": os.getenv("ANTHROPIC_DEFAULT_SONNET_MODEL", ""),
            "ANTHROPIC_DEFAULT_OPUS_MODEL": os.getenv("ANTHROPIC_DEFAULT_OPUS_MODEL", ""),
            "ANTHROPIC_DEFAULT_HAIKU_MODEL": os.getenv("ANTHROPIC_DEFAULT_HAIKU_MODEL", ""),
            "SANDBOX_MODEL": os.getenv("SANDBOX_MODEL", ""),
            "MAX_LLM_CALLS": os.getenv("MAX_LLM_CALLS", ""),
        }
        
        # Install uv and dependencies once
        print("[E2B] Installing uv and dependencies...")
        # Install uv to /usr/local/bin (system-wide)
        uv_install = self.sandbox.commands.run(
            "curl -LsSf https://astral.sh/uv/install.sh | sh && export PATH=$HOME/.local/bin:$PATH",
            timeout=120
        )
        if uv_install.exit_code != 0:
            raise RuntimeError(f"Failed to install uv: {uv_install.stderr}")
        
        # Install dependencies using uv (uv is now in PATH)
        install_result = self.sandbox.commands.run(
            "export PATH=$HOME/.local/bin:$PATH && cd /workspace && uv pip install --system claude-agent-sdk langchain langchain-openai langchain-core",
            timeout=180
        )
        
        if install_result.exit_code != 0:
            raise RuntimeError(f"Failed to install dependencies: {install_result.stderr}")
        
        self._initialized = True
        print("[E2B] Sandbox initialized successfully")
    
    def _should_upload_file(self, rel_path: Path) -> bool:
        """
        Determine if a file should be uploaded to sandbox.
        
        Excludes:
        - agent_messages.jsonl (generated during agent runs)
        - __pycache__ directories
        - .pyc files
        - .DS_Store files
        
        Args:
            rel_path: Relative path from workspace_base
            
        Returns:
            True if file should be uploaded, False otherwise
        """
        path_str = rel_path.as_posix()
        
        # Exclude agent message logs
        if rel_path.name == "agent_messages.jsonl":
            return False
        
        # Exclude Python cache
        if "__pycache__" in path_str:
            return False
        
        if rel_path.suffix == ".pyc":
            return False
        
        # Exclude system files
        if rel_path.name == ".DS_Store":
            return False
        
        return True
    
    def _upload_workspace(self):
        """Upload workspace_base to sandbox, excluding irrelevant files."""
        for item in self.workspace_base.rglob("*"):
            if item.is_file():
                rel_path = item.relative_to(self.workspace_base)
                
                # Skip files that shouldn't be uploaded
                if not self._should_upload_file(rel_path):
                    continue
                
                remote_path = f"/workspace/{rel_path.as_posix()}"
                content = item.read_bytes()
                try:
                    # Ensure parent directory exists
                    remote_parent = "/".join(remote_path.split("/")[:-1])
                    if remote_parent != "/workspace":
                        try:
                            self.sandbox.commands.run(f"mkdir -p {remote_parent}", timeout=5)
                        except:
                            pass
                    self.sandbox.files.write(remote_path, content)
                except Exception as e:
                    print(f"Warning: Failed to upload {remote_path}: {e}")
    
    def sync_evaluation_data(self, workspace_base: Path):
        """
        Upload all JSON/JSONL files from data/ and iter*/logs/ to sandbox.
        This ensures agents can access all evaluation data and logs from previous iterations.
        
        Data structure:
        - data/: Contains training data (e.g., train.jsonl)
        - iter*/logs/: Contains evaluation results and trajectories for each iteration
        
        Args:
            workspace_base: Local workspace base directory
        """
        # 1. Sync all JSON/JSONL files in data/ directory (training data)
        data_dir = workspace_base / "data"
        if data_dir.exists():
            # Ensure data directory exists in sandbox
            self.sandbox.commands.run("mkdir -p /workspace/data", timeout=5)
            
            # Upload all .json and .jsonl files
            for file_path in data_dir.glob("*.json*"):
                if file_path.is_file():
                    remote_path = f"/workspace/data/{file_path.name}"
                    content = file_path.read_bytes()
                    self.sandbox.files.write(remote_path, content)
                    print(f"[E2B] Synced data/{file_path.name}")
        
        # 2. Sync all JSON/JSONL files in iter*/logs/ directories
        # This includes evaluation.json and train_trajectories.jsonl (for sequential tasks)
        for iter_dir in sorted(workspace_base.glob("iter*")):
            if not iter_dir.is_dir():
                continue
            
            logs_dir = iter_dir / "logs"
            if logs_dir.exists():
                iter_name = iter_dir.name
                remote_logs_dir = f"/workspace/{iter_name}/logs"
                self.sandbox.commands.run(f"mkdir -p {remote_logs_dir}", timeout=5)
                
                # Upload all .json and .jsonl files
                for file_path in logs_dir.glob("*.json*"):
                    if file_path.is_file():
                        remote_path = f"{remote_logs_dir}/{file_path.name}"
                        content = file_path.read_bytes()
                        self.sandbox.files.write(remote_path, content)
                        print(f"[E2B] Synced {iter_name}/logs/{file_path.name}")
    
    def sync_iteration_results(self, iter_dir: Path):
        """
        Download results from current iteration back to local filesystem.
        
        Args:
            iter_dir: Local iteration directory to sync to
        """
        iter_name = iter_dir.name
        remote_iter_dir = f"/workspace/{iter_name}"
        
        iter_dir.mkdir(parents=True, exist_ok=True)
        self._download_directory(remote_iter_dir, iter_dir)
    
    def _download_directory(self, remote_dir: str, local_dir: Path):
        """Recursively download directory from sandbox."""
        local_dir.mkdir(parents=True, exist_ok=True)
        files = self.sandbox.files.list(remote_dir)
        for f in files:
            remote_path = f"{remote_dir}/{f.name}"
            local_path = local_dir / f.name
            
            if f.type == FileType.DIR:
                local_path.mkdir(exist_ok=True)
                self._download_directory(remote_path, local_path)
            else:
                try:
                    content = self.sandbox.files.read(remote_path, format="bytes")
                    local_path.parent.mkdir(parents=True, exist_ok=True)
                    local_path.write_bytes(content)
                except Exception as e:
                    print(f"Warning: Failed to download {remote_path}: {e}")

    async def run_agent(
        self,
        iter_dir: Path,
        prompt: str,
        allowed_tools: list,
        timeout: int = 1200,
        logger = None,
    ) -> Dict[str, Any]:
        """
        Run agent in sandbox without writing prompt to file.
        
        Args:
            iter_dir: Current iteration directory
            prompt: Agent prompt (passed as command line argument)
            allowed_tools: List of allowed tools
            timeout: Execution timeout in seconds
            logger: Optional logger for logging messages
            
        Returns:
            Dictionary with execution results
        """
        if not self._initialized:
            self.initialize()
        
        # Sync evaluation data from previous iterations (logs + trajectories)
        self.sync_evaluation_data(self.workspace_base)
        
        iter_name = iter_dir.name
        
        # Write prompt to a temporary file for robustness
        prompt_file = f"/workspace/{iter_name}/.agent_prompt.txt"
        self.sandbox.files.write(prompt_file, prompt.encode('utf-8'))
        
        # Create agent runner script that reads prompt from file and logs messages
        agent_script = f'''import asyncio
import sys
import json
from pathlib import Path
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

async def main():
    # Read prompt from file and immediately delete it
    workspace_base = Path("/workspace")
    prompt_file = workspace_base / "{iter_name}" / ".agent_prompt.txt"
    prompt = prompt_file.read_text()
    prompt_file.unlink()  # Delete immediately after reading
    
    log_file = workspace_base / "{iter_name}" / "agent_messages.jsonl"
    
    options = ClaudeAgentOptions(
        cwd=str(workspace_base),
        allowed_tools={allowed_tools!r},
    )
    
    message_count = 0
    async with ClaudeSDKClient(options=options) as client:
        await client.query(prompt)
        async for message in client.receive_response():
            message_count += 1
            # Print to stdout
            print(f"Message {{message_count}}: {{type(message).__name__}}", flush=True)
            # Log to file as JSON
            with open(log_file, "a") as f:
                f.write(json.dumps({{"count": message_count, "type": str(type(message).__name__), "message": str(message)}}) + "\\n")
    
    print(f"Total messages: {{message_count}}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
'''
        
        # Write runner script
        self.sandbox.files.write("/workspace/run_agent.py", agent_script.encode('utf-8'))
        
        # Execute agent
        # Use uv run to execute Python (consistent with local environment)
        # Build environment variable exports
        env_exports = " && ".join([f"export {k}='{v}'" for k, v in self.env_vars.items() if v])
        
        print(f"[E2B] Running agent for {iter_name}...")
        result = self.sandbox.commands.run(
            f"export PATH=$HOME/.local/bin:$PATH && {env_exports} && cd /workspace && uv run python run_agent.py",
            timeout=timeout
        )
        
        # Sync results back (including agent_messages.jsonl)
        self.sync_iteration_results(iter_dir)
        
        # If logger provided, replay messages from log file
        if logger:
            log_file = iter_dir / "agent_messages.jsonl"
            if log_file.exists():
                try:
                    with open(log_file, "r") as f:
                        for line in f:
                            msg_data = json.loads(line)
                            logger.info(f"[E2B Message {msg_data['count']}] {msg_data['type']}")
                    
                    # Delete local agent_messages.jsonl after replaying
                    log_file.unlink()
                    print(f"[E2B] Deleted local agent_messages.jsonl")
                    
                    # Delete agent_messages.jsonl from sandbox
                    remote_log_file = f"/workspace/{iter_name}/agent_messages.jsonl"
                    self.sandbox.commands.run(f"rm -f {remote_log_file}", timeout=5)
                    print(f"[E2B] Deleted sandbox agent_messages.jsonl")
                    
                except Exception as e:
                    logger.warning(f"Failed to replay messages from log: {e}")
        
        return {
            "success": result.exit_code == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.exit_code,
        }
    
    def cleanup(self):
        """Cleanup sandbox resources."""
        if self.sandbox:
            try:
                print("[E2B] Killing sandbox...")
                self.sandbox.kill()
            except Exception as e:
                print(f"Warning: Failed to kill sandbox: {e}")
            finally:
                self.sandbox = None
                self._initialized = False
