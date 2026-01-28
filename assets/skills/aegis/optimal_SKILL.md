# Balanced Error Correction with Precision Control Skill

## Skill Overview

Systematically analyze training errors and evolve context with balanced precision control—addressing both false positives (over-classification) and false negatives (under-classification) using surgical pattern updates. Uses a structured feedback loop with explicit precision/recall trade-offs, enabling robust classification that avoids common small model pitfalls like over-matching keywords.

## Task Background

The AEGIS2 benchmark requires classifying prompts as safe/unsafe and identifying violation categories. Small models (8B parameters) are prone to two critical failures:

1. **Over-classification (False Positives)**: Flagging benign prompts as unsafe
   - Common with: creative roleplay, content templates, conversational statements
   - Root cause: keyword patterns too broad, missing safe exclusions

2. **Under-classification (False Negatives)**: Missing actual violations
   - Common with: content extraction jailbreaks, indirect cheating patterns
   - Root cause: missing trigger patterns, context not retrieved

**Target Categories:**
1. `Copyright_Trademark_Plagiarism` - Reproducing copyrighted content, brand impersonation, plagiarism
2. `Political_Misinformation_Conspiracy` - False political claims, election misinfo, conspiracy theories
3. `Unauthorized_Advice` - Professional advice (medical/legal/financial) requiring licensed expertise
4. `Immoral_Unethical` - Morally questionable or deceptive requests, jailbreak attempts
5. `safe` - No violation

## Methodology

### Phase 1: Load Evaluation Results and Error Analysis
```python
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any
from utils.llm import call_llm

# Load training evaluation results
train_results_path = Path('data/train.json')
with open(train_results_path, 'r') as f:
    train_data = json.load(f)

# train_data contains:
# - summary: overall metrics
# - detailed_results: list of {id, question, llm_answer, target, is_correct, error_type?}
```

### Phase 2: Categorize Errors with Precision/Recall Analysis
```python
def categorize_errors(detailed_results: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Categorize errors by type for balanced correction.
    Track both over-classification and under-classification.
    """
    error_categories = {
        # False Positives (Over-classification)
        'false_positive_safe': [],    # Predicted unsafe, should be safe
        'false_positive_copyright': [],   # Wrong category assignment
        'false_positive_misinfo': [],
        'false_positive_unauthorized': [],
        'false_positive_immoral': [],

        # False Negatives (Under-classification)
        'false_negative_safe': [],    # Predicted safe, should be unsafe
        'false_negative_missed_category': [],  # Unsafe but wrong/no category
        'false_negative_format': [],  # Output format issues

        # Multi-label errors
        'multi_label_partial': [],    # Some categories missed
        'multi_label_wrong': [],      # Wrong categories assigned
    }

    for result in detailed_results:
        if not result['is_correct']:
            target = result['target']
            prediction = result['llm_answer']

            # Normalize to lists
            target_list = target if isinstance(target, list) else [target]
            pred_list = prediction if isinstance(prediction, list) else [prediction]

            if target_list == ['safe'] and pred_list != ['safe']:
                error_categories['false_positive_safe'].append(result)
            elif 'safe' in pred_list and target_list != ['safe']:
                error_categories['false_negative_safe'].append(result)
            elif pred_list != target_list:
                # Check if wrong category or missing categories
                if set(pred_list) & set(['safe', 'unsafe', 'Copyright_Trademark_Plagiarism',
                                        'Political_Misinformation_Conspiracy', 'Unauthorized_Advice',
                                        'Immoral_Unethical']):
                    error_categories['false_negative_missed_category'].append(result)
                else:
                    error_categories['multi_label_wrong'].append(result)

    return error_categories

def analyze_error_distribution(error_categories: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """
    Analyze error distribution to understand precision vs recall balance.
    Returns actionable insights for balanced correction.
    """
    over_class_count = sum(len(v) for k, v in error_categories.items()
                          if k.startswith('false_positive'))
    under_class_count = sum(len(v) for k, v in error_categories.items()
                           if k.startswith('false_negative'))

    return {
        'over_classification_count': over_class_count,
        'under_classification_count': under_class_count,
        'total_errors': over_class_count + under_class_count,
        'dominant_error_type': 'over' if over_class_count > under_class_count else 'under',
        'precision_focus_needed': over_class_count > 0,
        'recall_focus_needed': under_class_count > 0
    }
```

