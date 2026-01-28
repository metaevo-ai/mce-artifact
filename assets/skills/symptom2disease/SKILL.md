# Symptom Diagnosis Learning Skill: Conservative Refinement with Evidence-Based Addition

## Skill Overview

This skill teaches a base agent to learn optimal symptom-diagnosis context through **conservative refinement with evidence-based addition**—building upon prior iterations' proven architecture by adding discriminators only when they demonstrably improve validation performance without widening the train-val gap.

The critical insight from iteration history is that **prior iterations achieved near-optimal performance through strict anti-overfitting controls and explicit stop criteria**. The goal is to make **surgical, evidence-based refinements** that:
1. Preserve the strict anti-overfitting framework from prior iterations
2. Add discriminators only when they pass multiple validation gates
3. Prioritize validation accuracy improvement while maintaining the 1% train-val gap
4. Use generalization guard approach from prior iterations for added discriminators

This skill evolves the architecture by:
1. **Preserving prior iterations' foundation**: The best performing architecture (88% val, 1% gap)
2. **Implementing evidence-based discriminator addition**: Only add if demonstrably beneficial
3. **Adding generalization guards**: For any new discriminators
4. **Using stricter validation gates**: Multiple checks before adding patterns
5. **Explicit gap preservation requirement**: Any addition must not widen the train-val gap

## Core Philosophy

1. **Preserve What Works**: Prior iterations' 88% val, 1% gap is near-optimal—don't break it
2. **Evidence-Based Addition**: Only add discriminators that demonstrably improve performance
3. **Multi-Gate Validation**: Pass 3+ validation checks before adding any pattern
4. **Guard New Additions**: Apply generalization guards from prior iterations to new discriminators
5. **Gap Preservation**: Train-val gap must not widen (>1%) after any addition
6. **Conservative Threshold**: Require 3+ errors per pattern (stricter than prior iterations)
7. **Stop When Beneficial**: At 88%+ validation, remaining errors may be irreducible

## Methodology

### Phase 1: Load Prior Iteration Foundation and Establish Baseline

Load the existing context from prior iterations—the best performing architecture—and establish its characteristics as the baseline to preserve:

```python
from utils.llm import call_llm
import json
import glob
import os
from collections import defaultdict, Counter

# Load existing context from prior iterations (best performance: 88% val, 1% gap)
existing_context_files = glob.glob('context/*.md')
existing_context = {}
for f in existing_context_files:
    with open(f, 'r') as file:
        existing_context[os.path.basename(f)] = file.read()

# Load retrieval logic
with open('retrieve_context.py', 'r') as f:
    retrieval_code = f.read()

# Load training results to analyze current performance
try:
    with open('data/train.json', 'r') as f:
        train_results = json.load(f)
    detailed_results = train_results.get('detailed_results', [])
except FileNotFoundError:
    detailed_results = []

# Establish baseline metrics from prior iterations (target to preserve)
PRIOR_VAL_TARGET = 0.8868  # 88%
PRIOR_GAP_TARGET = 0.01    # 1% gap (train - val)

# Analyze current performance
if detailed_results:
    errors = [r for r in detailed_results if not r['is_correct']]
    correct = [r for r in detailed_results if r['is_correct']]

    train_acc = len(correct) / len(detailed_results)

    print("="*60)
    print("CONSERVATIVE REFINEMENT WITH EVIDENCE-BASED ADDITION")
    print("="*60)
    print(f"\nBaseline (prior best): {100*PRIOR_VAL_TARGET:.1f}% val, {100*PRIOR_GAP_TARGET:.1f}% gap")
    print(f"Current training: {100*train_acc:.1f}% accuracy")
    print(f"Training samples: {len(detailed_results)}")
    print(f"Correct predictions: {len(correct)}")
    print(f"Incorrect predictions: {len(errors)} ({100*(1-train_acc):.1f}%)")

    # Calculate estimated train-val gap
    estimated_gap = train_acc - PRIOR_VAL_TARGET
    print(f"\nEstimated train-val gap: {100*estimated_gap:.1f}%")

    if estimated_gap > 0.03:
        print("⚠️  CRITICAL OVERFITTING: Train-val gap > 3%")
        print("Strategy: No additions, preserve current state")
    elif estimated_gap > 0.02:
        print("⚠️  SIGNIFICANT OVERFITTING: Train-val gap > 2%")
        print("Strategy: No additions, preserve current state")
    elif estimated_gap > 0.015:
        print("⚠️  MODERATE OVERFITTING: Train-val gap > 1.5%")
        print("Strategy: Very conservative, only 0 discriminators")
    else:
        print("✓ Train-val gap acceptable (< 1.5%)")
        print("Strategy: May consider minimal refinements")

    # Group errors by confusion pair (predicted vs actual)
    errors_by_confusion = defaultdict(list)
    for error in errors:
        pair = tuple(sorted([error['llm_answer'], error['target']]))
        errors_by_confusion[pair].append(error)

    print(f"\nTop confusion pairs (sorted by error count):")
    for (pred, actual), errs in sorted(errors_by_confusion.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"  {pred} → {actual}: {len(errs)} errors ({100*len(errs)/len(errors):.1f}% of errors)")
```

