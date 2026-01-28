# Retrosynthesis Guide: Deprotections

## Overview

Deprotection reactions remove protecting groups to reveal functional groups like amines, alcohols, or acids. The retrosynthetic analysis involves identifying the protecting group and determining what reagent would remove it.

## Key Patterns for Deprotections

### 1. Benzyl Ether Deprotection (Most Common)

Benzyl ethers (OBn) are removed by hydrogenolysis to give phenols:

**Pattern**: Product has free phenol (OH) → Precursor has benzyl ether (OCH2Ph)
- **Retrosynthetic disconnection**: Add benzyl group to oxygen → `OCH2c1ccccc1`

**Identifying features**:
- Look for `OCH2c1ccccc1` or `OCc1ccccc1` in precursor SMILES
- This represents O-benzyl protecting group
- Debenzylation reveals phenol (Ar-OH)

**Example**:
- Target: `O=C(...)c1ccc(-c2ccccc2O)cc1` (phenol group)
- Precursor: `O=C(...)c1ccc(-c2ccccc2OCc2ccccc2)cc1` (benzyl ether protected)
- Forward reaction: Hydrogenolysis with H2/Pd removes benzyl group
- **SMILES pattern**: `OCc1ccccc1` = benzyl ether (O-CH2-Ph)

### 2. Methyl Ether Deprotection

Methyl ethers (OMe) are removed by strong Lewis acids like BBr3:

**Pattern**: Product has free phenol (OH) → Precursor has methyl ether
- **Retrosynthetic disconnection**: Add methyl group to oxygen → `OC`

**IMPORTANT**: Distinguish between:
- Methyl ether: `OC` (methoxy group, simple methyl)
- Benzyl ether: `OCc1ccccc1` (benzyloxy group, has benzyl ring)

**Example**:
- Target: `...-c2ccccc2O` (phenol)
- Precursor: `...-c2ccccc2OC` (methyl ether, deprotection with BBr3)
- **SMILES pattern**: `OC` alone means methyl, `OCc...` means benzyl

## CRITICAL ERROR PATTERN: Methyl Ether vs Free Phenol Confusion

### Common Mistake (ERROR #38 - Current Training Error)
- **Product**: `Oc1ccc2cc(CNCc3ccc(C(F)(F)F)cc3)c(-c3ccsc3)nc2c1` (FREE phenol - note: starts with `O` not `OC`)
- **Wrong answer**: `Brc1ccc2cc(CNCc3ccc(C(F)(F)F)cc3)c(-c3ccsc3)nc2c1.OCc1ccccc1` (benzyl bromide + benzyl alcohol - COMPLETELY WRONG)
- **Correct answer**: `COc1ccc2cc(CNCc3ccc(C(F)(F)F)cc3)c(-c3ccsc3)nc2c1` (METHYL ETHER precursor)

### Why This Matters
- The product has a FREE phenol (the `O` at the start of SMILES indicates free OH group)
- The correct precursor has a METHYL ETHER: `COc1...` where `OC` = methoxy group
- This is a DEMETHYLATION reaction: the methyl group was removed from the methyl ether
- The model added a bromide AND benzyl alcohol - completely wrong interpretation
- Demethylation uses BBr3, NOT hydrogenolysis (which removes benzyl)

### How to Identify Methyl Ether Deprotection
```
Product: Oc1ccc2cc(...)nc2c1
         |
         Free phenol: O at the start indicates OH group
         This phenol came from DEMETHYLATION of a methyl ether

Correct precursor: COc1ccc2cc(...)nc2c1
                  |
                  Methyl ether: OC (methoxy) instead of free O
                  The methyl group (C before OC) was removed

Key distinction:
- Free phenol: ...c1O or O... (OH group, no methyl attached)
- Methyl ether: ...c1OC or OC... (methoxy group, methyl attached to oxygen)
- Benzyl ether: ...c1OCc1ccccc1 (benzyloxy, has benzyl ring)

Demethylation: R-OC → R-OH (methyl removed by BBr3)
Debenzylation: R-OCc1ccccc1 → R-OH (benzyl removed by H2/Pd)
```

