# Retrosynthesis Guide: Reductions

## Overview

Reduction reactions decrease the oxidation state of carbon atoms. Common transformations include nitro → amine, alkene/alkyne → alkane, and carbonyl → alcohol.

## Common Reduction Patterns

### 1. Nitro to Amine

**Pattern**: Nitro group reduced to primary amine
- **SMILES change**: `[N+](=O)[O-]` → `N`
- **Reagents**: H2/Pd, Fe/HCl, Sn/HCl, Zn/NH4Cl

**Retrosynthetic**: Primary amine → nitro compound

### 2. Alkene to Alkane

**Pattern**: Carbon-carbon double bond reduced to single bond
- **SMILES change**: `C=C` → `CC`
- **Reagents**: H2/Pd, H2/Pt, H2/Ni

**Retrosynthetic**: Alkane → alkene

### 3. Alkyne to Alkane/Alkene

**Pattern**: Carbon-carbon triple bond reduced
- **Alkyne → Alkane**: H2/Pd, H2/Pt
- **Alkyne → cis-Alkene**: H2/Lindlar
- **Alkyne → trans-Alkene**: Na/NH3

### 4. Carbonyl Reduction

**Aldehyde → Primary alcohol**
- **SMILES change**: `C=O` → `CO`
- **Reagents**: NaBH4, LiAlH4

**Ketone → Secondary alcohol**
- **SMILES change**: `C(=O)C` → `C(O)C`
- **Reagents**: NaBH4, LiAlH4

**Retrosynthetic**: Alcohol → carbonyl (oxidation)

### 5. Ester/Alkanamide Reduction