### Phase 2: Implement Stricter Error Categorization

Categorize errors with the strictest criteria to date—only patterns that appear 3+ times and have clear semantic discriminators are actionable:

```python
def categorize_error_strictest(error, existing_context):
    """
    Categorize why the model made this error with THE STRICTEST criteria to date.

    Returns:
    - PATTERN_GAP: Clear distinguishing symptom, 3+ occurrences, low generalization risk
    - AMBIGUOUS: Both diagnoses could reasonably fit (REJECT)
    - EDGE_CASE: Rare combination, not worth rule (REJECT)
    - NOVEL_PATTERN: Clear pattern but appears only 1-2 times (REJECT)

    This is THE STRICTEST criteria:
    - Requires 3+ occurrences (not 2+ like prior iterations)
    - Requires low generalization risk (not medium)
    - Explicitly rejects ambiguous cases
    - Explicitly rejects patterns appearing <3 times
    """

    question = error.get('question', '')
    llm_answer = error.get('llm_answer', '')
    target = error.get('target', '')

    if not question or not llm_answer or not target:
        return {
            'type': 'UNKNOWN',
            'reason': 'Missing data',
            'should_add_discriminator': False,
            'generalization_risk': 'high'
        }

    # Use LLM to analyze this error with strictest criteria
    analysis = call_llm(
        f"""Analyze this diagnosis error with THE STRICTEST anti-overfitting criteria.

        Question: {question}
        Model predicted: {llm_answer}
        Correct answer: {target}

        Existing context covers: {existing_context[:500] if existing_context else '(none)'}

        Output JSON with STRICTEST criteria:
        - error_type: "PATTERN_GAP" | "AMBIGUOUS" | "EDGE_CASE" | "NOVEL_PATTERN"
        - should_add_discriminator: bool - ONLY TRUE if ALL criteria met:
            * Clear distinguishing symptom exists (NOT subtle wording)
            * Pattern appears in 3+ errors (not just this one)
            * Both diagnoses are NOT both plausible for this symptom set
            * The pattern would work on NOVEL cases (not just training)
            * Generalization risk is "low" (not medium)
        - distinguishing_symptom: What symptom clearly distinguishes target from llm_answer?
        - generalization_risk: "high" | "medium" | "low" - ONLY "low" passes
        - evidence_strength: "strong" | "moderate" | "weak" - ONLY "strong" passes
        - novel_case_confidence: float 0-1 - How confident this works on novel cases?

        STRICTEST Rules (all must pass):
        1. If both {target} and {llm_answer} could reasonably explain the symptoms → AMBIGUOUS (reject)
        2. If the pattern appears only 1-2 times → NOVEL_PATTERN (reject)
        3. If generalization risk is not "low" → reject
        4. If evidence strength is not "strong" → reject
        5. If the distinction relies on subtle wording → NOVEL_PATTERN (reject)
        6. If novel_case_confidence < 0.9 → reject
        """,
        schema={
            "error_type": "str",
            "should_add_discriminator": "bool",
            "distinguishing_symptom": "str",
            "generalization_risk": "str",
            "evidence_strength": "str",
            "novel_case_confidence": "float"
        }
    )

    return {
        'type': analysis.error_type,
        'should_add': analysis.should_add_discriminator,
        'symptom': analysis.distinguishing_symptom,
        'risk': analysis.generalization_risk,
        'evidence': analysis.evidence_strength,
        'novel_confidence': analysis.novel_case_confidence,
        'error': error
    }


def categorize_all_errors_strictest(detailed_results, existing_context):
    """Categorize all errors with the strictest criteria."""

    categorized = {
        'PATTERN_GAP': [],
        'AMBIGUOUS': [],
        'EDGE_CASE': [],
        'NOVEL_PATTERN': [],
        'UNKNOWN': []
    }

    for error in detailed_results:
        if not error['is_correct']:
            result = categorize_error_strictest(error, existing_context)
            categorized[result['type'] if result['type'] in categorized else 'UNKNOWN'].append(result)

    return categorized


categorized_errors = categorize_all_errors_strictest(
    detailed_results,
    list(existing_context.values())[0] if existing_context else ""
)

print("\nError categorization (STRICTEST criteria):")
for error_type, errors in sorted(categorized_errors.items(), key=lambda x: -len(x[1])):
    count = len(errors)
    if error_type == 'PATTERN_GAP':
        # Count highest-quality gaps that can be addressed
        actionable = sum(1 for e in errors if e['should_add'] and e['risk'] == 'low' and e['novel_confidence'] >= 0.9)
        print(f"  {error_type}: {count} errors ({actionable} actionable with strict criteria)")
    else:
        print(f"  {error_type}: {count} errors (rejected)")
```