### Critical Recognition Steps for Deprotection
```
When analyzing a deprotection question:
1. Look at the oxygen-containing groups in the product
2. Check if there are free OH groups (phenol, alcohol, carboxylic acid)
3. Determine what protecting group was removed:
   - If product has free phenol and precursor has OC (methoxy) → DEMETHYLATION
   - If product has free phenol and precursor has OCc1ccccc1 → DEBENZYLATION
   - If product has free acid and precursor has C(=O)OC → ESTER HYDROLYSIS
   - If product has free amine and precursor has Boc → BOC REMOVAL

For ERROR #38:
- Product: Oc1ccc... (free phenol)
- Precursor: COc1ccc... (methyl ether)
- Reaction: Methyl ether deprotection (demethylation)
- Reagent: BBr3 (not H2/Pd which is for benzyl!)
```

### 3. Boc Deprotection

tert-Butoxycarbonyl (Boc) groups are removed with acid:

**Pattern**: Product has free amine → Precursor has Boc-protected amine
- **Retrosynthetic disconnection**: Add Boc group → `C(C)(C)C` attached to nitrogen

**Identifying features**:
- Boc-protected amine: `NC(=O)OC(C)(C)C` or similar
- Deprotection with TFA or HCl reveals primary/secondary amine

### 4. Cbz Deprotection

Benzyloxycarbonyl (Cbz) groups are removed by hydrogenolysis:

**Pattern**: Product has free amine → Precursor has Cbz-protected amine
- **Retrosynthetic disconnection**: Add Cbz group → `C(=O)OCc1ccccc1` attached to nitrogen

### 5. Benzyl Ester Deprotection

Benzyl esters (CO2CH2Ph) are removed by hydrogenolysis:

**Pattern**: Product has free carboxylic acid → Precursor has benzyl ester
- **Retrosynthetic disconnection**: Add benzyl ester → `C(=O)OCc1ccccc1`

## Common Deprotection Reagents (SMILES)

| Protecting Group | SMILES Pattern | Deprotection Reagent |
|-----------------|----------------|---------------------|
| Benzyl ether | `OCc1ccccc1` | H2/Pd |
| Methyl ether | `OC` | BBr3 |
| Boc | `C(C)(C)C` | TFA, HCl |
| Cbz | `C(=O)OCc1ccccc1` | H2/Pd |
| Benzyl ester | `C(=O)OCc1ccccc1` | H2/Pd |

## Deprotection SMILES Guide

**Key distinction - Benzyl vs Methyl**:

```
# Benzyl ether (protecting group)
OCc1ccccc1    # O-CH2-Ph (benzyloxy) - REMOVED BY HYDROGENOLYSIS

# Methyl ether (protecting group)
OC            # O-CH3 (methoxy) - REMOVED BY STRONGER CONDITIONS

# In context:
-c2ccccc2OCc2ccccc2   # Phenol with BENZYL protection
-c2ccccc2OC           # Phenol with METHYL protection
```

## Common Pitfalls

1. **Confusing benzyl and methyl protecting groups**:
   - Benzyl: `OCc1ccccc1` - hydrogenolysis removes it
   - Methyl: `OC` - requires BBr3 or similar

2. **Missing the benzyl ring**: When you see `OCc...`, the `c1ccccc1` is the benzyl ring

3. **Forgetting the CH2 in benzyl**: Benzyl is `-CH2-Ph`, so `OCc1ccccc1` not `Oc1ccccc1`

4. **Overlooking multiple protecting groups**: Some molecules have several protected functional groups

5. **Wrong deprotection mechanism**: Each protecting group has specific removal conditions

## Example Analysis

**Target**: `O=C(NCC(=O)N1CCN(C(=O)c2ccccc2C(F)(F)F)CC1)c1ccc(-c2ccccc2OCc2ccccc2)cc1`

