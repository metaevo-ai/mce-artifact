# Meta Context Engineering (MCE)

## Overview

We introduce **Meta Context Engineering (MCE)**, a bi-level framework that supersedes static CE heuristics by co-evolving *CE skills* and *context artifacts*.
In MCE iterations, a meta-level agent refines engineering skills via *agentic crossover*, a deliberative search over the history of skills, their executions, and evaluations.
A base-level agent executes these skills, learns from training rollouts, and optimizes context as flexible files and code. Our experiments evaluate MCE across five disparate domains under both offline and online settings. MCE demonstrates consistent performance gains, achieving 5.6--53.8\% relative improvement over state-of-the-art agentic CE methods (mean of 16.9\%), while maintaining superior context and adaptation efficiency.

## Project Structure

```
mce-assets-public/
├── mce/                          # Core MCE framework
│   ├── main.py                   # Offline training loop
│   ├── main_online.py            # Online learning mode
│   ├── eval.py                   # Evaluation module
│   ├── base_agent.py             # Base-level agent (context optimizer)
│   ├── meta_agent.py             # Meta-level agent (skill evolver)
│   ├── llm_client.py             # LLM client with OpenRouter/OpenAI support
│   ├── prompts/                  # Agent prompts
│   └── workspace_utils/          # Utilities for workspace operations
├── env/                          # Evaluation environments
│   ├── aegis2/                   # AI safety classification
│   ├── finer/                    # XBRL financial entity recognition
│   ├── symptom_diagnosis/        # Medical symptom-to-disease mapping
│   ├── uspto/                    # Chemical retrosynthesis
│   ├── crime_prediction/         # Crime prediction task
│   └── base.py                   # Base environment interface
├── assets/                       # Pre-trained assets
│   ├── context/                  # Learned context artifacts per environment
│   │   ├── aegis/mce/            # MCE-learned context for aegis
│   │   ├── finer/mce/            # MCE-learned context for finer
│   │   └── ...
│   └── skills/                   # CE skills per environment
│       ├── finer/                # Initial and optimal skills
│       └── ...
├── scripts/                      # Training and evaluation scripts
│   ├── train_*.sh                # Offline training scripts
│   ├── train_*_online.sh         # Online training scripts
│   └── eval_*_mce.sh             # Evaluation scripts
├── pyproject.toml                # Project dependencies
└── .env.template                 # Environment variables template
```

## Installation

```bash
# Install uv
curl -fsSL https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
uv pip install -e .
```

## Configuration

Copy `.env.template` to `.env` and set your API keys:

```bash
cp .env.template .env
```

The system uses **OpenRouter** by default with automatic fallback to **OpenAI**:

```bash
# Option 1: OpenRouter (recommended)
export OPENROUTER_API_KEY="your-api-key"
export OPENROUTER_API_BASE="https://openrouter.ai/api/v1"

# Option 2: OpenAI (fallback if OpenRouter not set)
export OPENAI_API_KEY="your-api-key"
export OPENAI_API_BASE="https://api.openai.com/v1"  # Optional

# To use Claude agent SDK
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# If you are using OpenRouter
export ANTHROPIC_BASE_URL=https://openrouter.ai/api
export ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY"
export ANTHROPIC_API_KEY=""

# Set default models for Claude agent SDK
export ANTHROPIC_DEFAULT_SONNET_MODEL="minimax/minimax-m2.1"
export ANTHROPIC_DEFAULT_OPUS_MODEL="minimax/minimax-m2.1"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="minimax/minimax-m2.1"
```

### E2B Sandbox (TODO, currently not tested)

For isolated agent execution in cloud sandboxes:

```bash
export E2B_API_KEY="your-e2b-api-key"
```

**Note**: E2B sandboxes on the Hobby billing plan have a default timeout of 1 hour. For long-running tasks, you can periodically resume training from checkpoints.

## Usage

### Quick Start with Scripts

The `scripts/` directory contains ready-to-use training and evaluation scripts for all environments:

| Script | Description |
|--------|-------------|
| `train_aegis.sh` | Offline training for AI safety (aegis2) |
| `train_finer.sh` | Offline training for XBRL tagging |
| `train_s2d.sh` | Offline training for symptom-to-disease |
| `train_uspto.sh` | Offline training for retrosynthesis |
| `train_crime_prediction.sh` | Offline training for crime prediction |
| `train_*_online.sh` | Online learning variants |
| `eval_*_mce.sh` | Evaluate MCE-learned context |

