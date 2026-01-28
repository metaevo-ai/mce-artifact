# Learning Context for XBRL Tag Classification

## Skill Overview

This skill guides the base agent to analyze training data, identify semantic patterns in XBRL tag usage, and curate comprehensive context for accurate financial entity classification. The skill uses LLM-assisted pattern analysis combined with structured knowledge extraction.

## Methodology

### Phase 1: Load Prior Context and Data

1. **Check for existing context**: Read any files in `context/` directory to understand what knowledge is already captured
2. **Load training data**: Read `.meta_agent/train.jsonl` to analyze patterns
3. **Load evaluation results**: If available, read `data/train.json` to identify error patterns from previous iterations

### Phase 2: Analyze Tag Semantics and Distinguishing Features

Use LLM to analyze the training samples and extract key distinguishing features for each tag category. Focus on:

- **Linguistic cues**: Words/phrases that signal specific tag types
- **Numeric patterns**: Whether the entity is a percentage, dollar amount, etc.
- **Contextual dependencies**: What surrounding words determine the correct tag

### Phase 3: Extract Decision Rules Per Tag Category

For each unique tag in the training data, derive explicit decision rules:

1. **DebtInstrumentInterestRateStatedPercentage**: Look for percentage values (X.Y%) explicitly stated as the interest rate on notes/bonds
   - Key phrases: "% Senior Notes", "% notes due", "interest rate of X%", "bearing interest at X%"
   - Distinguish from: Basis spread (which is a margin ADDED to a benchmark rate)

2. **LineOfCreditFacilityMaximumBorrowingCapacity**: Look for credit facility capacity limits
   - Key phrases: "maximum borrowing capacity", "aggregate of $X billion", "committed lines of credit", "capacity was increased to $X"
   - Distinguish from: Current borrowing (which is what has been borrowed SO FAR)

3. **DebtInstrumentFaceAmount**: Look for principal amounts of specific debt instruments
   - Key phrases: "aggregate principal amount", "face amount", "principal balance of $X note", "repayment of $X"
   - Distinguish from: Fair value (which is market valuation, not face/par value)

4. **DebtInstrumentBasisSpreadOnVariableRate1**: Look for percentage margins on variable rate loans
   - Key phrases: "LIBOR plus X%", "margin ranging from X% to Y%", "basis spread", "plus a margin of X%"
   - Distinguish from: Stated interest rate (which is the TOTAL rate, not a margin added to benchmark)

5. **LongTermDebtFairValue**: Look for estimated/market-based valuations
   - Key phrases: "fair value", "quoted market prices", "estimate the fair value", "based on quoted prices"
   - Distinguish from: Carrying amount (book value) or face amount

6. **DebtInstrumentRedemptionPricePercentage**: Look for prices paid to redeem/repurchase debt
   - Key phrases: "redemption price equal to X%", "repurchase at a price equal to X%", "offer to holders at X%"
   - Distinguish from: Stated interest rate (this is a price percentage, not an interest rate)

7. **DebtInstrumentCarryingAmount**: Look for book/accounting values on balance sheet
   - Key phrases: "carrying amount", "balance including principal and accrued interest", "book value"
   - Distinguish from: Face amount (carrying amount may include accrued interest)

8. **LineOfCreditFacilityCurrentBorrowingCapacity**: Look for current outstanding borrowings against a facility
   - Key phrases: "current borrowing capacity", "borrowings outstanding", "amount outstanding", "drawn amount"
   - Distinguish from: Maximum capacity (which is the total available)

9. **LineOfCredit**: General line of credit references
   - Key phrases: "line of credit", "revolving credit facility", "bank guarantees", "no outstanding balance"
   - May not mention specific dollar amounts; refers to the facility itself

10. **LongTermDebt**: Long-term debt obligations (general)
    - Key phrases: "long-term debt", "term loan balance", "mortgage notes on land"
    - Distinguish from: Specific instrument types (FaceAmount, FairValue, etc.)

11. **LettersOfCreditOutstandingAmount**: Outstanding letters of credit
    - Key phrases: "letters of credit", "letter of credit issued", "letters of credit were outstanding"
    - Specific to LOC instruments, not general debt