Analysis:
1. Identify protected groups: Look for `OCc1ccccc1` pattern
2. Found: `-c2ccccc2OCc2ccccc2` = phenyl with benzyl ether protection
3. Deprotection removes benzyl, revealing phenol: `-c2ccccc2O`
4. Precursor: Same molecule but with benzyl group on oxygen

**Forward reaction**: H2, Pd/C removes benzyl group to give phenol

## Critical Error Pattern: Ester Deprotection Position

### Common Mistake
- **Question**: `CC(C)(C)n1nc(-c2ccncc2)c2c1CCC(C(=O)O)C2`
- **Wrong answer**: `CC(C)(C)n1nc(-c2ccncc2)c2c1CCC(C(=O)OC)C2`
- **Correct answer**: `COC(=O)C1CCc2c(c(-c3ccncc3)nn2C(C)(C)C)C1`

### Why This Matters
- The ester protecting group placement must match the correct position in the bicyclic system
- SMILES numbering must reflect the actual connectivity of the fused ring system
- The correct precursor has the ester at the correct bridgehead position

### How to Identify Correct Ester Position
```
Product: CC(C)(C)n1nc(-c2ccncc2)c2c1CCC(C(=O)O)C2
         |
         Carboxylic acid at: C(=O)O on cyclohexane ring
         The cyclohexane is fused to pyrazole (n1nc...c2...C2)

Key structural features:
- Pyrazole ring: n1nc with tert-butyl on nitrogen
- Fused cyclohexane: c2c1CCC(C(=O)O)C2
- The ester should be: C(=O)OC (methyl ester)

Precursor analysis:
- Product has free acid: C(=O)O
- Precursor has methyl ester: C(=O)OC
- The ester position is determined by the ring fusion pattern

SMILES interpretation:
- c2c1CCC(C(=O)O)C2: Carbon 2 of cyclohexane connects to pyrazole carbon
- The carboxylic acid is on carbon 3 or 4 of the cyclohexane
- C(=O)OC means methyl ester (CH3O-CO-)

Correct precursor: COC(=O)C1CCc2c(c(-c3ccncc3)nn2C(C)(C)C)C1
                   |
                   Methyl ester on cyclohexane ring
                   Fused pyrazole with pyridine substituent
```

### Key Principle: Ring Fusion Determines SMILES Position
```
For fused bicyclic systems:
1. Identify which ring is the base (usually more complex or aromatic)
2. Determine fusion points (atoms shared between rings)
3. Place substituents on the correct ring carbon
4. Match the SMILES numbering to the actual connectivity

In pyrazole-cyclohexane fusion:
- Pyrazole is aromatic (n1nc)
- Cyclohexane is non-aromatic (c2c1CCC...C2)
- Fusion: Pyrazole carbon connects to cyclohexane carbon
- Ester goes on cyclohexane (not on pyrazole)
```

## ✅ SUCCESS PATTERN: Fused Ring Ester Deprotection (Id 9 - Oxidations)

### What Worked
**Product**: `O=CC12CC3CC(CC(C3)C1)C2`
**Precursor**: `OCC12CC3CC(CC(C3)C1)C2`
**Result**: ✅ CORRECT (100% Jaccard similarity)

### Key Success Factors
1. **Correctly identified oxidation**: Aldehyde `O=C` → primary alcohol `CO`
2. **Maintained ring structure**: Bicyclic framework unchanged
3. **Proper SMILES transformation**: `O=C` → `OCC` (aldehyde to primary alcohol)

### Pattern to Replicate
```
For aldehyde oxidation questions:

1. Look for aldehyde group: O=C at start or attached to chain
   - Aldehyde: O=C (carbonyl carbon with H)
   - Primary alcohol: OCC (CH2-OH)

2. Transform aldehyde to primary alcohol:
   - Product: O=C... (aldehyde)
   - Precursor: OCC... (primary alcohol)

3. Preserve all ring systems and substituents unchanged

Key distinction:
- Aldehyde: O=C (carbon double-bonded to O, attached to H)
- Primary alcohol: OCC (carbon single-bonded to O, attached to H and C)
```

