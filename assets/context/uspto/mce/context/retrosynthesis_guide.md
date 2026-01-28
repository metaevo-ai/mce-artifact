# Retrosynthesis Guide: USPTO-50k Benchmark

## Overview

This guide covers retrosynthetic analysis for single-step retrosynthesis predictions on the USPTO-50k benchmark. Each reaction type has specific patterns and SMILES notation requirements.

## Reaction Types

### 1. Functional Group Addition (FGA)
Adding functional groups to molecules via nucleophilic substitution, electrophilic addition, or other mechanisms.

**Key patterns**:
- Thioether formation: Alkyl halide + thiol → thioether
- Bromine addition to alkenes
- Ester to amide conversion

**See**: `fga.md`

### 2. Deprotections
Removing protecting groups to reveal functional groups.

**Key patterns**:
- Benzyl ether deprotection: OCH2Ph → OH (hydrogenolysis)
- Boc deprotection: acid removes Boc group
- Cbz deprotection: hydrogenolysis removes Cbz

**See**: `deprotections.md`

### 3. Heterocycle Formation
Creating heterocyclic ring systems via cyclization, cycloaddition, or condensation.

**Key patterns**:
- Hantzsch thiazole: thioamide + α-halo carbonyl → thiazole
- Paal-Knorr pyrrole: 1,4-diketone + amine → pyrrole
- Imidazole, oxazole, pyridine syntheses

**See**: `heterocycle_formation.md`

### 4. Functional Group Interconversion (FGI)
Transforming one functional group to another while maintaining carbon skeleton.

**Key patterns**:
- Ester → amide (with ammonia)
- Acid → ester
- Nitrile → amidine
- Oxidation/reduction of carbonyls

**See**: `fgi.md`

### 5. Other Reaction Types

**C-C Bond Formation**: Suzuki, Stille, Heck, aldol, Grignard reactions
- New C-C bond formed between coupling partners

**Heteroatom Alkylation/Arylation**: Buchwald-Hartwig, Ullmann, Williamson
- New C-N, C-O, C-S bonds formed

**Oxidations**: Alcohol → carbonyl, sulfide → sulfoxide/sulfone
- Common reagents: PCC, Dess-Martin, m-CPBA

**Reductions**: Nitro → amine, alkene → alkane
- Common reagents: H2/Pd, NaBH4, LiAlH4

**Acylation**: Amide, ester, anhydride formation
- Common reagents: acyl chlorides, anhydrides

## General Retrosynthesis Principles

### Disconnection Strategy
1. Identify the functional groups in the product
2. Determine what bond(s) could be formed in the forward reaction
3. Work backward from product to precursors

### Key Questions
1. What reaction type is this? (check the context)
2. What bonds are formed? (where should I disconnect?)
3. What reagents would form this bond?
4. What do the precursors look like in SMILES?

### SMILES Notation Basics

**Functional group abbreviations**:
- Alcohol: `O` (hydroxyl group)
- Amine: `N` (amino group)
- Carbonyl: `C(=O)` or `C=O`
- Ester: `C(=O)OC` (methyl), `C(=O)OCC` (ethyl)
- Amide: `C(=O)N` (primary), `C(=O)NC` (secondary)
- Ether: `OC` (methoxy), `OCC` (ethoxy), `OCc1ccccc1` (benzyloxy)
- Thiol: `SH` (at chain end)
- Thioether: `CS` (methylthio), `CSc1ccccc1` (aryl thioether)

**Ring systems**:
- Benzene: `c1ccccc1`
- Piperazine: `N1CCNCC1`
- Thiazole: `c1sc[nH]1`
- Pyrazole: `c1n[nH]c[nH]1`

**Common patterns**:
- Methyl: `C`
- Ethyl: `CC`
- Propyl: `CCC`
- Phenyl: `c1ccccc1`
- Benzyl: `Cc1ccccc1`

## Critical SMILES Patterns

### Protecting Groups (MOST COMMON ERRORS)

**Benzyl vs Methyl Ether**:
```
# WRONG: Using methyl for what should be benzyl
-c2ccccc2OC           # This is methyl ether (methoxy)

# CORRECT: Benzyl ether protecting group
-c2ccccc2OCc1ccccc1   # This is benzyl ether (benzyloxy)
```

The key difference: `OC` alone = methyl, `OCc...` = benzyl

### Thioethers
```
# CORRECT: Thioether (S connecting two carbons)
CSc1ccc(...)          # Methylthio aryl
ClCc1ccc(...)         # Benzyl chloride (for making thioethers)

# WRONG: Confusing with chloromethyl sulfide
ClCS...               # Not how thioethers are formed
```

### α-Halo Carbonyls (for Hantzsch thiazole)
```
# CORRECT: Ethyl 2-bromo-3-oxobutanoate
CCOC(=O)C(Br)C(=O)    # Bromo at position 2

# WRONG: Malformed SMILES
BrC(C(=O)OCC)=O       # Incorrect structure
```

