from pathlib import Path

def build_base_agent_prompt(
    task_instruction: str, 
    iter_dir: str, 
    workspace_base: str = None,
    initial_prompt: str = None,
    evolve_retrieval: bool = False,
) -> str:
    """
    Build the base agent prompt with task-specific instruction.
    
    Args:
        task_instruction: Task-specific instruction from env
        iter_dir: Iteration directory path (this is the working directory)
        workspace_base: Base workspace directory (for reference only)
        initial_prompt: Optional initial prompt (only for iter1 without seed context)
        
    Returns:
        Formatted prompt string
    """
    iter_name = Path(iter_dir).name  # e.g., "iter1"
    
    # Build conditional sections based on evolve_retrieval
    if evolve_retrieval:
        expected_outputs = """## Expected Outputs

1. **Context Files** (`context/`): Learned context files
2. **Retrieval Function** (`retrieve_context.py`):

```python
from pathlib import Path

def retrieval_function(question: str) -> str:
    \"\"\"Return relevant context for the given question.\"\"\"
    # CRITICAL: Use absolute paths to read context files
    # The retrieval function will be called from different working directories during evaluation
    script_dir = Path(__file__).parent.resolve()
    
    # Example: Read a context file using absolute path
    context_file = script_dir / "context" / "example.md"
    with open(context_file, 'r') as f:
        content = f.read()
    
    return content
```"""
        
        validation_note = """**Before finishing, validate your implementation**:
Run the validation script to ensure everything is correct:
```bash
uv run python utils/validate_base.py .
```

This script will verify:
- `context/` has markdown files with substantive content
- `retrieve_context.py` exists with correct signature: `def retrieval_function(question: str) -> str:`
- Retrieval function can be imported and returns non-empty strings

Only finish after all validations pass (✅). If any validation fails (❌), fix the issues and re-run the script."""
    else:
        expected_outputs = """## Expected Outputs

1. **Context Files** (`context/`): Learned context in markdown files

**NOTE**: Retrieval function is handled automatically. The system will use full retrieval (all context concatenated), so focus ONLY on creating high-quality, well-organized context files."""
        
        validation_note = ""

    prompt = f'''# Context Engineer

## Task Overview

{task_instruction}

## Working Directory

**Working Directory**: `{iter_dir}`

Your directory contains:
```
{iter_name}/
  .claude/skills/learning-context/SKILL.md  # Your skill guidance (MUST READ THIS)
  context/                                   # Prior best context (modify/replace)
  retrieve_context.py                        # Prior best retrieval
  data/
    train.json                               # Prior best context's evaluation results
  utils/
    llm.py                                   # LLM calls (call_llm)
    embedding.py                             # Embeddings (compute_embedding_similarity)
```

**File Access**:
- Read/Write: Only files within `{iter_dir}/`
- You CANNOT access any other directories or files outside of your iteration directory

{expected_outputs}

## Skill Guidance

**IMPORTANT**: Read `.claude/skills/learning-context/SKILL.md` for your learning methodology. Execute the skill to create effective context.

## Available Utilities

```python
# LLM calls (use sparingly - expensive)
from utils.llm import call_llm
# Batch text responses
responses = call_llm(["Question 1?", "Question 2?"])
for r in responses:
    print(r)  # Each r is a string

# Structured response with Pydantic schema
from pydantic import BaseModel, Field

class Analysis(BaseModel):
    pattern: str = Field(description="The identified pattern")
    confidence: float = Field(description="Confidence score 0-1")

# Batch structured responses
results = call_llm(["Analyze A", "Analyze B"], schema=Analysis)
for r in results:
    print(r.pattern)

# Embeddings
from utils.embedding import compute_embedding_similarity
# Compute similarity matrix between two lists of strings
similarity_matrix = compute_embedding_similarity(
    ["text 1", "text 2"],  # First list
    ["text A", "text B"]   # Second list
)
# Returns shape (len(strings_a), len(strings_b)) with cosine similarities
```

## Core Objective: Learn from Training Data

**CRITICAL**: Your primary goal is to analyze `data/train.json` and update context to fix ALL incorrect predictions.

### Training Data Analysis

1. **Load and inspect** `data/train.json`:
    - `summary`: Overall metrics
    - `detailed_results`: List of rollouts

2. **Analyze both incorrect AND correct predictions**:
   - **Incorrect predictions**:
     - **Why did the model answer incorrectly?** (wrong knowledge, missing pattern, incorrect format, calculation error)
     - **What context would have prevented this mistake?** (specific facts, rules, examples, procedures)
     - **How can this generalize?** (identify the underlying pattern, not just the specific instance)
   
   - **Correct predictions**:
     - **What patterns led to success?** (correct reasoning, effective context usage, proper format)
     - **Can we extract reusable strategies?** (identify what worked and why)
     - **How to reinforce these patterns?** (make successful approaches more explicit in context)

3. **Update context strategically**:
   - **Add missing knowledge**: If model lacked domain facts, add them with clear examples
   - **Clarify ambiguous rules**: If model misinterpreted, make rules explicit and unambiguous
   - **Provide error-correcting patterns**: Show correct approach with before/after examples

### Quality Standard

Your context must achieve TWO goals simultaneously:

1. **Fix All Incorrect Predictions**: Every incorrect sample in `data/train.json` must be addressable by your updated context
   - For each incorrect sample, ask: "If the model had retrieved the right context, would it have answered correctly?"
   - If NO, your context is incomplete—add what's missing

2. **Generalization**: Context must work on unseen examples, not just memorize training data
   - Extract **patterns** and **principles**, not just specific answers
   - Use training examples as **illustrations** of general rules
   - Ensure retrieval logic can match new questions to relevant context

## Environment

Use `uv run python ...` for all Python execution.

{validation_note}

Work efficiently: focus on impactful changes, avoid over-analysis, finish promptly once validated.
'''
    
    # Append initial_prompt at the end if provided (for iter1 without seed context)
    if initial_prompt:
        prompt += f"\n\n## Additional Instructions\n\n{initial_prompt}"
    
    return prompt