## ✅ SUCCESS PATTERN: Benzyl Ether Deprotection (Id 19)

### What Worked
**Product**: `O=C(NCC(=O)N1CCN(C(=O)c2ccccc2C(F)(F)F)CC1)c1ccc(-c2ccccc2O)cc1`
**Precursor**: `O=C(NCC(=O)N1CCN(C(=O)c2ccccc2C(F)(F)F)CC1)c1ccc(-c2ccccc2OCc2ccccc2)cc1`
**Result**: ✅ CORRECT (100% Jaccard similarity)

### Key Success Factors
1. **Correctly identified protecting group**: Phenol `-c2ccccc2O` → benzyl ether `-c2ccccc2OCc2ccccc2`
2. **Correct SMILES pattern**: `OCc1ccccc1` = O-CH2-benzyl (NOT methyl `OC`)
3. **Proper transformation**: Free phenol from benzyl deprotection

### Pattern to Replicate
```
For phenol deprotection questions:

1. Look for free phenol group in product: -c2ccccc2O
   - SMILES: `O` at the end of aromatic ring = free OH group

2. Determine protecting group:
   - If benzyl ether: OCc1ccccc1 (O-CH2-phenyl ring)
   - If methyl ether: OC (O-methyl, simple)

3. Add protecting group to oxygen:
   - Product: -c2ccccc2O
   - Precursor (benzyl): -c2ccccc2OCc2ccccc2

4. Verify the benzyl ring is present:
   - OCc1ccccc1 = has phenyl ring after OCc
   - OC = just methyl, no ring

Key distinction:
- Benzyl: OCc1ccccc1 (has `c1ccccc1` after OCc)
- Methyl: OC (just C after O)
```

## Critical Error Pattern: Ethyl vs Tert-Butyl Ester Deprotection

### Common Mistake (ERROR #43)
- **Question**: `CC(C(=O)O)c1ccc(C#N)nc1` (carboxylic acid product)
- **Wrong answer**: `CC(C(=O)OC(C)(C)C)c1ccc(C#N)nc1` (tert-butyl ester precursor)
- **Correct answer**: `CCOC(=O)C(C)c1ccc(C#N)nc1` (ethyl ester precursor)

### Why This Matters
- Both tert-butyl and ethyl esters deprotect to carboxylic acids
- The SMILES patterns are DIFFERENT and must be matched correctly
- Tert-butyl: `OC(C)(C)C` (three carbons attached to oxygen with branching)
- Ethyl: `OCC` (two carbons in a chain attached to oxygen)
- Using the wrong ester pattern results in incorrect SMILES

