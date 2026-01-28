## Skill Overview

This skill guides the base agent to UPDATE and IMPROVE the prior best context by analyzing training results, identifying high-impact pattern gaps, and refining the existing knowledge base.

## Methodology

### Phase 1: Load Prior Best Context and Training Results

1. **Load existing context**: Read all markdown files from `context/` directory to understand what's already documented
2. **Load training evaluation**: Read `data/train.json` containing:
   - `summary`: Overall metrics and statistics
   - `detailed_results`: Array of samples with `id`, `question`, `llm_answer`, `target`, `is_correct`
3. **Identify success patterns**: Extract samples where `is_correct: true` - these show what context is working
4. **Identify failure patterns**: Extract samples where `is_correct: false` - these show what needs improvement

### Phase 2: Analyze What Works (Success Pattern Mining)

For correct predictions, use LLM reflection to understand WHY they succeeded:

```python
from utils.llm import call_llm

def reflect_on_success(question, llm_answer, target):
    """Understand what context patterns led to correct prediction."""
    reaction_type = extract_reaction_type(question)

    success_prompt = f"""
    This retrosynthesis prediction was CORRECT.

    Question: {question}
    Model Answer: {llm_answer}
    Target: {target}
    Reaction Type: {reaction_type}

    Analyze:
    1. What chemical pattern did the model correctly identify?
    2. What reaction type classification was correct?
    3. What SMILES notation pattern was applied correctly?
    4. What context from the documentation was helpful?

    Extract 2-3 actionable patterns that can be documented for similar cases.
    """
    return call_llm(success_prompt)
```

**Goal**: Identify 5-10 "success patterns" that should be emphasized in the updated context

### Phase 3: Analyze What Failed (Failure Pattern Mining)

For incorrect predictions, use LLM reflection to identify root causes:

```python
def reflect_on_error(question, llm_answer, target):
    """Understand why prediction failed and what guidance is missing."""
    reaction_type = extract_reaction_type(question)
    product_smiles = extract_product_smiles(question)

    error_prompt = f"""
    This retrosynthesis prediction was INCORRECT.

    Question: {question}
    Model Answer: {llm_answer}
    Correct Target: {target}
    Reaction Type: {reaction_type}

    Analyze:
    1. What chemical pattern was misidentified or missed?
    2. What was the correct retrosynthetic disconnection?
    3. What SMILES notation rule was violated or misunderstood?
    4. What specific guidance would have helped avoid this error?

    Extract 2-3 specific, actionable improvements for the context documentation.
    """
    return call_llm(error_prompt)
```

**Goal**: Identify 10-15 "failure patterns" that need additional context guidance

### Phase 4: Categorize Patterns by Reaction Type

Group identified patterns by reaction type and prioritize by frequency:

| Reaction Type | Success Patterns | Failure Patterns | Priority |
|--------------|------------------|------------------|----------|
| Deprotections | X | Y | High/Med/Low |
| C-C Bond Formation | X | Y | High/Med/Low |
| FGI | X | Y | High/Med/Low |
| ... | ... | ... | ... |

**Prioritization Criteria**:
- **High Priority**: Patterns that appear in >3 training samples
- **Medium Priority**: Patterns that appear in 2-3 samples
- **Low Priority**: Unique edge cases (consider documenting but not emphasizing)

### Phase 5: Update Context Incrementally

For each high-priority pattern, UPDATE existing context files:

#### 5.1 Add Success Pattern Sections

In the appropriate reaction type file (e.g., `deprotections.md`), add:

```markdown
## ✅ What Works: Success Patterns

### Pattern: [Brief Description]

**When you see**: [SMILES pattern or structural feature]

**Do this**: [Retrosynthetic disconnection]

**Example**:
- Product: [SMILES]
- Precursor: [SMILES]
- Why it works: [Brief explanation]
```

#### 5.2 Refine Existing Error Sections

Review existing error documentation in `examples.md`:
- **Keep**: Error patterns that are genuinely high-frequency
- **Condense**: Long error explanations to 2-3 bullet points max
- **Remove**: Edge case errors that appear only once (these add noise)

#### 5.3 Add Decision Workflow Section

Create a new `context/workflow.md` file with step-by-step decision process:

```markdown
# Retrosynthesis Decision Workflow

## Step 1: Identify Reaction Type
- Look at the question: "The reaction type is ___"
- This tells you which context file to consult

## Step 2: Identify Key Functional Groups
- List all functional groups in the product SMILES
- Look for: carbonyls, heterocycles, halides, protecting groups

## Step 3: Apply Reaction-Specific Pattern
[Decision tree for this reaction type]

## Step 4: Verify SMILES Syntax
- Check ring numbering consistency
- Verify ester/ether protecting groups
- Confirm functional group connectivity
```

### Phase 6: Simplify and Prioritize

**Compression Strategy**:
1. Reduce `examples.md` from verbose error cases to concise pattern summaries
2. Keep only top 20 most common error patterns (remove unique edge cases)
3. Add explicit "COMMON PATTERNS" sections to each reaction type file
4. Create a `QUICK_REFERENCE.md` with condensed decision rules

**Structure After Update**:
```
context/
  retrosynthesis_guide.md    # Updated overview with key patterns highlighted
  QUICK_REFERENCE.md         # NEW: Condensed decision rules (max 100 lines)
  workflow.md               # NEW: Step-by-step decision process
  deprotections.md          # Added success patterns, simplified errors
  cc_bond_formation.md      # Added success patterns, simplified errors
  ... (other reaction type files)
  examples.md               # Reduced to top 20 high-frequency patterns
```

### Phase 7: Validate Context Coherence

1. **Cross-check**: Ensure success patterns and error patterns don't contradict
2. **Verify completeness**: All major reaction types should have both success and error patterns
3. **Check SMILES accuracy**: Ensure all example SMILES in context match training data format
4. **Test coherence**: Read through updated context as if you were the LLM making predictions

## Key Principles

1. **Update, Don't Rebuild**: Build upon existing context, preserve what's working
2. **Prioritize Action**: Patterns should be actionable, not just informative
3. **Success > Error**: Document what works more than what doesn't
4. **Simplify Ruthlessly**: Remove edge cases, focus on common patterns
5. **Workflow First**: Provide decision processes, not just information

## Implementation Hints

```python
# Load existing context
existing_context = {}
for file in Path("context").glob("*.md"):
    existing_context[file.name] = file.read_text()

# Load training results
with open("data/train.json") as f:
    training_data = json.load(f)

# Reflect on successes and errors
success_patterns = []
error_patterns = []

for sample in training_data["detailed_results"]:
    if sample["is_correct"]:
        pattern = reflect_on_success(sample["question"], sample["llm_answer"], sample["target"])
        success_patterns.append((sample["reaction_type"], pattern))
    else:
        pattern = reflect_on_error(sample["question"], sample["llm_answer"], sample["target"])
        error_patterns.append((sample["reaction_type"], pattern))

# Group by reaction type and prioritize
# Update context files incrementally
```

## Expected Outputs

After executing this skill, the `context/` directory should contain:
- `QUICK_REFERENCE.md` - Condensed decision rules (new file)
- `workflow.md` - Step-by-step decision process (new file)
- Updated `examples.md` - Simplified to top 20 patterns (max 300 lines)
- Updated reaction type files - Each with success patterns section added
- All files should be more concise and action-oriented than iteration 1

The base agent will automatically set retrieval to full retrieval, so all context will be available for inference.