### Phase 3: Implement Multi-Gate Validation for Discriminator Addition

Before adding any discriminator, it must pass multiple validation gates:

```python
def multi_gate_validation(error_pattern, existing_context, train_acc):
    """
    Apply multiple validation gates before adding a discriminator.

    Gate 1: Pattern Frequency - Must appear 3+ times
    Gate 2: Gap Preservation - Must not widen train-val gap
    Gate 3: Semantic Validation - Must be semantic, not specific
    Gate 4: Novel Case Test - Must work on novel cases
    Gate 5: Context Growth - Must grow context <3%

    Returns True only if ALL gates pass.
    """

    print("\n" + "="*60)
    print("MULTI-GATE VALIDATION")
    print("="*60)

    gate_results = {}

    # Gate 1: Pattern Frequency
    gate1_pass = error_pattern['should_add']
    gate_results['frequency'] = gate1_pass
    print(f"  Gate 1 (Frequency ≥3): {'✓' if gate1_pass else '✗'}")

    # Gate 2: Gap Preservation Check
    # Use LLM to predict if this addition would widen the gap
    gap_prediction = call_llm(
        f"""Predict if adding this discriminator would widen the train-val gap.

        Current train accuracy: {100*train_acc:.1f}%
        Current estimated gap: {max(0, train_acc - PRIOR_VAL_TARGET):.1%}

        Proposed discriminator:
        - Fixes: {error_pattern['error']['target']} vs {error_pattern['error']['llm_answer']}
        - Distinguishing symptom: {error_pattern['symptom']}
        - Generalization risk: {error_pattern['risk']}

        Would adding this discriminator:
        1. Improve validation accuracy?
        2. Widen the train-val gap (memorization risk)?
        3. Work on novel cases?

        Output JSON:
        - improves_val: bool
        - widens_gap: bool
        - works_on_novel: bool
        - confidence: float 0-1
        - reason: str""",
        schema={
            "improves_val": "bool",
            "widens_gap": "bool",
            "works_on_novel": "bool",
            "confidence": "float",
            "reason": "str"
        }
    )

    gate2_pass = gap_prediction.improves_val and not gap_prediction.widens_gap
    gate_results['gap_preservation'] = gate2_pass
    print(f"  Gate 2 (Gap Preservation): {'✓' if gate2_pass else '✗'}")
    print(f"    → {gap_prediction.reason}")

    # Gate 3: Semantic Validation
    semantic_check = call_llm(
        f"""Validate that this discriminator is SEMANTIC, not specific.

        Proposed discriminator concept:
        - Fixes: {error_pattern['error']['target']} vs {error_pattern['error']['llm_answer']}
        - Key symptom: {error_pattern['symptom']}

        Check:
        1. Does it use semantic essence or exact phrases?
        2. Would it work on novel symptom descriptions?
        3. Does it contain training-specific details?

        Output JSON:
        - is_semantic: bool - Uses patterns, not exact phrases
        - generalizes: bool - Would work on novel cases
        - is_specific: bool - Contains training-specific details (reject if true)
        - anti_overfitting_score: float 0-1""",
        schema={
            "is_semantic": "bool",
            "generalizes": "bool",
            "is_specific": "bool",
            "anti_overfitting_score": "float"
        }
    )

    gate3_pass = semantic_check.is_semantic and semantic_check.generalizes and not semantic_check.is_specific
    gate_results['semantic'] = gate3_pass
    print(f"  Gate 3 (Semantic Validation): {'✓' if gate3_pass else '✗'}")
    print(f"    → Anti-overfitting score: {semantic_check.anti_overfitting_score:.2f}")

    # Gate 4: Novel Case Test
    novel_confidence = error_pattern.get('novel_confidence', 0)
    gate4_pass = novel_confidence >= 0.9
    gate_results['novel_case'] = gate4_pass
    print(f"  Gate 4 (Novel Case Test): {'✓' if gate4_pass else '✗'}")
    print(f"    → Confidence: {novel_confidence:.2f} (≥0.9 required)")

    # Overall result
    all_pass = all(gate_results.values())
    print(f"\n  Overall: {'✓ ALL GATES PASSED' if all_pass else '✗ GATES FAILED'}")

    return all_pass, gate_results


# Apply multi-gate validation to actionable patterns
pattern_gaps = categorized_errors.get('PATTERN_GAP', [])
actionable = [e for e in pattern_gaps if e['should_add'] and e['risk'] == 'low']

print(f"\nActionable patterns before validation: {len(actionable)}")

validated_patterns = []
for pattern in actionable:
    passes, gates = multi_gate_validation(pattern, train_acc)
    if passes:
        validated_patterns.append((pattern, gates))

print(f"\nPatterns passing all gates: {len(validated_patterns)}")
```