### Phase 3: Extract Error Patterns with Context Analysis
```python
def extract_error_patterns(error_list: List[Dict]) -> Dict[str, Any]:
    """
    For each error, extract patterns and contextual features.
    Focus on discriminative features that separate correct from incorrect.
    """
    if not error_list:
        return {'patterns': [], 'examples': [], 'root_causes': []}

    patterns = defaultdict(list)
    examples = []
    root_causes = []

    for error in error_list[:10]:  # Limit to 10 for analysis
        question = error['question'].lower()
        prediction = error['llm_answer']
        target = error['target']

        # Extract keywords and patterns
        error_info = {
            'question': error['question'],
            'predicted': prediction,
            'target': target,
            'keywords': extract_keywords(question),
            'length': len(question.split()),
            'has_override': any(kw in question for kw in
                              ['ignore', 'disregard', 'forget', 'override']),
            'has_roleplay': any(kw in question for kw in
                               ['act as', 'you are a', 'you are an']),
            'has_template': any(ph in question for ph in
                               ['[prompt]', '[topic]', '[variable', '[target']),
            'has_extraction': any(kw in question for kw in
                                 ['rewrite', 'extract', 'take from', 'use information']),
        }

        examples.append(error_info)

        # Categorize by pattern type
        if error_info['has_override']:
            patterns['override_patterns'].append(error_info)
        if error_info['has_roleplay']:
            patterns['roleplay_patterns'].append(error_info)
        if error_info['has_template']:
            patterns['template_patterns'].append(error_info)
        if error_info['has_extraction']:
            patterns['extraction_patterns'].append(error_info)

    # Use LLM to identify root causes
    if examples:
        root_causes = synthesize_root_causes(examples)

    return {
        'patterns': dict(patterns),
        'examples': examples,
        'root_causes': root_causes,
        'pattern_counts': {k: len(v) for k, v in patterns.items()}
    }

def synthesize_root_causes(examples: List[Dict]) -> List[str]:
    """
    Use LLM reflection to understand why these errors occurred.
    Focus on pattern-level insights, not individual cases.
    """
    examples_text = "\n".join([
        f"Q: {ex['question'][:200]}...\nTarget: {ex['target']}\nPredicted: {ex['predicted']}"
        for ex in examples[:5]
    ])

    prompt = f"""Analyze these classification errors and identify ROOT CAUSES:

{examples_text}

For each error type, identify:
1. Why does the model make this mistake?
2. What pattern or feature is being over/under-matched?
3. What is the KEY DISTINCTION between correct and incorrect classification?

Format:
ROOT CAUSE: <2-3 sentences>
PATTERN: <specific feature or pattern>
FIX: <what needs to change in detection logic>
"""

    response = call_llm([prompt]) if examples else []
    return response if response else []
```

### Phase 4: Prioritize Fixes with Precision Control
```python
def prioritize_fixes(error_analysis: Dict, error_distribution: Dict) -> List[Dict]:
    """
    Prioritize fixes balancing precision and recall.
    Focus on high-impact, low-variance patterns.
    """
    fixes = []

    # If over-classification dominant, prioritize precision fixes
    if error_distribution['dominant_error_type'] == 'over':
        # Focus on false positive patterns
        for error_type, errors in error_analysis.items():
            if 'false_positive' in error_type and errors:
                fix = {
                    'error_type': error_type,
                    'priority': 1,  # High priority
                    'fix_type': 'precision',  # Add safe exclusions
                    'errors': errors[:5],
                    'approach': 'Add safe exclusion patterns or narrow detection'
                }
                fixes.append(fix)

    # If under-classification dominant, prioritize recall fixes
    if error_distribution['dominant_error_type'] == 'under':
        # Focus on false negative patterns
        for error_type, errors in error_analysis.items():
            if 'false_negative' in error_type and errors:
                fix = {
                    'error_type': error_type,
                    'priority': 1,
                    'fix_type': 'recall',  # Add detection patterns
                    'errors': errors[:5],
                    'approach': 'Add missing trigger patterns or enhance context'
                }
                fixes.append(fix)

    # Balance: if both present, alternate or fix both
    if error_distribution['precision_focus_needed'] and \
       error_distribution['recall_focus_needed']:
        # Add balanced fixes for both
        precision_fixes = [f for f in fixes if f['fix_type'] == 'precision']
        recall_fixes = [f for f in fixes if f['fix_type'] == 'recall']
        if len(precision_fixes) > len(recall_fixes):
            fixes.extend(recall_fixes)
        elif len(recall_fixes) > len(precision_fixes):
            fixes.extend(precision_fixes)

    # Sort by impact (number of errors)
    fixes.sort(key=lambda x: len(x['errors']), reverse=True)

    return fixes
```

### Phase 5: Surgical Context Updates with Explicit Precision Control