### Ester to Amide
```
# CORRECT: Ester + ammonia → amide
Precursor: ...C(=O)OC...
Reagent: N
Product: ...C(=O)N...

# WRONG: Missing ammonia
...C(=O)N... (no reagent specified)
```

## Common Error Patterns to Avoid

1. **Benzyl vs Methyl confusion**: Always check if the protecting group is benzyl (has ring) or methyl (simple C)

2. **Thioether formation**: Remember R-S-R' comes from R-X + R'-SH, not from adding SCCl

3. **Hantzsch thiazole reagents**: Thioacetamide is `CC(N)=S`, not something else. α-Halo carbonyl must have correct structure

4. **Amide formation**: Don't forget ammonia (`N`) as a reagent for ester → amide

5. **Deprotection precursors**: The protected form is the precursor, not the deprotected form

## Quick Reference: Reaction Type → Precursor Patterns

| Reaction Type | Product → Precursor Pattern |
|--------------|----------------------------|
| Deprotection | OH → OCH2Ph (add benzyl) or OC (add methyl) |
| FGA (thioether) | R-S-R' → R-X + R'-SH |
| FGA (bromination) | R-Br,R-Br → alkene + Br2 |
| FGI (ester→amide) | CONH2 → CO2CH3 + NH3 |
| Heterocycle (thiazole) | Thiazole → Thioamide + α-halo carbonyl |

## SMILES Validation Checklist

Before finalizing your answer:
- [ ] Are all atoms properly connected?
- [ ] Are parentheses balanced?
- [ ] Are ring closures numbered correctly (c1, c2, etc.)?
- [ ] Are functional groups in correct order (C(=O)O not CO(O))?
- [ ] Is the protecting group correctly identified (benzyl vs methyl)?
- [ ] Are reagents included (separated by periods)?

## Example Workflow

For a deprotection question:
1. Identify the product has a free phenol (OH)
2. Check for benzyl protecting group pattern: `OCc1ccccc1`
3. Precursor is product with benzyl added to oxygen
4. Forward reaction: H2, Pd/C removes benzyl

For a thiazole question:
1. Identify thiazole ring: `c1sc[nH]1` pattern
2. Find substituents on ring
3. Match to Hantzsch components
4. Use thioacetamide (`CC(N)=S`) for C2 substituent
5. Use correct α-halo carbonyl SMILES

## Critical SMILES Notation Patterns (From Training Errors)

### 1. Ring Numbering is Arbitrary

**Rule**: Ring numbers (`1`, `2`, `3`) in SMILES are arbitrary labels for connectivity, not specific atom identifiers.

**Example - Dithiolane Ring**:
```
Product: Cc1nc(NC(=O)CCCCC2CCSS2)sc1...
         |
         Ring 2 is the dithiolane (CCSS2)

Precursor (wrong): O=C(O)CCCCC2CCSS2
                   Using ring 2 (may not match expected answer)

Precursor (correct): O=C(O)CCCCC1CCSS1
                     Using ring 1 (matches expected answer format)

Key: Both represent the same molecule. Use the ring number that
     matches the expected answer format (usually 1 if connecting).
```

### 2. Same Bicyclic Structure, Different SMILES Representations

**Rule**: Fused ring systems can be written starting from different atoms, resulting in different but equivalent SMILES.

**Example - Indole-Piperazine Fusion**:
```
Product: CC(C)(C)OC(=O)N1CCn2c(cc3ccccc32)C1
         |
         Piperazine-indole fused system

SMILES Option 1: O=C1CCn2c(cc3ccccc32)C1
                 Starts from piperazine carbonyl

SMILES Option 2: c1ccc2c(c1)cc1n2CCNC1
                 Starts from indole phenyl ring

Both are valid representations of the same bicyclic system.
Use the format matching expected answers.
```

### 3. Acylation Site Selectivity

**Rule**: In molecules with multiple acylation sites, identify which fragment contains the acyl group.

**Example - β-Keto Amide Acylation**:
```
Product: ...NC(=O)CC(=O)c2ccnc(-c3cc(C)no3)c2...
         |
         β-Keto amide: NC(=O)CC(=O)- pattern

Analysis:
1. The fragment c2ccnc(-c3cc(C)no3)c2 contains the keto carbonyl
2. This fragment undergoes acylation with a β-keto acid
3. β-Keto acid precursor: O=C(O)CC(=O)c2ccnc(-c3cc(C)no3)c2

Key: Look for characteristic patterns:
- β-Keto amide: NC(=O)CC(=O)-
- β-Keto acid: HOOC-CC(=O)-
- Match carbonyl + carbon chain to find acylation site
```

### 4. Ester Position in Fused Ring Systems

**Rule**: For deprotection of esters in fused systems, the ester position must match the actual connectivity.

