# Error-Driven Generalization for XBRL Tag Classification

## Skill Overview

This skill guides the base agent to analyze prediction errors from training evaluations, extract **generalizable principles** from those errors, and incrementally refine context by pruning overfitted content while building on existing knowledge. The key innovation is focusing on **why** errors occur at a semantic level, not memorizing specific examples.

## Core Philosophy

The previous iteration captured 29 specific patterns, but the 4.5% train/val gap indicates overfitting to training examples. This iteration prioritizes:
1. **Abstract principles over specific examples** - What makes a pattern generalizable?
2. **Semantic reasoning chains** - How should the model *think* about classification, not just what to answer
3. **Cross-example patterns** - Identify themes across multiple errors rather than isolated mistakes

## Methodology

### Phase 1: Load Existing Context (Build Upon, Don't Rebuild)

```python
from utils.llm import call_llm

# Read existing context files
existing_semantic = read_file("context/semantic-guidance.md")
existing_tag_ref = read_file("context/tag-reference.md")
existing_patterns = read_file("context/common-patterns.md")
```

**Key Principle**: The existing context contains valuable knowledge. Your goal is to *refine and generalize*, not discard and start over.

### Phase 2: Analyze Error Patterns Systematically

Load training evaluation results and categorize errors by *type of reasoning failure*:

#### Error Taxonomy Categories:

1. **Superficial Pattern Matching** (most common overfitting signal)
   - Error: Model sees "$X facility" and selects MaximumBorrowingCapacity without deeper analysis
   - Fix: Add reasoning steps that question the initial pattern match

2. **Missing Semantic Distinction**
   - Error: Confusing facility capacity (Maximum) with current state (Current) or debt instrument (Face)
   - Fix: Strengthen the semantic boundary definitions

3. **Context Blindness**
   - Error: Ignoring key words like "outstanding principal balance" vs "principal amount"
   - Fix: Highlight critical context words that change meaning

4. **Category Confusion**
   - Error: Confusing interest rate types (Stated vs Basis Spread) or debt value types (Face vs Fair vs Carrying)
   - Fix: Clarify the fundamental categories and their boundaries

### Phase 3: Extract Generalizable Principles (Not Examples)

For each error type, derive abstract rules:

**BAD** (Too Specific - Example-Dependent):
```
"Tranche A loan facility of up to $16.0 million" → DebtInstrumentFaceAmount
```

**GOOD** (Generalizable Principle):
```
If the facility is a TRANCHE or TERM LOAN (not revolving), it represents
a specific debt instrument principal, NOT a flexible borrowing capacity.
Key indicators: "Tranche A/B", "term loan", "loan facility" (vs "credit facility")
```

**BAD** (Too Specific):
```
"$400.0 million facility with $90.5M borrowings outstanding" → CurrentBorrowingCapacity
```

**GOOD** (Generalizable Principle):
```
When a facility amount is given WITH a breakdown showing what has been borrowed
vs unused, the facility amount refers to CURRENT borrowed state, not maximum limit.
Pattern: "$X facility with [amount] borrowings outstanding and [amount] unused"
```

### Phase 4: Cross-Error Pattern Synthesis

Group errors that share the same underlying reasoning failure:

```python
# Example grouping from error analysis
error_groups = {
    "facility_type_confusion": [
        "Tranche A loan facility → FaceAmount (not Maximum)",
        "Term loan facility → FaceAmount (not Maximum)",
        "Revolving credit facility → Maximum (not FaceAmount)",
        "Note Purchase Agreement → Maximum (not FaceAmount)"
    ],
    "state_vs_capacity_confusion": [
        "Facility with breakdown → Current state",
        "Outstanding under facility → CarryingAmount",
        "Allowing to borrow up to X → Current mechanism"
    ],
    "interest_rate_type_confusion": [
        "Plus/above LIBOR → BasisSpread",
        "Rate on note → StatedPercentage",
        "Issue price % → RedemptionPrice"
    ]
}
```

For each group, create ONE generalizable rule that covers all cases:

```
## Facility Type Resolution

When classifying dollar amounts associated with facilities, first determine
the FACILITY TYPE, which determines the tag category:

1. REVOLVING CREDIT FACILITY / CREDIT FACILITY
   → Capacity tags: MaximumBorrowingCapacity, CurrentBorrowingCapacity, RemainingBorrowingCapacity
   → Key: These have flexible borrowing limits

2. TERM LOAN FACILITY / TRANCHE FACILITY / LOAN FACILITY
   → Debt instrument tags: FaceAmount, CarryingAmount
   → Key: These are specific debt instruments with fixed principals

3. NOTE PURCHASE AGREEMENT / PRIVATE SHELF AGREEMENT
   → Capacity tags: MaximumBorrowingCapacity
   → Key: These establish facility limits for future note purchases

RESOLUTION RULE: The facility NAME itself tells you the category.
Look for: "revolving", "credit facility", "term loan", "tranche", "loan facility", "shelf agreement"
```

### Phase 5: Refine Existing Context Incrementally

For each section in the existing context:

1. **READ** the existing rule/pattern
2. **ASK**: "Is this a generalizable principle or a specific example?"
3. **IF SPECIFIC EXAMPLE**: Transform it into a generalizable rule, or remove if not representative
4. **IF ALREADY GENERAL**: Keep it, but add a "Reasoning Chain" section
5. **ADD** a "Common Pitfalls" section based on error analysis
6. **UPDATE** with newly discovered generalizable patterns

### Phase 6: Add Reasoning Chains (Anti-Overfitting Measure)

For each major decision point, add explicit reasoning steps:

```markdown
## Decision Chain: Classifying Dollar Amounts

When you encounter a dollar amount in a financial context, follow this chain:

STEP 1: What TYPE of entity is this?
   [ ] Dollar amount of money
   [ ] Percentage
   [ ] Non-numeric entity (go to LineOfCredit check)

STEP 2: If Dollar Amount → What CATEGORY of financial instrument?
   [ ] Credit facility capacity (revolving, commitment, limit)
   [ ] Specific debt instrument (notes, bonds, loans)
   [ ] Long-term debt balance (general, not specific instrument)
   [ ] Letters of credit
   [ ] Discount/unamortized amount

STEP 3: If Credit Facility → What SPECIFIC ASPECT?
   [ ] Maximum limit available (use MaximumBorrowingCapacity)
   [ ] Currently borrowed/outstanding (use CurrentBorrowingCapacity)
   [ ] Available but unused (use RemainingBorrowingCapacity)
   [ ] Just the facility exists, no amount specified (use LineOfCredit)

STEP 4: If Debt Instrument → What SPECIFIC ASPECT?
   [ ] Original principal/face amount (use FaceAmount)
   [ ] Current book value including accrued interest (use CarryingAmount)
   [ ] Fair market value estimate (use FairValue)
   [ ] Remaining discount (use UnamortizedDiscount)

STEP 5: If Percentage → What TYPE of rate?
   [ ] Margin/spread ADDED to benchmark (use BasisSpreadOnVariableRate)
   [ ] TOTAL rate STATED on instrument (use StatedPercentage)
   [ ] Price for redemption (use RedemptionPricePercentage)
```

### Phase 7: Create Anti-Patterns Section

Document what NOT to do, based on common errors:

```markdown
## Anti-Patterns (What Causes Errors)

### Anti-Pattern 1: Facility Word Trigger
PROBLEM: Seeing "$X facility" or "$X credit facility" and immediately
selecting MaximumBorrowingCapacity without checking the facility type.

WRONG: "$16.0 million Tranche A loan facility" → MaximumBorrowingCapacity
RIGHT: "$16.0 million Tranche A loan facility" → DebtInstrumentFaceAmount

REASONING: "Tranche A loan" signals a specific debt instrument, not a
revolving capacity. The facility type name is the key discriminator.

### Anti-Pattern 2: "Outstanding" Always Means CurrentBorrowingCapacity
PROBLEM: Seeing "outstanding" and selecting CurrentBorrowingCapacity
without considering what is outstanding.

WRONG: "$60 million outstanding under the Revolving Credit Facility" → CurrentBorrowingCapacity
RIGHT: "$60 million outstanding under the Revolving Credit Facility" → DebtInstrumentCarryingAmount

REASONING: "Outstanding under [facility]" refers to the debt instrument's
carrying amount, not the facility's current borrowing capacity. The phrasing
"under the facility" indicates the debt, not the facility itself.

### Anti-Pattern 3: Any "Fair Value" Is LongTermDebtFairValue
PROBLEM: Seeing "fair value" and selecting LongTermDebtFairValue without
checking if it's specific notes or general long-term debt.

CORRECT: "fair value of long-term debt" → LongTermDebtFairValue
ALSO CORRECT: "fair value of these Notes" → LongTermDebtFairValue

NOTE: LongTermDebtFairValue is correct for BOTH general long-term debt
AND specific notes. The key is it's a FAIR VALUE, not carrying amount.
```

### Phase 8: Write Updated Context

Organize the refined context into three files:

1. **reasoning-chains.md**: Step-by-step decision processes for classification
2. **semantic-principles.md**: Generalizable rules and anti-patterns
3. **tag-reference.md**: Per-tag quick reference (condensed from iteration 1)

## Key Principles for This Iteration

1. **One Principle, Many Examples**: Each rule should explain the *reasoning*, not just show examples
2. **Reasoning Chains Over Memorization**: Force explicit thinking steps, not pattern matching
3. **Cross-Validation Thinking**: Ask "Would this rule work for different but similar examples?"
4. **Principle Hierarchy**:
   - Level 1: Category boundaries (what category does this belong to?)
   - Level 2: Within-category distinctions (what specific tag within the category?)
   - Level 3: Edge cases and exceptions (what's unusual about this case?)

## Quality Check Before Finalizing

For each section, verify:

- [ ] Does this rule explain *why*, not just *what*?
- [ ] Would this work for a similar but different example not in training?
- [ ] Is this more about semantic category than surface pattern?
- [ ] Does this build on existing context rather than duplicating it?
- [ ] Have I removed overly specific examples that don't generalize?

## Implementation Guidance

### Using LLM for Error Analysis

```python
from utils.llm import call_llm

# Analyze a batch of errors to find common themes
error_batch = [e for e in detailed_results if not e['is_correct']]
analysis_prompt = f"""
Analyze these {len(error_batch)} errors from training:

{chr(10).join([f"ID {e['id']}: LLM={e['llm_answer']}, Correct={e['target']}, Question={e['question'][:200]}..."
               for e in error_batch[:15]])}

Group these errors by their underlying REASONING FAILURE (not by the wrong answer).
For each group, describe the cognitive mistake the model made and propose
one generalizable rule that would prevent this entire class of errors.
"""
themes = call_llm(analysis_prompt)
```

### Using LLM to Generalize Specific Rules

```python
# Take a specific pattern and make it general
specific_pattern = "Tranche A loan facility of up to $X → DebtInstrumentFaceAmount"
generalization_prompt = f"""
Convert this specific pattern into a generalizable rule:

{specific_pattern}

What is the underlying principle? What other similar patterns would this rule cover?
Express as a rule that doesn't mention the specific example.
"""
generalized_rule = call_llm(generalization_prompt)
```

### Using LLM to Create Reasoning Chains

```python
# Create explicit reasoning steps for a decision point
decision_point = "Distinguishing MaximumBorrowingCapacity from DebtInstrumentFaceAmount"
chain_prompt = f"""
Create a step-by-step reasoning chain for:

{decision_point}

Include 3-5 decision steps that force explicit thinking about the category
boundaries. Each step should ask a question that leads to the correct answer.
"""
reasoning_chain = call_llm(chain_prompt)
```

## Success Metrics

This iteration succeeds if:
1. Context contains more reasoning principles than specific examples
2. Each major decision has an explicit reasoning chain
3. Anti-patterns section exists and documents common mistakes
4. The context can generalize to novel examples not in training
5. Validation accuracy improves while training accuracy may slightly decrease (reduced overfitting)