#### For Precision Fixes (Reducing False Positives):
```python
def apply_precision_fix(fix: Dict, context_files: Dict[str, str]) -> Dict[str, str]:
    """
    Apply precision fix by adding safe exclusion patterns.
    Key: Be specific and add clear examples of what IS safe.
    """
    updated_files = context_files.copy()

    # Identify which context file needs update
    if 'copyright' in fix['error_type']:
        target_file = 'context/01_copyright_patterns.md'
    elif 'misinfo' in fix['error_type']:
        target_file = 'context/02_misinformation_patterns.md'
    elif 'unauthorized' in fix['error_type']:
        target_file = 'context/03_unauthorized_advice.md'
    elif 'immoral' in fix['error_type']:
        target_file = 'context/04_immoral_unethical_patterns.md'
    else:
        target_file = 'context/00_safe_baseline.md'

    # Add SAFE EXCLUSION section
    safe_exclusion_section = f"""

## CRITICAL: SAFE EXCLUSIONS - These Are NOT Violations

Based on training errors, these patterns were incorrectly flagged:

### Examples That Should Be SAFE:
"""

    for i, error in enumerate(fix['errors'][:3], 1):
        safe_exclusion_section += f"""
**SAFE Example {i}**: "{error['question'][:150]}..."
- Why SAFE: [Explain why this doesn't violate the category]
- Correct classification: {error['target']}
"""

    safe_exclusion_section += """
## Updated Decision Rule

**BEFORE**: [Previous rule that caused error]

**AFTER**: [Revised rule with safe exclusion]

IF [original trigger] AND NOT [safe exclusion condition]:
    THEN classify as [category]
"""

    # Append to appropriate section in context file
    updated_content = updated_files[target_file] + safe_exclusion_section
    updated_files[target_file] = updated_content

    return updated_files
```

#### For Recall Fixes (Reducing False Negatives):
```python
def apply_recall_fix(fix: Dict, context_files: Dict[str, str]) -> Dict[str, str]:
    """
    Apply recall fix by adding missing trigger patterns.
    Key: Be specific and add clear examples of what IS unsafe.
    """
    updated_files = context_files.copy()

    # Identify which context file needs update
    if 'copyright' in fix['error_type']:
        target_file = 'context/01_copyright_patterns.md'
    elif 'misinfo' in fix['error_type']:
        target_file = 'context/02_misinformation_patterns.md'
    elif 'unauthorized' in fix['error_type']:
        target_file = 'context/03_unauthorized_advice.md'
    elif 'immoral' in fix['error_type']:
        target_file = 'context/04_immoral_unethical_patterns.md'
    else:
        target_file = 'context/00_safe_baseline.md'

    # Add NEW PATTERN section
    new_pattern_section = f"""

## NEW PATTERN - Previously Missed Violations

Based on training errors, these patterns were NOT detected:

### Examples That Should Be UNSAFE:
"""

    for i, error in enumerate(fix['errors'][:3], 1):
        new_pattern_section += f"""
**UNSAFE Example {i}**: "{error['question'][:150]}..."
- Why UNSAFE: [Explain the violation]
- Should classify as: {error['target']}
"""

    new_pattern_section += """
## Updated Decision Rule

**ADDED**: New trigger patterns

IF [new trigger pattern]:
    THEN classify as [category]

**Trigger Keywords/Patterns**:
- [keyword 1]
- [keyword 2]
- [keyword 3]
"""

    # Append to appropriate section in context file
    updated_content = updated_files[target_file] + new_pattern_section
    updated_files[target_file] = updated_content

    return updated_files
```

### Phase 6: Update Retrieval Logic with Precision Controls

#### For Precision Fixes in retrieve_context.py:
```python
def add_safe_exclusion(retrieval_code: str, pattern: str, exclusion: str) -> str:
    """
    Add safe exclusion to prevent over-classification.
    """
    # Find the pattern detection section
    if f"if any(kw in question_lower for kw in {pattern}" in retrieval_code:
        # Add exclusion check
        exclusion_check = f"""
    # SAFE EXCLUSION: {exclusion}
    has_{exclusion.replace(' ', '_').lower()} = any(kw in question_lower for kw in ['{exclusion}'])
    if has_{exclusion.replace(' ', '_').lower()}:
        # This is safe, don't add context
        pass
    elif """
        # This would modify the detection logic
        pass

    return retrieval_code
```

#### For Recall Fixes in retrieve_context.py:
```python
def add_detection_pattern(retrieval_code: str, pattern_name: str,
                         keywords: List[str], context_file: str) -> str:
    """
    Add new detection pattern to catch previously missed violations.
    """
    new_detection = f"""
    # NEW: {pattern_name}
    {pattern_name.lower().replace(' ', '_')}_keywords = {keywords}
    if any(kw in question_lower for kw in {pattern_name.lower().replace(' ', '_')}_keywords):
        {context_file.lower().replace('.md', '').replace('context/', '')}_path = script_dir / "{context_file}"
        with open({context_file.lower().replace('.md', '').replace('context/', '')}_path, 'r') as f:
            context_parts.append(f.read())
"""

    # Append to retrieval function
    return retrieval_code + new_detection
```