**Example - Pyrazole-Cyclohexane Fusion**:
```
Product: CC(C)(C)n1nc(-c2ccncc2)c2c1CCC(C(=O)O)C2
         |
         Carboxylic acid on cyclohexane ring

Precursor (wrong): ...CCC(C(=O)OC)C2
                   Incorrect ester position/connectivity

Precursor (correct): COC(=O)C1CCc2c(c(-c3ccncc3)nn2C(C)(C)C)C1
                     Correct: methyl ester at proper position
                     Correct: fused ring numbering

Key:
1. Identify the base ring (usually aromatic)
2. Determine fusion points
3. Place ester on correct ring carbon
4. Match SMILES numbering to actual connectivity
```

## Quick Reference: SMILES Validation

| Issue | Check | Fix |
|-------|-------|-----|
| Ring numbers | Using consistent numbering | Use same number for connected atoms |
| Bicyclic systems | Different SMILES formats | Match expected answer format |
| Acylation sites | Which fragment has carbonyl? | Identify β-keto/activated pattern |
| Ester position | Fused ring connectivity | Place ester on correct ring carbon |
| Protecting groups | Benzyl vs methyl | Check for ring in `OCc...` |

---

## C-C Bond Formation: Critical Pattern Guide

### 1. Suzuki vs Sonogashira Coupling

**Key Distinction**:
| Feature | Suzuki | Sonogashira |
|---------|--------|-------------|
| Partner 1 SMILES | `B(O)O` (boronic acid) | `C#C` (terminal alkyne) |
| Product | No alkyne | Has alkyne (C#C) |

**Common Mistake**: Confusing `B(O)O` with `C#C`
- **WRONG**: Using `C#C` for Suzuki
- **CORRECT**: `c1ccc(B(O)O)cc1` for Suzuki (aryl boronic acid)

### 2. Wittig vs Cross-Coupling

**Key Distinction**:
| Feature | Wittig | Cross-Coupling |
|---------|--------|----------------|
| Product has | Alkene (C=C) from carbonyl + ylide | C-C bond, no new C=C |
| Partner 1 SMILES | `C[P+](...)` (ylide) | Organometallic (B, Sn, Zn) |
| Partner 2 SMILES | `C=O` (carbonyl) | Halide (Br, I, Cl) |

**Wittig Pattern**: Product with vinyl group → disconnect at C=C
- Look for: `C=C` attached to aromatic/alkyl
- Precursor 1: Carbonyl compound (`C=O`)
- Precursor 2: Phosphonium ylide (`C[P+](...)`)

### 3. Halide Specificity (Br vs I vs Cl)

| Halide | SMILES | Common Use |
|--------|--------|------------|
| Iodine | `I` | Stille, Sonogashira (most reactive) |
| Bromine | `Br` | Suzuki, Heck, Sonogashira (common) |
| Chlorine | `Cl` | Suzuki (special catalysts) |

**Critical**: Match the halide correctly. Using `I` when answer expects `Br` is wrong.

### 4. Protecting Groups in Ylides

Wittig ylides can contain protected functional groups:

**Benzyl ether protecting group**:
- SMILES: `OCc1ccccc1`
- Structure: O-CH2-Ph (NOT methyl ether `OC`)

**Example**: Ylide with benzyl protection
```
c1ccc(COc2ccccc2C[P+](c2ccccc2)(c2ccccc2)c2ccccc2)cc1
       |              |
       benzyl ether   phosphonium ylide
```

### 5. Reduction: Alkene Hydrogenation

**Pattern**: Saturated chain with ester → alkene precursor with same ester
- Product: `CCCCOC(=O)CCc1...` (saturated chain)
- Precursor: `CCCCOC(=O)/C=C/c1...` (alkene in chain)
- SMILES `/C=C/` indicates the double bond that was hydrogenated

**Key**: The ester stays the same, only the alkene is reduced!

## Critical Patterns from Training Analysis

### 1. Acetylating Agent Selection

**Key distinction**: Acetic anhydride vs acetyl chloride
- Both can acetylate amines to form acetamides
- Anhydride: `CC(=O)OC(=O)C` (milder, less likely to cause racemization)
- Acid chloride: `CC(=O)Cl` (more reactive)

**When to use which**:
- Prefer anhydride for substrates with sensitive stereochemistry
- Check training examples for patterns

### 2. Phenol Protecting Groups

**Key distinction**: Ester vs ether protection
- Phenol ester: `OC(=O)c1ccccc1` (O-C(=O)-phenyl, benzoate)
- Phenol ether: `OCc1ccccc1` (O-CH2-phenyl, benzyl ether)

**How to tell apart**:
- Look for `OC(=O)` pattern → ester protection
- Look for `OCc` pattern → ether protection

### 3. Azide Formation

**SMILES pattern**: `[N+]=[N-]` (linear azide group)
- Converts amines to azides using azide sources
- Azide appears as N=[N+]=[N-] in SMILES
- Different from nitro groups `[N+](=O)[O-]`

### 4. Ester Deprotection as "Reduction"

When classified as "Reduction":
- Phenol ester hydrolysis reveals free phenol
- Product has free phenol: `...c(O)c...`
- Precursor has ester: `...c(OC(=O)R)c...`
- Look for `OC(=O)` pattern for ester protection