12. **DebtInstrumentUnamortizedDiscount**: Remaining unamortized discounts
    - Key phrases: "unamortized discount", "discount remains unamortized", "discount on the Term Loan"
    - Specific accounting concept for debt discounts

### Phase 4: Build Semantic Disambiguation Guide

Create a decision tree/flowchart for distinguishing between commonly confused tags:

**Percentage Values**:
- Is it an interest rate STATED on the note? → `DebtInstrumentInterestRateStatedPercentage`
- Is it a margin ADDED to LIBOR/base rate? → `DebtInstrumentBasisSpreadOnVariableRate1`
- Is it a redemption/repurchase price? → `DebtInstrumentRedemptionPricePercentage`

**Dollar Amounts (Credit Facilities)**:
- Is it the MAXIMUM available to borrow? → `LineOfCreditFacilityMaximumBorrowingCapacity`
- Is it what has been borrowed SO FAR? → `LineOfCreditFacilityCurrentBorrowingCapacity`
- Does it just reference the facility generally? → `LineOfCredit`

**Dollar Amounts (Debt Instruments)**:
- Is it the stated PRINCIPAL/FACE value? → `DebtInstrumentFaceAmount`
- Is it the estimated MARKET value? → `LongTermDebtFairValue`
- Is it the BOOK value (with accrued interest)? → `DebtInstrumentCarryingAmount`
- Is it the remaining DISCOUNT amount? → `DebtInstrumentUnamortizedDiscount`
- Does it refer to the debt generally? → `LongTermDebt`
- Is it specifically about LETTERS OF CREDIT? → `LettersOfCreditOutstandingAmount`

### Phase 5: Create Reference Examples

For each tag, compile 2-3 exemplary question-answer pairs from training data that demonstrate:
- The entity value
- The surrounding context that signals the correct tag
- Why other similar tags would Phase 6: be incorrect

### Update and Organize Context Files

Write curated context to `context/` directory with the following structure:

1. **semantic-guidance.md**: Decision rules, disambiguation guide, key distinguishing phrases
2. **tag-reference.md**: Per-tag reference with examples and exclusion criteria
3. **common-patterns.md**: Frequently occurring patterns and their correct tags

## Implementation Guidance

### Using LLM for Pattern Analysis

```python
from utils.llm import call_llm

# Analyze samples for a specific tag
samples_for_tag = [s for s in training_data if s['target'] == tag_name]
analysis_prompt = f"""
Analyze these {len(samples_for_tag)} examples tagged as "{tag_name}":
{chr(10).join([s['question'] for s in samples_for_tag[:10]])}

Identify:
1. Common linguistic patterns that indicate this tag
2. Key phrases that distinguish it from similar tags
3. Common mistakes/confusion points with other tags
"""
patterns = call_llm(analysis_prompt)
```

### Handling Edge Cases

When analyzing training data, watch for:
- **Multi-million/billion formatting**: "$ 4.3 billion" vs "$ 4,300,000,000"
- **Currency variations**: $, £, €, etc. (all should be treated similarly)
- **Percentage ranges**: "from X% to Y%" - usually the range bounds are basis spreads
- **Percent signs in different positions**: "9.250 %" vs "9.250%" (both are percentages)

### Organization Principles

- Group by semantic category (debt instruments vs credit facilities)
- Within each category, order by frequency in training data
- Highlight the most common confusion points first
- Use concrete examples from training data as reference

## Key Distinctions to Emphasize

1. **Interest Rate vs Basis Spread**: Stated rate is the total; basis spread is added to benchmark
2. **Face Amount vs Fair Value vs Carrying Amount**: Par value vs market estimate vs book value
3. **Maximum vs Current Borrowing**: Capacity limit vs actual borrowed amount
4. **Percentage of Principal vs Redemption Price**: Interest rate vs repurchase price

## Quality Check

Before finalizing context, verify:
- Each tag has clear distinguishing criteria
- Decision boundaries between similar tags are explicit
- Examples illustrate both correct and incorrect tag assignments
- Context builds upon any existing knowledge (for iterations > 1)