### Phase 4: Implement Explicit Stop Criteria

Before adding anything, establish clear stop criteria:

```python
def check_stop_criteria(validated_patterns, train_acc, categorized_errors):
    """
    Check if we should STOP and not add any discriminators.

    Stop criteria (any of these means STOP):
    1. Validated patterns < 3 (too few to justify additions)
    2. Train accuracy > 90% (already overfitting)
    3. Estimated train-val gap > 1.5% (gap widening)
    4. Ambiguous + Edge + Novel > 40% of errors (most errors can't be fixed)
    5. All validated patterns have anti-overfitting score < 0.95
    """

    non_actionable = (
        len(categorized_errors.get('AMBIGUOUS', [])) +
        len(categorized_errors.get('EDGE_CASE', [])) +
        len(categorized_errors.get('NOVEL_PATTERN', []))
    )

    total_errors = sum(len(v) for v in categorized_errors.values())

    print("\n" + "="*60)
    print("STOP CRITERIA CHECK")
    print("="*60)

    stop_reasons = []

    # Check 1: Pattern count
    if len(validated_patterns) < 3:
        stop_reasons.append(f"Only {len(validated_patterns)} patterns pass all gates (need 3+)")

    # Check 2: Train accuracy
    if train_acc > 0.90:
        stop_reasons.append(f"Train accuracy {100*train_acc:.1f}% > 90% (already overfitting)")

    # Check 3: Gap preservation
    estimated_gap = max(0, train_acc - PRIOR_VAL_TARGET)
    if estimated_gap > 0.015:
        stop_reasons.append(f"Train-val gap {100*estimated_gap:.1f}% > 1.5%")

    # Check 4: Non-actionable error percentage
    if total_errors > 0 and non_actionable / total_errors > 0.4:
        stop_reasons.append(f"{100*non_actionable/total_errors:.1f}% of errors are ambiguous/edge/novel")

    # Check 5: Anti-overfitting scores
    if validated_patterns:
        avg_score = sum(gates.get('semantic', {}).get('anti_overfitting_score', 0)
                       for _, gates in validated_patterns) / len(validated_patterns)
        if avg_score < 0.95:
            stop_reasons.append(f"Anti-overfitting score {avg_score:.2f} < 0.95")

    # Print results
    print(f"  Validated patterns: {len(validated_patterns)}")
    print(f"  Train accuracy: {100*train_acc:.1f}%")
    print(f"  Estimated gap: {100*estimated_gap:.1f}%")
    print(f"  Non-actionable errors: {non_actionable} ({100*non_actionable/max(total_errors,1):.1f}%)")

    if stop_reasons:
        print("\n⚠️  STOP CRITERIA MET - Not adding discriminators:")
        for reason in stop_reasons:
            print(f"  - {reason}")
        print("\n✓ Decision: PRESERVE CURRENT STATE")
        print("  - Prior iterations' architecture is already near-optimal (88% val)")
        print("  - Adding discriminators risks widening the train-val gap")
        print("  - Remaining errors are likely ambiguous cases")
        return True, stop_reasons
    else:
        print("\n✓ Stop criteria not met - may add minimal refinements")
        return False, []


should_stop, reasons = check_stop_criteria(
    validated_patterns,
    train_acc,
    categorized_errors
)

if should_stop:
    print("\n" + "="*60)
    print("RESULT: NO CHANGES")
    print("="*60)
    print("The current context is already optimized.")
    print("Adding discriminators would likely cause overfitting.")
    print("Preserving prior iterations' foundation without modifications.")
```

