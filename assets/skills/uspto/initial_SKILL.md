## Skill Overview

This skill guides the base agent to curate comprehensive retrosynthesis context by analyzing training examples, extracting reaction-type-specific patterns, and building a knowledge base that captures organic chemistry principles for single-step reaction prediction.

## Methodology

### Phase 1: Load and Analyze Training Data

1. **Load training results**: Read `data/train.json` which contains evaluation results with:
   - `summary`: Overall metrics and statistics
   - `detailed_results`: Array of samples with `id`, `question`, `llm_answer`, `target`, `is_correct`

2. **Load training data**: Read `meta_agent/train.jsonl` to understand the full dataset structure:
   - Question format: `Context: The reaction type is <TYPE>.\nInput: <PRODUCT_SMILES>\nAnswer: `
   - Target format: `<REACTANT1>.<REACTANT2>...` (period-separated SMILES strings)

### Phase 2: Reaction Type Analysis

1. **Extract all reaction types** from training data:
   - Protections
   - Deprotections
   - Oxidations
   - Reductions
   - Acylation and related processes
   - C-C bond formation
   - Heteroatom alkylation and arylation
   - Heterocycle formation
   - Functional group interconversion (FGI)
   - Functional group addition (FGA)

2. **For each reaction type**, analyze patterns:

   **Protections**:
   - Identify protecting groups (Boc, Cbz, Fmoc, Bn, etc.)
   - Common reagents: `CC(C)(C)OC(=O)OC(=O)OC(C)(C)C` (Boc2O), benzyl halides, silyl chlorides
   - Pattern: Product contains protected functional group; reactants include protecting reagent + substrate

   **Deprotections**:
   - Reverse of protections
   - Common reagents: H2/Pd (hydrogenolysis), TFA (acidic deprotection), fluoride sources
   - Pattern: Product has deprotected group; reactants include protected substrate + deprotecting agent

   **Oxidations**:
   - Common transformations: alcohol → aldehyde/ketone, sulfide → sulfoxide/sulfone, primary alcohol → aldehyde
   - Reagents: PCC, Dess-Martin, Swern, m-CPBA, TEMPO-based oxidants
   - Pattern: Product has oxidized functional group; reactants include oxidant + substrate

   **Reductions**:
   - Common transformations: nitro → amine, alkene/alkyne → alkane, ketone → alcohol
   - Reagents: H2/Pd, NaBH4, LiAlH4, catalytic hydrogenation
   - Pattern: Product has reduced functional group; reactants include reductant + substrate

   **Acylation**:
   - Formation of amide, ester, anhydride bonds
   - Reagents: acyl chlorides, anhydrides, carboxylic acids with coupling agents
   - Pattern: Product contains new carbonyl-oxygen/nitrogen bond; reactants include acyl donor + nucleophile

   **C-C Bond Formation**:
   - Suzuki, Stille, Negishi, Heck, aldol, Grignard reactions
   - Coupling partners: organoboron, organotin, organozinc, aryl halides
   - Pattern: Product has new carbon-carbon bond; reactants are coupling partners

   **Heteroatom Alkylation/Arylation**:
   - Buchwald-Hartwig, Ullmann, Williamson ether synthesis
   - Pattern: New C-N, C-O, C-S bond formed; reactants include nucleophile + electrophile

   **Heterocycle Formation**:
   - Cycloadditions, cyclizations, condensation reactions
   - Pattern: Product contains newly formed ring system; reactants cyclize together

### Phase 3: Extract Chemical Patterns via LLM Reflection

For samples with incorrect predictions, use structured LLM reflection:

```python
from utils.llm import call_llm

def reflect_on_error(question, llm_answer, target):
    """Analyze why prediction failed and what chemistry knowledge was missing."""
    reaction_type = extract_reaction_type(question)
    product_smiles = extract_product_smiles(question)

    reflection_prompt = f"""
    Analysis Task for Retrosynthesis Prediction:

    Question (Product): {question}
    Model Prediction: {llm_answer}
    Correct Answer: {target}

    Reaction Type: {reaction_type}

    Please analyze:
    1. What transformation is happening (product → reactants)?
    2. What specific chemical knowledge or reaction mechanism should the model understand?
    3. What functional groups are involved?
    4. What reagents or protecting groups are key to this reaction?
    5. What pattern should be extracted for similar reactions?

    Provide your analysis as a structured summary suitable for context documentation.
    """
    return call_llm(reflection_prompt)
```

### Phase 4: Build Organized Context

Create context organized by reaction type with the following structure for each:

```markdown
# <Reaction Type> Context

## Overview
Brief description of this reaction class and its key characteristics.

## Key Patterns
- List of common patterns observed in training data
- Structural features that identify this reaction type
- Common reagents and their SMILES representations

## Representative Examples
For each example:
- Product SMILES
- Reactants (with period separation)
- Key transformation details

## Common Pitfalls
- Common mistakes to avoid
- Edge cases to handle
- Common confusions with similar reaction types

## SMILES Notation Notes
- Important SMILES patterns for this reaction type
- Atom mapping considerations
- Stereochemistry handling
```

### Phase 5: Incremental Context Refinement

Since this is iteration 1 (no prior context exists), build comprehensive context from scratch:

1. **Create main context file**: `context/retrosynthesis_guide.md` with:
   - Overview of all reaction types
   - General retrosynthesis principles
   - SMILES notation guide for organic chemistry

2. **Create reaction-type files**: Individual files per reaction type:
   - `context/protections.md`
   - `context/deprotections.md`
   - `context/oxidations.md`
   - `context/reductions.md`
   - `context/acylation.md`
   - `context/cc_bond_formation.md`
   - `context/heteroatom_alkylation.md`
   - `context/heterocycle_formation.md`
   - `context/fgi.md`
   - `context/fga.md`

3. **Create examples file**: `context/examples.md` with curated examples organized by reaction type

### Phase 6: Validate Context Coverage

1. Cross-reference context with training samples to ensure coverage
2. Identify any reaction subtypes or patterns not covered
3. Add additional patterns as needed

## Key Principles

1. **Chemical Accuracy**: Ensure all chemistry information is accurate and reflects real organic reaction mechanisms

2. **SMILES Specificity**: Include actual SMILES strings for common reagents and functional groups

3. **Pattern Generalization**: Focus on generalizable patterns, not memorized examples

4. **Reaction Type Clarity**: Each reaction type should have clear identification criteria

5. **Complete Transformations**: Document full reactant lists (all period-separated SMILES)

## Implementation Notes

- Use `utils/llm.py` for structured reflection calls
- Use `utils/embedding.py` if needed for similarity-based grouping
- Context files should be markdown for readability
- Include specific SMILES examples (not just descriptions)
- Focus on patterns that generalize across multiple examples

## Expected Outputs

After executing this skill, the `context/` directory should contain:
- `retrosynthesis_guide.md` - Main overview and principles
- `protections.md` through `fga.md` - Individual reaction type guides
- `examples.md` - Curated examples with full SMILES

The base agent will automatically set retrieval to full retrieval, so all context will be available for inference.