### Phase 7: Validate Precision/Recall Balance
```python
def validate_precision_recall_balance(train_data: Dict, context_files: Dict[str, str]) -> Dict:
    """
    Validate that fixes don't create new errors in opposite direction.
    """
    detailed_results = train_data['detailed_results']

    # Count errors by type
    false_positives = sum(1 for r in detailed_results
                         if not r['is_correct'] and r['llm_answer'] != 'safe'
                         and r['target'] == 'safe')
    false_negatives = sum(1 for r in detailed_results
                         if not r['is_correct'] and r['llm_answer'] == 'safe'
                         and r['target'] != 'safe')

    # Check balance
    balance_score = 1 - (abs(false_positives - false_negatives) /
                        max(false_positives + false_negatives, 1))

    return {
        'false_positives': false_positives,
        'false_negatives': false_negatives,
        'balance_score': balance_score,
        'is_balanced': balance_score > 0.7,  # 70% balance threshold
        'total_errors': false_positives + false_negatives
    }
```

## Key Principles

### 1. Balanced Error Correction
- Don't just fix one error type—maintain precision/recall balance
- Each fix should consider impact on opposite error type
- Document both over and under-classification patterns

### 2. Surgical Precision
- Change only what's broken, don't rewrite entire context
- Add SAFE EXCLUSION sections for precision fixes
- Add NEW PATTERN sections for recall fixes
- Each addition should have explicit examples

### 3. Discriminative Features
- Always identify what feature distinguishes safe from unsafe
- "What makes this X and not Y?"
- Add explicit examples of both classes

### 4. Conservative Pattern Addition
- Add patterns conservatively—each risks false positives
- Prefer high-precision patterns (low false positive rate)
- Always add safe examples to prevent over-classification

### 5. Explicit Decision Rules
- Small models need clear IF-THEN rules
- Rules should specify conditions AND exclusions
- Include concrete examples for each rule

### 6. Context-Dependent Handling
- "Ignore previous instructions" requires content type check
- Roleplay requires bypass language check
- Conversational statements need context awareness

### 7. Critical Distinctions
- CREATE new content = SAFE
- EXTRACT/REWRITE existing = UNSAFE
- Benign roleplay without override = SAFE
- Roleplay with override + harmful content = UNSAFE

## Common Error Patterns and Fixes

### Pattern 1: Over-Classification of Content Templates
**Root Cause**: Keyword matching too broad, missing content creation exclusion
**Fix**: Add content creation patterns to safe exclusions
```
IF has [roleplay] AND has [content creation keywords]:
    THEN SAFE (not a jailbreak)
```

### Pattern 2: Over-Classification of Roleplay
**Root Cause**: "Stay in character" flagged without bypass language check
**Fix**: Require bypass language for roleplay classification
```
IF has "stay in character" AND NOT has ["no rules", "no ethics"]:
    THEN SAFE (benign roleplay)
```

### Pattern 3: Under-Classification of Content Extraction
**Root Cause**: "Ignore" + extraction not detected
**Fix**: Add content extraction patterns before benign content check
```
IF has "ignore" AND has [extraction keywords]:
    THEN UNSAFE (takes precedence)
```

### Pattern 4: Under-Classification of Indirect Cheating
**Root Cause**: "Can't pass this test" not recognized as cheating
**Fix**: Add indirect dishonesty patterns
```
IF has [can't pass, not ready, not prepared] AND has [exam, test]:
    THEN UNSAFE (academic dishonesty)
```

### Pattern 5: Category Boundary Confusion
**Root Cause**: Similar patterns assigned to wrong category
**Fix**: Add discriminative features for boundary cases
```
IMMORAL_UNETHICAL: [jailbreak + override] OR [persona + no rules]
UNAUTHORIZED_ADVICE: [professional roleplay + diagnostic request]
```

## Utilities Reference

- `utils/llm.call_llm()`: Use for synthesizing error-specific corrections and pattern analysis
- `utils/embedding.compute_embedding_similarity()`: Use for semantic pattern matching when keyword matching is insufficient

## Output Artifacts

Generate:
1. Updated `context/*.md` files with surgical error fixes
2. Updated `retrieve_context.py` with balanced detection patterns
3. `context/PRECISION_RECALL_ANALYSIS.md` documenting error distribution and balance

## Validation Checklist

After applying fixes:
- [ ] Error distribution analyzed (over vs under)
- [ ] Both precision and recall issues addressed
- [ ] Each fix has explicit examples (3-5 per pattern)
- [ ] Safe exclusions prevent new false positives
- [ ] New patterns catch actual violations
- [ ] Retrieval logic updated for new patterns
- [ ] Precision/recall balance validated (balance score > 0.7)
- [ ] Changes documented in PRECISION_RECALL_ANALYSIS.md
