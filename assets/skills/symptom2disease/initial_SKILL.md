## Skill Overview

This skill teaches a base agent to learn optimal symptom-diagnosis context from training data through a three-phase approach: **Pattern Extraction**, **Profile Synthesis**, and **Error-Driven Refinement**. The key insight is that medical diagnoses are characterized by specific symptom *combinations* and *patterns* rather than isolated symptoms. The skill guides the agent to build generalized symptom profiles that capture essential diagnostic criteria without memorizing specific training examples.

## Methodology

### Phase 1: Load and Analyze Training Data

1. **Load prior context**: Read any existing context files from the `context/` directory to understand what's already captured
2. **Load training results**: If `data/train.json` exists, load it to understand which predictions were correct/incorrect
3. **Load training data**: Parse `meta_agent/train.jsonl` - each line contains a `question` (symptom description) and `answer` (diagnosis)

```python
from utils.llm import call_llm
import json

# Load training data
with open('meta_agent/train.jsonl', 'r') as f:
    training_samples = [json.loads(line) for line in f]

# Load prior context (if exists)
try:
    existing_context_files = glob.glob('context/*.md')
    existing_context = {f: read_file(f) for f in existing_context_files}
except FileNotFoundError:
    existing_context = {}
```

### Phase 2: Extract Symptom-Diagnosis Patterns

For each diagnosis, extract the core symptom patterns that characterize it. **Focus on generalizable patterns, not specific examples.**

```python
from utils.llm import call_llm
from collections import defaultdict

# Group samples by diagnosis
diagnosis_samples = defaultdict(list)
for sample in training_samples:
    diagnosis_samples[sample['answer']].append(sample['question'])

# For each diagnosis, extract the core symptom pattern
diagnosis_profiles = {}
for diagnosis, samples in diagnosis_samples.items():
    # Synthesize a generalized symptom profile for this diagnosis
    profile = call_llm(
        f"""Analyze these {len(samples)} symptom descriptions for '{diagnosis}' and extract the CORE symptom PATTERN that defines this diagnosis.

        Symptom descriptions:
        {chr(10).join(f'- {s}' for s in samples[:15])}  # Use first 15 to avoid context overflow

        Output a concise symptom profile that captures the ESSENTIAL diagnostic criteria.
        Focus on: What symptom combinations are characteristic? What descriptors are most common?
        Do NOT list specific examples - extract the general pattern.

        Format:
        **Core Symptoms**: [list main symptoms]
        **Typical Descriptors**: [list common ways symptoms are described]
        **Key Pattern**: [2-3 sentence description of the defining symptom combination]""",
        schema={
            "core_symptoms": "list[str]",
            "typical_descriptors": "list[str]",
            "key_pattern": "str"
        }
    )
    diagnosis_profiles[diagnosis] = profile
```

### Phase 3: Synthesize Comprehensive Diagnosis Guide

Create a structured guide organizing all diagnoses with their symptom profiles. This becomes the primary context for prediction.

```python
# Synthesize comprehensive diagnosis guide
diagnosis_guide = "## Medical Diagnosis Symptom Guide\n\n"
for diagnosis, profile in sorted(diagnosis_profiles.items()):
    diagnosis_guide += f"### {diagnosis.title()}\n"
    diagnosis_guide += f"**Core Symptoms**: {', '.join(profile.core_symptoms)}\n"
    diagnosis_guide += f"**Typical Descriptors**: {', '.join(profile.typical_descriptors)}\n"
    diagnosis_guide += f"**Key Pattern**: {profile.key_pattern}\n\n"

# Save to context
write_to_file('context/diagnosis_guide.md', diagnosis_guide)
```

### Phase 4: Error-Driven Refinement (if training results exist)

If `data/train.json` exists (contains prediction results), use errors to refine the context:

