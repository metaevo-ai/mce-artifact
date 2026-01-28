from pathlib import Path
import json
import re

def build_meta_agent_prompt(
    task_instruction: str,
    iter_dir: str,
    workspace_base: str,
    evolve_retrieval: bool = False,
) -> str:
    """
    Build the meta agent prompt with task-specific instruction and iteration context.
    
    Args:
        task_instruction: Task-specific instruction from env
        iter_dir: Iteration directory path
        workspace_base: Workspace base directory path
        
    Returns:
        Formatted prompt string
    """
    iter_name = Path(iter_dir).name  # e.g., "iter1" or "iter1_sub0"
    # Extract iteration number, handling both "iter1" and "iter1_sub0" formats
    iter_part = iter_name.split("iter")[1]  # "1" or "1_sub0"
    current_iteration = int(iter_part.split("_")[0])  # Extract just the number
    skill_database = _build_skill_database(workspace_base, current_iteration)
    
    # Build retrieval-specific sections conditionally
    if evolve_retrieval:
        base_output_desc = """- Receives your skill + training rollouts + prior best context artifacts
- Executes the skill to learn and update context
- Output: `context/` files + `retrieve_context.py`"""
        
        retrieval_output_req = """
**`{iter_name}/.claude/skills/learning-context/SKILL.md`**:
- MUST include `## Skill Overview` section (distinguishes from other iterations)
- Describe a complete learning procedure
- NO iteration-specific references (e.g., "improve iter2's approach")
- Mention useful utilities (`utils/llm.py`, `utils/embedding.py`)
- Include clear methodology and implementation guidance
- NOTE: This skill will be automatically copied to `meta_agent/skills/iter{current_iteration}/` for future review"""
    else:
        base_output_desc = """- Receives your skill + training data + prior best context artifacts
- Executes the skill to learn and update context
- Output: `context/` files only (retrieval function is automatically set to full retrieval)"""
        
        retrieval_output_req = """
**`{iter_name}/.claude/skills/learning-context/SKILL.md`**:
- MUST include `## Skill Overview` section (distinguishes from other iterations)
- Describe a complete learning procedure for context curation
- NO iteration-specific references (e.g., "improve iter2's approach")
- Mention useful utilities (`utils/llm.py`, `utils/embedding.py`)
- Include clear methodology and implementation guidance
- NOTE: Retrieval is handled automatically (full context retrieval), focus ONLY on context curation
- NOTE: This skill will be automatically copied to `meta_agent/skills/iter{current_iteration}/` for future review"""
    
    return f"""# Meta-Level Agent: Skill Evolution for Context Engineering

## Task Overview

{task_instruction}

## Your Role

You are a **meta-level agent** that evolves context engineering skills across iterations. Your goal is to design self-contained skills that teach a base agent how to learn optimal task-specific context from training data.

Each skill you create should be a complete learning procedure that can be understood and executed independently, without reference to specific iteration numbers or prior attempts.

## Architecture

**Meta-Level (You)**:
- Analyze iteration history (skills → implementations → results)
- Perform agentic crossover to evolve better skills
- Output: `{iter_name}/.claude/skills/learning-context/SKILL.md`

**Base-Level (Context Engineer)**:
{base_output_desc}

**Key Flow**: Base-agent starts with the BEST context from previous iterations and UPDATES it based on your skill's instructions. It does NOT start from scratch—it refines existing knowledge.

## Working Directory

**Working Directory**: `{workspace_base}`

```
{workspace_base}/
  meta_agent/                                  # READ FROM HERE for iteration history
    train.jsonl                                 # Full training dataset for holistic task understanding (can be very large, handle it gracefully)
    evaluations.json                            # AGGREGATED METRICS: Read this to see train_acc, val_acc for all iterations
    skills/                                     # PREVIOUS SKILLS: Read these to understand what was tried
      iter1/SKILL.md                            # Skill from iteration 1
      iter2/SKILL.md                            # Skill from iteration 2
  iter1_sub0/, iter1_sub1/, ...                 # Sub-iteration folders (read-only, for reference only)
    .claude/skills/learning-context/SKILL.md   # Skill that guided learning (copied to all sub-iters)
    context/                                    # Learned context (markdown files)
    retrieve_context.py                         # Retrieval logic
    utils/
      llm.py                                    # LLM utilities (call_llm, structured output)
      embedding.py                              # Embedding utilities (compute_embedding_similarity)
    data/
      train.json                                # Training rollouts for this batch

```

**Write Access**: Only `{iter_name}/.claude/skills/`

**IMPORTANT**: To review iteration history, you can read from `meta_agent/evaluations.json` and `meta_agent/skills/`.

## Skill Database (Iteration History)

{skill_database}

## Your Task

1. **Review Iteration History**: 
   - Read `meta_agent/evaluations.json` for performance metrics (train_acc, val_acc) of all previous iterations
   - Read skills from `meta_agent/skills/iter*/SKILL.md` to understand what strategies were tried
   - Analyze: What strategies worked? What failed?
   - **Overfitting Check**: Is train accuracy significantly higher than validation accuracy? If so, the skill may be memorizing training examples rather than learning generalizable patterns.
   - **Underfitting Check**: Are both train and validation accuracies low? If so, the skill may not be extracting enough useful context or patterns from the data.

2. **Agentic Crossover**: Combine successful elements, address failure patterns, innovate

3. **Evolve Skill**: Design a skill that guides the base-agent to UPDATE and IMPROVE the prior best context (not rebuild from scratch).


## Skill Examples

### Example Skill A: Direct Agentic Curation

```markdown
## Skill Overview
Directly analyze training data (with inference results) and curates context in a fully agentic manner—reading incorrect predictions, identifying patterns, and updating context files without heavy LLM scaffolding.

## Methodology
1. **Load prior best context**: Read existing context files from `context/` directory
2. **Scan evaluation results**: Load `data/train.json`
3. **Analyze incorrect prediction patterns**: 
   - Group incorrect predictions by mistake type (e.g., wrong format, missing knowledge, calculation error)
   - Identify recurring themes across multiple incorrect predictions
   - Extract concrete examples of what went wrong and why
4. **Update context incrementally**:
   - ADD new sections for newly discovered mistake patterns
   - UPDATE existing sections with refined guidance based on new errors
   - REMOVE or REFINE sections that may be causing overfitting
   - Organize by task-relevant categories (e.g., by formula type, entity type, reaction class)

## Key Principles
- Build upon existing context, don't discard working patterns
- Let the agent's reasoning drive curation, not rigid LLM-call loops
- Prioritize high-impact patterns (frequent mistakes > rare edge cases)
- Focus on generalizable patterns that improve validation performance
```

### Example Skill B: ACE-Style Reflection & Curation

```markdown
## Skill Overview
Use LLM calls for structured reflection on incorrect predictions, then programmatically curate insights into context while building on prior knowledge.

## Methodology
1. **Load existing context**: Read current context files from `context/` directory to understand what's already known
2. **Load training results**: Load `data/train.json` (contains: summary + detailed_results with id, question, llm_answer, target, is_correct)
3. **Reflect on errors**: For each incorrect sample, call LLM to reflect: "Why did the model answer incorrectly? What knowledge was missing?"
4. **Incrementally curate insights**: 
   - ADD new insights for novel error patterns
   - UPDATE existing insights with refined guidance
   - MERGE duplicates to avoid redundancy
5. **Save updated context**: Write curated context to `context/` files

## Implementation Hint
```python
from utils.llm import call_llm
# Load existing context first
existing_context = read_context_files()

# Simple text response
reflection = call_llm(f"Model answered '{{llm_answer}}' but correct is '{{target}}'. What knowledge was missing?")
# reflection is a string

# Or use structured output for better parsing
from pydantic import BaseModel, Field
class ErrorAnalysis(BaseModel):
    missing_knowledge: str = Field(description="What knowledge was missing")
    suggested_context: str = Field(description="What to add to context")

analysis = call_llm(f"Analyze error: model said '{{llm_answer}}' but correct is '{{target}}'", schema=ErrorAnalysis)
# analysis.missing_knowledge and analysis.suggested_context are now available

# Update context incrementally based on reflection
updated_context = merge_insights(existing_context, reflection)
```
```

### Example Skill C: Clustering + Batch Synthesis

```markdown
## Skill Overview
Group training samples by characteristics, then synthesize context per group for coherent organization.

## Methodology
1. Extract features from training data (question type, domain tags, entity categories)
2. Cluster samples using rule-based grouping
3. For each cluster: analyze patterns, synthesize dedicated context section
```

## Output Requirements

{retrieval_output_req}

**Before finishing, verify**:
- SKILL.md exists in `{iter_name}/.claude/skills/learning-context/SKILL.md`
- SKILL.md has a clear `## Skill Overview` section

Begin by analyzing the skill database and evolving the next generation skill. You work efficiently without compromising the quality of the skill.
"""