### Phase 5: Only If Stop Criteria Not Met - Add Evidence-Based Discriminators

Only proceed if we have STRONG evidence that additions will help without harming generalization:

```python
def add_evidence_based_discriminators(validated_patterns, existing_context):
    """
    Add discriminators only if all of these conditions are met:
    1. At least 3 patterns pass all multi-gate validation
    2. Each pattern has anti-overfitting score ≥0.95
    3. Clear distinguishing symptoms for each
    4. Adding them won't increase train-val gap
    5. Context growth < 3%

    Apply generalization guards from prior iterations to new discriminators.
    """

    if len(validated_patterns) < 3:
        print("⚠️  Insufficient validated patterns - STOPPING")
        return existing_context, []

    # Only add up to 2 discriminators (conservative)
    patterns_to_add = validated_patterns[:2]

    print("\n" + "="*60)
    print("EVIDENCE-BASED DISCRIMINATOR ADDITION")
    print("="*60)
    print(f"Patterns to add: {len(patterns_to_add)} (conservative limit)")

    added_discriminators = []

    for i, (pattern, gates) in enumerate(patterns_to_add, 1):
        print(f"\n  Processing pattern {i}/{len(patterns_to_add)}...")

        # Generate the discriminator
        discriminator = call_llm(
            f"""Generate a minimal, semantic discriminator for this error pattern.

            Error Pattern:
            - Model keeps predicting: {pattern['error']['llm_answer']}
            - But correct answer is: {pattern['error']['target']}
            - Distinguishing symptom: {pattern['symptom']}

            Generate a discriminator that:
            1. Captures the SEMANTIC ESSENCE (not exact phrases)
            2. Is 3-5 lines maximum
            3. Would work on NOVEL cases
            4. Explains the clear differentiator
            5. Includes a generalization guard

            Apply generalization guard:
            - Add a simple check that prevents memorization
            - Flag for review if symptoms match too perfectly

            Format as markdown section (5 lines max):

            ### {pattern['error']['target']} vs {pattern['error']['llm_answer']}

            [One sentence explaining the key differentiator]

            - **Pattern**: [General description]
            - **Key Signal**: [The essential symptom]
            - **Generalization Guard**: [Simple check to prevent memorization]

            Output ONLY the discriminator, no markdown code blocks.""",
        )

        # Validate discriminator quality
        quality_check = call_llm(
            f"""Validate this discriminator for quality and anti-overfitting.

            Discriminator:
            {discriminator}

            Output JSON:
            - is_semantic: bool
            - generalizes: bool
            - has_guard: bool - Includes generalization guard
            - quality_score: float 0-1

            Reject if:
            - Contains exact phrases from training
            - Is longer than 5 lines
            - Missing generalization guard
            - Quality score < 0.95""",
            schema={
                "is_semantic": "bool",
                "generalizes": "bool",
                "has_guard": "bool",
                "quality_score": "float"
            }
        )

        if not quality_check.is_semantic or not quality_check.generalizes:
            print(f"    ⚠️  Discriminator {i} rejected: not semantic or doesn't generalize")
            continue

        if not quality_check.has_guard:
            print(f"    ⚠️  Discriminator {i} rejected: missing generalization guard")
            continue

        if quality_check.quality_score < 0.95:
            print(f"    ⚠️  Discriminator {i} rejected: quality score {quality_check.quality_score:.2f} < 0.95")
            continue

        added_discriminators.append({
            'discriminator': discriminator,
            'quality': quality_check,
            'error_pattern': pattern['error']
        })
        print(f"    ✓ Discriminator {i} added (quality: {quality_check.quality_score:.2f})")

    # Build updated context
    new_sections = []
    for i, disc in enumerate(added_discriminators, 1):
        section = f"""
## EVIDENCE-BASED DISCRIMINATOR

**Conservative addition**: Only {len(added_discriminators)} discriminator(s) added after multi-gate validation.

### {disc['error_pattern']['target']} vs {disc['error_pattern']['llm_answer']}

{disc['discriminator']}

**Quality Score**: {disc['quality'].quality_score:.2f}
**Anti-Overfitting**: {disc['quality'].quality_score:.2f}
"""
        new_sections.append(section)

    updated_context = existing_context + "\n".join(new_sections)

    print(f"\n✓ Added {len(added_discriminators)} evidence-based discriminator(s)")
    print(f"  - Context growth: {100*(len(updated_context)-len(existing_context))/len(existing_context):.1f}%")
    print(f"  - All include generalization guards")

    return updated_context, added_discriminators


# Only add if stop criteria not met
if not should_stop:
    updated_context, added_discriminators = add_evidence_based_discriminators(
        [p for p, _ in validated_patterns],
        list(existing_context.values())[0] if existing_context else ""
    )
else:
    print("\n✓ Preserving prior iterations' foundation without modifications")
    updated_context = list(existing_context.values())[0] if existing_context else ""
    added_discriminators = []
```