```python
from utils.llm import call_llm

try:
    with open('data/train.json', 'r') as f:
        train_results = json.load(f)
    detailed_results = train_results.get('detailed_results', [])
except FileNotFoundError:
    detailed_results = []

# Analyze incorrect predictions
incorrect = [r for r in detailed_results if not r['is_correct']]
if incorrect:
    # Group errors by diagnosis type
    error_reflection = call_llm(
        f"""Analyze these {len(incorrect)} incorrect predictions to identify systematic issues.

        For each error, we predicted: {{predicted}} but correct was: {{target}}

        {chr(10).join(f'Error {i+1}: Predicted \"{e.get("llm_answer", "N/A")}\" but correct is \"{e["target"]}\". Question: {e["question"][:200]}...' for i, e in enumerate(incorrect[:10]))}

        Identify:
        1. Which diagnoses are commonly confused with each other?
        2. What symptom patterns led to wrong predictions?
        3. What additional context would help disambiguate similar diagnoses?
        4. What specific symptom keywords are being missed or misinterpreted?

        Output a prioritized list of refinements to add to the diagnosis guide.""",
        schema={
            "confused_pairs": "list[dict[str, str]]",
            "missed_patterns": "list[str]",
            "recommended_additions": "list[str]",
            "disambiguation_notes": "list[str]"
        }
    )

    # Add disambiguation section to context
    disambiguation = "## Differential Diagnosis Notes\n\n"
    disambiguation += "### Commonly Confused Conditions\n"
    for pair in error_reflection.confused_pairs:
        disambiguation += f"- {pair['diagnosis1']} vs {pair['diagnosis2']}: {pair['distinguishing_features']}\n"

    disambiguation += "\n### Key Disambiguation Points\n"
    for note in error_reflection.disambiguation_notes:
        disambiguation += f"- {note}\n"

    append_to_file('context/diagnosis_guide.md', disambiguation)
```

### Phase 5: Create Retrieval Logic

Write a retrieval script that uses the context for prediction:

```python
# Write to retrieve_context.py
retrieval_code = '''import json
from utils.llm import call_llm
from utils.embedding import compute_embedding_similarity

def retrieve_context(question: str) -> str:
    """Retrieve relevant diagnosis context for a symptom question."""
    # Read the diagnosis guide
    with open('context/diagnosis_guide.md', 'r') as f:
        guide = f.read()

    # Use LLM to identify most relevant diagnoses based on symptoms
    relevant = call_llm(
        f"""Given this symptom question: "{question}"

        Which diagnoses from this guide are most likely?
        Guide: {guide[:2000]}...

        Return the top 2-3 most relevant diagnoses with their symptom profiles.""",
        schema={
            "relevant_diagnoses": "list[str]",
            "reasoning": "str"
        }
    )

    # Return context for those diagnoses
    context = []
    for diag in relevant.relevant_diagnoses:
        # Extract the section for this diagnosis from the guide
        section = extract_section(guide, diag)
        if section:
            context.append(section)

    return "\\n\\n".join(context)
'''

with open('retrieve_context.py', 'w') as f:
    f.write(retrieval_code)
```

## Key Principles

1. **Pattern over Memorization**: Extract general symptom combinations, not specific examples
2. **Balance Coverage**: Ensure all 22 diagnoses are represented, not just common ones
3. **Disambiguation Focus**: Pay special attention to diagnoses with similar symptoms
4. **Incremental Refinement**: Build on existing context rather than starting fresh
5. **Use Utilities**: Leverage `call_llm` for structured synthesis and `compute_embedding_similarity` if needed for fuzzy matching

## Output Structure

The skill produces:
- `context/diagnosis_guide.md`: Main context with symptom profiles for all diagnoses
- `retrieve_context.py`: Retrieval logic to extract relevant context for new questions
- Optional: Updated context based on error analysis

## Anti-Patterns to Avoid

- **Don't memorize specific training examples** - extract general patterns
- **Don't create diagnosis profiles from a single sample** - use multiple samples
- **Don't ignore rare diagnoses** - all 22 diagnoses should have profiles
- **Don't skip the disambiguation step** - similar symptoms cause most errors