Run any script directly:

```bash
bash scripts/train_finer.sh
bash scripts/eval_finer_mce.sh
```

### Offline Training (mce.main)

Offline training uses a bi-level loop where meta-agent evolves skills and base-agent optimizes context:

```bash
uv run python -m mce.main \
    --workspace "workspace/finer" \
    --env "finer" \
    --train-data "env/finer/data/train.jsonl" \
    --val-data "env/finer/data/val.jsonl" \
    --model "deepseek/deepseek-chat-v3.1" \
    --iterations 5 \
    --start-iter 1 \
    --train-limit 200 \
    --val-limit 100 \
    --log-dir "logs/finer" \
    --train-batch-size 50
```

#### Offline Training Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--workspace` | Path to workspace directory (required) | - |
| `--env` | Environment name: `finer`, `aegis2`, `symptom_diagnosis`, `uspto`, `crime_prediction` (required) | - |
| `--train-data` | Path to training data JSONL file | - |
| `--val-data` | Path to validation data JSONL file | - |
| `--model` | LLM model for evaluation (OpenRouter format) | `deepseek/deepseek-chat-v3.1` |
| `--iterations` | Number of MCE iterations | 1 |
| `--start-iter` | Starting iteration number (for resuming) | 1 |
| `--train-limit` | Number of training samples per iteration | 50 |
| `--val-limit` | Number of validation samples | 20 |
| `--train-batch-size` | Batch size for sub-iterations | 50 |
| `--log-dir` | Directory for log files | `logs` |
| `--evolve-retrieval` | Enable retrieval function evolution | False |
| `--skill-path` | Path to pre-evolved skill (skips meta-agent) | None |
| `--no-meta-agent` | Skip meta-agent entirely (no skills) | False |
| `--use-e2b` | Run agents in E2B sandbox | False |

### Online Learning (mce.main_online)

Online mode learns directly from test data without a separate training/validation split:

```bash
uv run python mce/main_online.py \
    --workspace "workspace/finer_online" \
    --env "finer" \
    --test-data "env/finer/data/test.jsonl" \
    --test-limit 100 \
    --train-batch-size 5 \
    --data-accumulation-limit 0 \
    --model "deepseek/deepseek-chat-v3.1" \
    --log-dir "logs/finer_online"
```

#### Online Learning Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--workspace` | Path to workspace directory (required) | - |
| `--env` | Environment name (required) | - |
| `--test-data` | Path to test data JSONL file (required) | - |
| `--test-limit` | Total test samples to process | 100 |
| `--train-batch-size` | Samples per batch | 20 |
| `--data-accumulation-limit` | Max accumulated samples (0 = unlimited) | 0 |
| `--model` | LLM model for evaluation | `deepseek/deepseek-chat-v3.1` |
| `--skill-path` | Path to initial skill directory | None |
| `--log-dir` | Directory for log files | `logs` |
| `--continue-training` | Resume from last completed sub-iteration | False |
| `--use-e2b` | Run agents in E2B sandbox | False |

### Evaluation (mce.eval)

Evaluate learned context on test data:

```bash
uv run python -m mce.eval \
    --iter_dir "assets/context/finer/mce/context-l" \
    --env "finer" \
    --data "env/finer/data/test.jsonl" \
    --limit 500 \
    --model "deepseek/deepseek-chat-v3.1" \
    --save-results-to "results/finer_mce"
```

#### Evaluation Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--iter_dir` | Path to context directory with `retrieve_context.py` | - |
| `--env` | Environment name (required) | - |
| `--data` | Path to test data JSONL file (required) | - |
| `--limit` | Number of samples to evaluate | 500 |
| `--model` | LLM model for evaluation | `deepseek/deepseek-chat-v3.1` |
| `--save-results-to` | Directory to save results (required) | - |


### Using Pre-trained Context

The `assets/context/` directory contains MCE-learned context for each environment. To evaluate:

```bash
bash scripts/eval_finer_mce.sh
bash scripts/eval_aegis_mce.sh
bash scripts/eval_symptom_mce.sh
bash scripts/eval_crime_prediction_mce.sh
bash scripts/eval_uspto_mce.sh
```