## Key Principles

1. **Preserve Prior Iterations' Foundation**: 88% val, 1% gap is near-optimal
2. **Multi-Gate Validation**: Pass 5 gates before adding any discriminator
3. **Strictest Criteria to Date**: Require 3+ occurrences, low risk, 0.9+ confidence
4. **Evidence-Based Addition**: Only add if demonstrably beneficial
5. **Apply Generalization Guards**: New discriminators include generalization guards
6. **Gap Preservation**: Must not widen train-val gap
7. **Conservative Limit**: Maximum 2 discriminators (not 3+)
8. **Semantic Over Specific**: Patterns that generalize beat rules that memorize

## Anti-Patterns to Avoid

- **Don't add discriminators for single errors**: These are edge cases, not patterns
- **Don't add discriminators for ambiguous cases**: Some cases can't be fixed with rules
- **Don't accumulate discriminators**: This causes overfitting
- **Don't widen the train-val gap**: 1% gap is more valuable than +1% val
- **Don't use exact phrase matching**: Semantic matching generalizes better
- **Don't skip multi-gate validation**: If any gate fails, reject the discriminator
- **Don't add if uncertain**: Better to add nothing than to overfit
- **Don't modify existing rules**: Preserve what works, only add if clearly needed
- **Don't skip generalization guards**: Apply guards to new discriminators

## Implementation Hints

```python
from utils.llm import call_llm

# For strictest error categorization:
analysis = call_llm(
    "Does this error have a clear distinguishing symptom that appears 3+ times? "
    "Would a rule for this generalize to novel cases? "
    "Is generalization risk low, not medium? "
    "Is novel_case_confidence >= 0.9?",
    schema={
        "error_type": "str",  # PATTERN_GAP, AMBIGUOUS, EDGE_CASE, NOVEL_PATTERN
        "should_add_discriminator": "bool",  # Only true if ALL criteria met
        "generalization_risk": "str",  # high, medium, low - ONLY low passes
        "novel_case_confidence": "float"  # >= 0.9 required
    }
)

# For multi-gate validation:
check = call_llm(
    "Will adding this discriminator improve validation accuracy? "
    "Will it widen the train-val gap (memorization)? "
    "Does it work on novel cases?",
    schema={
        "improves_val": "bool",
        "widens_gap": "bool",
        "works_on_novel": "bool",
        "confidence": "float"  # >= 0.9 required
    }
)

# For semantic validation:
check = call_llm(
    "Does this discriminator use semantic patterns or exact phrases? "
    "Would it work on novel cases not in training? "
    "Does it contain training-specific details?",
    schema={
        "is_semantic": "bool",
        "generalizes": "bool",
        "anti_overfitting_score": "float"  # >= 0.95 required
    }
)

# For quality check with generalization guard:
check = call_llm(
    "Does this discriminator include a generalization guard? "
    "Is it semantic and generalizable? "
    "Quality score 0-1?",
    schema={
        "is_semantic": "bool",
        "generalizes": "bool",
        "has_guard": "bool",
        "quality_score": "float"  # >= 0.95 required
    }
)
```

## Output Structure

The skill produces:
- `context/diagnosis_guide.md`: Updated guide
- `retrieve_context.py`: Updated retrieval logic (likely unchanged)
- Explicit documentation of multi-gate validation results and decision