**Ester → Alcohol**
- **Reagents**: LiAlH4 (NaBH4 won't reduce esters)

**Amide → Amine**
- **Reagents**: LiAlH4

## Common Reduction Reagents (SMILES)

| Reagent | SMILES | Use |
|---------|--------|-----|
| H2/Pd | (gas + catalyst) | Nitro, alkene, alkyne |
| NaBH4 | `[Na+].[B-H4]-` | Carbonyl (not ester) |
| LiAlH4 | `[Li+].[AlH4]-` | Carbonyl, ester, amide |
| Fe | `[Fe]` | Nitro (with HCl) |
| Zn | `[Zn]` | Nitro (with NH4Cl) |

## Retrosynthetic Pattern

For reduction reactions, work backward by **oxidizing** the reduced functional group:
- Amine → nitro (reverse of reduction)
- Alkane → alkene (reverse of hydrogenation)
- Primary alcohol → aldehyde (reverse of NaBH4)
- Secondary alcohol → ketone (reverse of NaBH4)

## Key Points

1. **Selective reductions**: NaBH4 reduces aldehydes/ketones but not esters; LiAlH4 reduces both
2. **Catalytic vs stoichiometric**: H2/Pd is catalytic; NaBH4/LiAlH4 are stoichiometric
3. **Stereochemistry**: Reduction can create chiral centers

## Critical Error Pattern: Benzoate Ester vs Benzyl Ether Deprotection

### Common Mistake (id: 24 - Current Training Error)
- **Product**: `CCc1ccc(CCOc2cccc(O)c2)nc1`
  - Free phenol: `-Oc2cccc(O)c2` (hydroxy on aromatic)
- **Wrong Answer**: `CCc1ccc(CCOc2cccc(OCc3ccccc3)c2)nc1`
  - Used benzyl ether: `-OCc3ccccc3` (O-CH2-phenyl)
- **Correct Answer**: `CCc1ccc(CCOc2cccc(OC(=O)c3ccccc3)c2)nc1`
  - Used benzoate ester: `-OC(=O)c3ccccc3` (O-C(=O)-phenyl)

### Why This Matters
- **CRITICAL**: The model confused benzyl ether (OCc) with benzoate ester (OC(=O)c)
- These are DIFFERENT protecting groups with DIFFERENT deprotection mechanisms:
  - Benzyl ether: H2/Pd hydrogenolysis removes entire benzyl group → free phenol
  - Benzoate ester: Base hydrolysis or reduction removes benzoate → free phenol
- In USPTO-50k, "Reductions" includes ester reductions/hydrolyses that reveal phenols
- The SMILES patterns are similar but have a critical difference: `OCc` vs `OC(=O)c`

### How to Distinguish Benzoate Ester from Benzyl Ether
```
Product: ...c2cccc(O)c2
         |
         Free phenol (hydroxy on aromatic ring)

Key question: What was the protecting group?

SMILES patterns:
- Benzoate ester: OC(=O)c1ccccc1
                 |  |  |
                 O  C  O
                 |  |  |
                 |  carbonyl
                 |  (ester)
                 O connected to aryl

- Benzyl ether: OCc1ccccc1
                |  |
                O  CH2
                   |
                   phenyl
                O connected to CH2, then phenyl

Visual distinction:
- OCc1ccccc1: O-CH2-Ph (oxygen bonded to methylene, bonded to phenyl)
- OC(=O)c1ccccc1: O-C(=O)-Ph (oxygen bonded to carbonyl, bonded to phenyl)

In ERROR #24:
- Product: ...cccc(O)c2 (free phenol)
- Wrong precursor: ...cccc(OCc3ccccc3)c2 (benzyl ether)
- Correct precursor: ...cccc(OC(=O)c3ccccc3)c2 (benzoate ester)

Transformation:
- Forward: Benzoate ester + H2/Pd → phenol + toluene (reduction)
- Retro: Phenol ← Benzoate ester + H2/Pd

SMILES change:
- Precursor: OC(=O)c1ccccc1 (benzoate ester)
- Product: O (free phenol)
- Remove: C(=O)c1ccccc3 (benzoate group)
```

### Critical SMILES Distinction
```
BE VERY CAREFUL with these similar patterns:

Benzyl ether (hydrogenolysis):
- SMILES: OCc1ccccc1
- Structure: O-CH2-Ph
- Deprotection: H2/Pd removes entire benzyl group
- Product: O-H (free phenol)

Benzoate ester (reduction/hydrolysis):
- SMILES: OC(=O)c1ccccc1
- Structure: O-C(=O)-Ph
- Deprotection: H2/Pd or base removes benzoate
- Product: O-H (free phenol)

Phenyl acetate (ester):
- SMILES: OC(C)=O
- Structure: O-C(=O)-CH3
- Deprotection: Base hydrolysis
- Product: O-H (free phenol)

How to tell in SMILES:
- Look for the pattern AFTER the O:
  - OCc = O connected to CH2 (benzyl)
  - OC(=O)c = O connected to C(=O) (benzoate ester)
  - OC(C)=O = O connected to C(=O)CH3 (acetate)

In ERROR #24:
- Correct: OC(=O)c3ccccc3 (benzoate ester)
- Wrong: OCc3ccccc3 (benzyl ether)
- Critical difference: C(=O) between O and phenyl!
```

## Critical Error Pattern: Phenol Ester Deprotection as "Reduction"

### Common Mistake
- **Question**: `CCc1ccc(CCOc2cccc(O)c2)nc1`
- **Reaction Type**: Reductions
- **Wrong answer**: Focused on pyridine N-oxide reduction
- **Correct answer**: Phenol was protected as benzoate ester in precursor

### Why This Matters
- Phenols can be protected as esters (acetate, benzoate, etc.)
- Deprotection (ester hydrolysis) reveals the free phenol
- This transformation may be classified as "Reduction" in some datasets
- The key is recognizing the phenol protection pattern

### How to Identify Phenol Ester Deprotection
```
Product: ...c2cccc(O)c2
          |
          Free phenol (hydroxy on aromatic ring)

Precursor: ...c2cccc(OC(=O)c3ccccc3)c2
           |
           Phenol protected as benzoate ester

SMILES patterns for phenol protection:
- Free phenol: O (at end of aromatic chain)
- Acetate ester: OC(C)=O
- Benzoate ester: OC(=O)c1ccccc1

Transformation:
- Forward: Phenol-OC(=O)R + H2O → Phenol-OH + RCOOH
- Retrosynthetic: Phenol-OH ← Phenol-OC(=O)R + H2O

Key distinction from benzyl ether:
- Benzyl ether: OCc1ccccc1 (O-CH2-phenyl)
- Ester: OC(=O)c1ccccc1 (O-C(=O)-phenyl)

How to tell them apart:
- OCc1ccccc1: Simple O-CH2 bond to ring
- OC(=O)c1ccccc1: O-C(=O) carbonyl then ring

Example:
- Product: CCc1ccc(CCOc2cccc(O)c2)nc1
           |
           Phenol: ...cccc(O)c2

- Precursor: CCc1ccc(CCOc2cccc(OC(=O)c3ccccc3)c2)nc1
             |
             Protected phenol: ...cccc(OC(=O)c3ccccc3)c2
```

## Critical Error Pattern: Nitro to Amine Reduction

### Common Mistake (ID 11 - Current Training Error)
- **Product**: `COc1cc(N)ccc1Oc1ccc(Cl)c(Cl)c1` (amino group on aromatic)
- **Wrong answer**: `Oc1cc(N)ccc1OC.Brc1ccc(Cl)c(Cl)c1` (treated as Williamson ether synthesis!)
- **Correct answer**: `COc1cc([N+](=O)[O-])ccc1Oc1ccc(Cl)c(Cl)c1` (nitro precursor reduced to amine!)

### Why This Matters
- The model completely missed that this is a NITRO → AMINE reduction
- Product has amino group (N) on aromatic ring
- Precursor has nitro group `[N+](=O)[O-]` on same position
- The reaction type "Reductions" should trigger nitro→amine pattern recognition
- This is NOT an ether formation reaction!

### How to Identify Nitro→Amine Reduction
```
Product: COc1cc(N)ccc1Oc1ccc(Cl)c(Cl)c1
         |
         The key feature: N on aromatic ring
         SMILES: c1cc(N)ccc1
         This is ANILINE (aromatic amine)

Precursor: COc1cc([N+](=O)[O-])ccc1Oc1ccc(Cl)c(Cl)c1
           |
           The key feature: [N+](=O)[O-] on aromatic ring
           SMILES: c1cc([N+](=O)[O-])ccc1
           This is NITROBENZENE derivative

Reduction transformation:
Forward: Nitroarene + Reducing Agent → Aniline
Retro: Aniline ← Nitroarene + Reducing Agent

SMILES change:
[N+](=O)[O-] → N  (nitro becomes amino)

Key patterns:
- Nitro group: [N+](=O)[O-] (nitrogen with + charge, double bond O, single bond O-)
- Amino group: N (simple nitrogen attached to aromatic)
- The transformation adds 6 hydrogen atoms (reduction)

Common reducing agents:
- H2/Pd (hydrogenation)
- Fe/HCl (iron and acid)
- Sn/HCl (tin and acid)
- Zn/NH4Cl (zinc and ammonium chloride)
```

### How to Distinguish from Other Reactions
```
The product COc1cc(N)ccc1Oc1ccc(Cl)c(Cl)c1 has:
1. Ether linkage: COc1...Oc1... (diaryl ether)
2. Amino group: cc(N)ccc (aniline)
3. Dichloroaryl: c(Cl)c(Cl)

Model's WRONG analysis:
- "This is Williamson ether synthesis"
- "Disconnect at the diaryl ether oxygen"
- "Precursors: phenol + aryl bromide"

But the REACTION TYPE is "Reductions"!
- The amino group N didn't come from a coupling reaction
- The amino group N came from REDUCTION of nitro group
- The ether linkage was ALREADY PRESENT in the precursor

CORRECT analysis:
1. Recognize: Reaction type = Reductions
2. Look for reducible groups: Nitro → Amine is most common
3. Find: Aniline in product → Nitroarene in precursor
4. Disconnection: Replace N with [N+](=O)[O-]

The ether linkage is NOT being formed in this reaction!
The entire molecule with nitro group is reduced to give the amino product.
```

### Correct Retrosynthetic Analysis for ID 11
```
Step 1: Check the reaction type
        Context says: "Reductions"
        This means we're looking for a reduction transformation

Step 2: Identify the reduced functional group
        Product: COc1cc(N)ccc1Oc1ccc(Cl)c(Cl)c1
                 |
                 Contains: N (amino group on aromatic)
                 This came from reduction!

Step 3: Find the oxidized precursor form
        Replace N with [N+](=O)[O-] (nitro group)
        Precursor: COc1cc([N+](=O)[O-])ccc1Oc1ccc(Cl)c(Cl)c1
                   |
                   All other groups (ether, chloro) unchanged
                   The nitro was reduced to amine

Step 4: Verify the reduction pattern
        Nitroarene (precursor) → Aniline (product)
        SMILES: [N+](=O)[O-] → N
        The aniline is NOT from coupling, it's from reduction!

Key distinction:
- Williamson ether synthesis: Forms C-O-C bond from phenol + aryl halide
- Nitro→Amine reduction: Converts NO2 to NH2, no bond formation at N

When reaction type is "Reductions":
- Look for NO2 → NH2 transformation
- Don't assume bond-forming reactions like coupling
- The entire molecule skeleton stays the same
```

### Common Mistake (ID 4)
- **Question**: Reduction with product `Cc1c(-c2ccc(=O)n(Cc3cccc(F)c3F)c2)c2cc(F)ccc2n1CCO`
- **Wrong answer**: `Cc1c(-c2ccc(=O)n(Cc3cccc(F)c3F)c2)c2cc(F)ccc2n1CC=O` (aldehyde)
- **Correct answer**: `Cc1c(-c2ccc(=O)n(Cc3cccc(F)c3F)c2)c2cc(F)ccc2n1CC(=O)O` (carboxylic acid)

### Why This Matters
- The model incorrectly predicted aldehyde (CC=O) as the reduced product
- The correct precursor has an ester (CC(=O)O) that was reduced to primary alcohol (CCO)
- This is an ester → alcohol reduction, not aldehyde formation
- Common reagents: LiAlH4 reduces esters to primary alcohols
- NaBH4 does NOT reduce esters (only aldehydes/ketones)

### How to Identify Ester Reduction
```
Product: ...n1CCO
         |
         Primary alcohol (ethanolamine-type group)
         The CCO pattern indicates CH2-CH2-OH

Precursor: ...n1CC(=O)O
           |
           Ester group (acetic acid ester)
           The CC(=O)O pattern indicates CH3-C(=O)-O (acetyl ester)

SMILES patterns for carbonyls:
- Aldehyde: CC=O (methyl + carbonyl double bond, no oxygen after)
- Carboxylic acid: CC(=O)O (methyl + carbonyl + hydroxyl)
- Ester: CC(=O)O (same as acid but different connectivity)
- Primary alcohol: CCO (methyl + methylene + oxygen)

Key distinction:
- Aldehyde: R-CHO (one H attached to carbonyl carbon)
- Ester: R-COO-R' (alkoxy group attached to carbonyl)
- Both can reduce, but to different products!

Reduction patterns:
- Aldehyde → primary alcohol (R-CHO → R-CH2OH)
- Ester → primary alcohol (R-COO-R' → R-CH2OH + R'OH)
- The alcohol product CCO comes from reducing an ester, not aldehyde

Looking at the product more carefully:
- CCO = CH2-CH2-OH (two carbons in chain)
- The acetyl ester CC(=O)O reduces to give CCO + acetic acid
- This is the reverse: ester reduced to primary alcohol
```

### Retrosynthetic Analysis for Ester Reduction
```
1. Identify the alcohol product pattern: CCO (primary alcohol with 2 carbons)
2. Look for ester precursor: CC(=O)O (acetyl group)
3. The forward reaction: ester + reducing agent (LiAlH4) → primary alcohol
4. In retrosynthesis: primary alcohol ← ester + reducing agent

Key insight:
- CCO comes from CC(=O)O (not CC=O which is aldehyde)
- The ester has 2 carbons (CC) that become the alcohol carbons
- LiAlH4 is required for ester reduction (NaBH4 doesn't work)
```