def _build_skill_database(workspace_base, current_iteration: int) -> str:
    """Build a summary of the skill database (history of all previous iterations)."""
    if current_iteration == 0:
        return "No previous iterations (this is iteration 0). Design an initial skill based on the task and examples."
    
    if current_iteration == 1:
        return "No previous iterations (this is iteration 1, iter0 is baseline with no skills). Design an initial skill based on the task and examples above."
    
    workspace_base = Path(workspace_base)
    meta_agent_dir = workspace_base / "meta_agent"
    
    # Load aggregated evaluations
    evaluations_file = meta_agent_dir / "evaluations.json"
    if not evaluations_file.exists():
        raise FileNotFoundError(
            f"Aggregated evaluations file not found at {evaluations_file}. "
            "This file should have been created by previous iterations."
        )
    
    with open(evaluations_file) as f:
        evaluations = json.load(f)
    
    database_entries = []
    
    for i in range(1, current_iteration):  # Start from 1 (skip iter0 baseline)
        iter_key = f"iter{i}"
        
        if iter_key not in evaluations:
            # This shouldn't happen, but handle gracefully
            continue
        
        iter_data = evaluations[iter_key]
        
        # Get metrics - use actual metric names (e.g., train_accuracy, val_accuracy)
        # Find the primary metric by looking for train_* and val_* fields
        train_metrics = iter_data.get('train_metrics', {})
        val_metrics = iter_data.get('val_metrics', {})
        
        # Get primary metric name (first metric in val_metrics)
        primary_metric_name = next(iter(val_metrics)) if val_metrics else "accuracy"
        
        # Get train and val values for primary metric
        train_value = iter_data.get(f'train_{primary_metric_name}')
        val_value = iter_data.get(f'val_{primary_metric_name}')
        
        # Assert that we have both metrics
        assert train_value is not None, f"train_{primary_metric_name} missing for {iter_key} in {evaluations_file}"
        assert val_value is not None, f"val_{primary_metric_name} missing for {iter_key} in {evaluations_file}"
        
        train_str = f"{train_value:.2%}"
        val_str = f"{val_value:.2%}"
        
        # Build metrics display (show all metrics if more than one)
        metrics_display = f"**Train {primary_metric_name.capitalize()}**: {train_str} | **Val {primary_metric_name.capitalize()}**: {val_str}"
        if len(val_metrics) > 1:
            other_metrics = [f"{k}={v:.2%}" for k, v in val_metrics.items()]
            metrics_display += f"\n- **All Val Metrics**: {', '.join(other_metrics)}"
        
        # Get skill overview from meta_agent/skills/
        skill_file = meta_agent_dir / "skills" / iter_key / "SKILL.md"
        skill_overview = _extract_skill_overview(skill_file)
        
        # Get additional metadata
        num_sub_iters = iter_data.get('num_sub_iters', 1)
        total_rollouts = iter_data.get('total_rollouts', 0)
        last_sub_folder = iter_data.get('last_sub_folder', f'iter{i}')

        entry = f"""### Iteration {i}
- {metrics_display}
- **Rollouts**: {total_rollouts} ({num_sub_iters} sub-iteration{"s" if num_sub_iters > 1 else ""})
- **Skill Overview**:
{skill_overview}
- **Files**: `meta_agent/skills/iter{i}/SKILL.md`, `{last_sub_folder}/context/`, `{last_sub_folder}/retrieve_context.py`"""
        database_entries.append(entry)
    
    if not database_entries:
        return "No previous iterations available (only baseline iter0 exists)."
    
    return "\n\n".join(database_entries)



def _extract_skill_overview(skill_path: Path) -> str:
    """Extract the '## Skill Overview' section from SKILL.md."""
    if not skill_path.exists():
        return "  (SKILL.md not found)"
    
    try:
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return f"  (error reading file: {e})"
    
    # Find "## Skill Overview" section
    pattern = r'^##\s*Skill\s+Overview\s*$'
    match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
    
    if not match:
        return "  (no '## Skill Overview' section found)"
    
    # Extract until next ## heading or end of file
    start_pos = match.end()
    next_match = re.search(r'\n##\s+[^#]', content[start_pos:])
    
    if next_match:
        overview_content = content[start_pos:start_pos + next_match.start()].strip()
    else:
        overview_content = content[start_pos:].strip()
    
    if not overview_content:
        return "  (Skill Overview section is empty)"
    
    # Indent for formatting
    return "\n".join(f"  {line}" if line.strip() else "" for line in overview_content.split("\n"))


if __name__ == "__main__":
    print(build_meta_agent_prompt(
        task_instruction="my task instruction!!!!",
        iter_dir="/Users/yhr/Desktop/mce/workspace/finer/iter2",
        workspace_base="/Users/yhr/Desktop/mce/workspace/finer"
    ))