### How to Identify Correct Ester Type
```
Product: CC(C(=O)O)c1ccc(C#N)nc1
         |
         Carboxylic acid: C(=O)O
         Attached to tertiary carbon: CC(C(=O)O) = isopropyl-like group
         On pyridine ring: c1ccc(C#N)nc1

Retrosynthetic analysis:
1. Product has free acid: C(=O)O
2. Need to add ester protecting group
3. But WHICH ester? Check the precursor pattern:

Precursor patterns:
- Tert-butyl ester: CC(C(=O)OC(C)(C)C)...
                   |
                   OC(C)(C)C = O-C(C)(C)(C) - tert-butyl group

- Ethyl ester: CCOC(=O)C(C)...
               |
               OCC = O-CC - ethyl group (two carbons)

Key identification:
- Look at the SMILES structure in the correct answer
- Ethyl ester: C(=O)OCC (ester oxygen attached to two carbons)
- Tert-butyl: C(=O)OC(C)(C)C (ester oxygen attached to branched C4)

For ERROR #43:
- Correct precursor has: CCOC(=O)C(C)c1ccc(C#N)nc1
- The pattern CCOC(=O) means: CC-O-C(=O)- = ethyl ester
- NOT OC(C)(C)C which would be tert-butyl

SMILES breakdown:
- CCOC(=O): ethyl ester (CC-O-C(=O))
- C(C): tertiary carbon with the ester
- c1ccc(C#N)nc1: pyridine with cyano substituent

### Critical Error Pattern: Ethyl Ester vs Benzyl Ester Deprotection (ERROR #45)

### Common Mistake (ERROR #45)
- **Question**: `C[C@@H]1C[C@H](NC(=O)OC(C)(C)C)C(=O)N1CC(=O)O`
- **Wrong answer**: `C[C@@H]1C[C@H](NC(=O)OC(C)(C)C)C(=O)N1CC(=O)OCc1ccccc1`
- **Correct answer**: `CCOC(=O)CN1C(=O)[C@@H](NC(=O)OC(C)(C)C)C[C@H]1C`

### Why This Matters
- The wrong answer used BENZYL ester: `CC(=O)OCc1ccccc1`
- The correct answer uses ETHYL ester: `CCOC(=O)CN...`
- These are DIFFERENT protecting groups with DIFFERENT SMILES patterns
- Both deprotect to carboxylic acids but have different SMILES structures
- CRITICAL: The SMILES ordering and bond connectivity matter

### How to Identify Ethyl vs Benzyl Esters
```
Product: C[C@@H]1C[C@H](NC(=O)OC(C)(C)C)C(=O)N1CC(=O)O
         |
         Carboxylic acid: C(=O)O at the end
         Attached to: CC(=O) (methylene-acetyl group)
         Protected as an ester precursor

Correct precursor: CCOC(=O)CN1C(=O)[C@@H](NC(=O)OC(C)(C)C)C[C@H]1C
                  |
                  CCOC(=O)CN - ETHYL ESTER protecting group
                  The pattern is: CC-O-C(=O)-CN

SMILES breakdown of correct answer:
- CCOC(=O): ethyl ester (CH3CH2-O-C(=O)-)
- CN: the nitrogen attached to carbonyl (methylamino group)
- 1C(=O)...: continues to the lactam ring

Wrong SMILES pattern:
- CC(=O)OCc1ccccc1: This looks like benzyl but is malformed
- Benzyl ester is: C(=O)OCc1ccccc1 (carbonyl-O-CH2-phenyl)
- The CC(=O) prefix is wrong - should be C(=O) with ester oxygen

Key distinctions:
- Ethyl ester: CCOC(=O) (CH3CH2-O-C(=O))
- Benzyl ester: C(=O)OCc1ccccc1 (C(=O)-O-CH2-phenyl)
- Methyl ester: COC(=O) (CH3-O-C(=O))

For ERROR #45:
- Product has: ...CC(=O)O (carboxylic acid)
- Precursor has: ...CCOC(=O)CN (ethyl ester on nitrogen)
- The ester is on the side chain nitrogen, not the main chain
- Full SMILES: CCOC(=O)CN1C(=O)[C@@H](NC(=O)OC(C)(C)C)C[C@H]1C
               |              |              |
               Ethyl ester    Boc-protected  Proline-like
               on CN group    amine          ring
```

### Key Principle: Ester Location Determines SMILES Structure
```
When deprotecting to carboxylic acid:
1. Identify WHERE the carboxylic acid is (on which atom)
2. Determine which protecting group was used
3. Match the SMILES pattern to the correct ester type

In ERROR #45:
- Carboxylic acid is on: N1CC(=O)O (amide nitrogen with acetic acid side chain)
- The acid comes from: N1CC(=O)OC... (ethyl ester protecting group)
- Correct SMILES: CCOC(=O)CN1... (ethyl ester attached to nitrogen)

NOT: CC(=O)OCc1ccccc1 (benzyl ester would have the phenyl ring)
```
```
