# Retrosynthesis Guide: Functional Group Interconversion (FGI)

## Overview

Functional Group Interconversion (FGI) involves transforming one functional group into another while maintaining the carbon skeleton. Common examples include ester-amide, acid-ester, and alcohol-ketone conversions.

## Key Patterns for FGI

### 1. Ester to Amide Conversion

Esters convert to amides via nucleophilic acyl substitution:

**Pattern**: Product has `C(=O)N` where precursor has `C(=O)OC`
- **Retrosynthetic disconnection**: Replace alkoxy group with amine/nitrogen

**Identifying features**:
- Carbonyl carbon bonded to nitrogen (amide N) instead of oxygen (ester O)
- Common transformation in peptide and pharmaceutical synthesis

**Correct SMILES patterns**:
- **Methyl ester**: `C(=O)OC` (carbonyl with O-CH3)
- **Ethyl ester**: `C(=O)OCC` (carbonyl with O-CH2-CH3)
- **Primary amide**: `C(=O)N` (carbonyl with NH2)
- **Ammonia**: `N` (simple nitrogen)

**Mechanism**:
- Forward: R-COOCH3 + NH3 → R-CONH2 + CH3OH
- Retrosynthetic: R-CONH2 ← R-COOCH3 + NH3

**Important notes**:
- Use `N` for ammonia, not `[NH3]` or other forms
- The leaving group is the alcohol from the ester

**Example**:
- Target: `...C(=O)N...` (amide)
- Precursor: `...C(=O)OC...` (ester) + `N` (ammonia)
- Transformation: Ester + ammonia → amide + methanol

## ✅ SUCCESS PATTERN: Oxime Formation from Carbonyl (Id 14)

### What Worked
**Product**: `CC(C)(C)c1cc(C=NO)c(O)c(-c2ccc(C(F)(F)F)nc2)c1`
**Precursor**: `CC(C)(C)c1cc(C=O)c(O)c(-c2ccc(C(F)(F)F)nc2)c1.NO`
**Result**: ✅ CORRECT (100% Jaccard similarity)

### Key Success Factors
1. **Correctly identified FGI**: Oxime `C=NO` → carbonyl `C=O` + hydroxylamine
2. **Proper disconnection**: Break C=N bond to get aldehyde + hydroxylamine
3. **Correct reagents**: Carbonyl compound and hydroxylamine (`NO` in SMILES)

### Pattern to Replicate
```
For oxime formation questions:

1. Look for oxime group in product: C=NO
   - SMILES: C=NO (carbon double-bonded to N, N bonded to O)
   - This is a C=N-OH group (oxime)

2. Recognize this as FGI from carbonyl:
   - Oxime forms from: carbonyl + hydroxylamine
   - Carbonyl: C=O (aldehyde or ketone)
   - Hydroxylamine: NO (N-O, simple representation)

3. Retrosynthetic disconnection:
   - Product: ...C=NO...
   - Precursor 1: ...C=O... (aldehyde/ketone)
   - Precursor 2: NO (hydroxylamine)

4. Verify the carbonyl type:
   - If attached directly to ring: aldehyde (C=O, not C(=O))
   - If attached to two carbons: ketone (C(=O)C)

Key distinction:
- Oxime: C=NO (C=N-OH, from carbonyl + NH2OH)
- Aldehyde: C=O (from primary alcohol oxidation)
- Ketone: C(=O)C (from secondary alcohol oxidation)
```

### 2. Acid Chloride to Amide

Acid chlorides react with amines to form amides:

**Pattern**: Product has amide → Precursor has acid chloride + amine
- **Retrosynthetic disconnection**: Break C-N bond → acid chloride + amine

### 3. Nitrile to Amidine

Nitriles convert to amidines via Pinner reaction or other methods:

**Pattern**: Product has `C(=N)N` → Precursor has `C#N`
- **Retrosynthetic disconnection**: Add ammonia to nitrile → amidine

### 4. Alcohol to Carbonyl (Oxidation)

Alcohols oxidize to carbonyl compounds:

**Pattern**: Product has C=O → Precursor has CH-OH
- **Retrosynthetic disconnection**: Reduce carbonyl → alcohol

### 5. Alkene to Alkane (Reduction)

Alkenes reduce to alkanes:

**Pattern**: Product has single bond → Precursor has double bond
- **Retrosynthetic disconnection**: Add H2 to alkene → alkane

## Common FGI Transformations (SMILES)

| Transformation | Precursor SMILES | Product SMILES | Reagent |
|---------------|------------------|----------------|---------|
| Ester → Amide | `C(=O)OC` | `C(=O)N` | NH3 |
| Ester → Acid | `C(=O)OC` | `C(=O)O` | H2O, H+ |
| Acid → Ester | `C(=O)O` | `C(=O)OC` | ROH, H+ |
| Nitrile → Amidine | `C#N` | `C(=N)N` | NH3, HCl |
| Alkene → Alkane | `C=C` | `CC` | H2, Pd |
| Alcohol → Ketone | `C(O)C` | `C(=O)C` | Oxidation |
| Primary alcohol → Aldehyde | `CO` | `C=O` | PCC, Dess-Martin |

## SMILES Notation for FGI

**Key patterns**:
- Ester methyl: `C(=O)OC` - carbonyl carbon, double bond O, single bond O, single bond C
- Ester ethyl: `C(=O)OCC` - carbonyl carbon, double bond O, single bond O, single bond C, single bond C
- Primary amide: `C(=O)N` - carbonyl carbon, double bond O, single bond N
- Ammonia: `N` - single nitrogen atom

**Important distinction**:
```
# Methyl ester (reactive)
C(=O)OC

# Ethyl ester (reactive)
C(=O)OCC

# Amide (product)
C(=O)N

# Ammonia (reagent)
N
```

## Common Pitfalls

1. **Wrong leaving group**: Esters leave alkoxide (becoming alcohol), amides leave amide ion (becoming ammonia)

2. **Confusing amide nitrogen source**:
   - Primary amide from ammonia: `C(=O)N` + H2O
   - Secondary amide from primary amine: `C(=O)NC`
   - Tertiary amide from secondary amine: `C(=O)N(CC)C

3. **Forgetting to add nitrogen**: When converting ester to amide, ammonia is a reactant

4. **Incorrect SMILES for ammonia**: Use simple `N`, not complex representations

5. **Missing the carbonyl oxygen**: Both ester and amide have `C(=O)`

6. **Over-complicating**: Some FGIs are direct, not multi-step transformations

## Example Analysis

**Target**: `CCNc1nccc2c1c(C(=O)N)nn2-c1cccc(C#C[C@]2(O)CCN(C)C2=O)c1`

Analysis:
1. Identify FGI: Look for amide `C(=O)N` in context of other carbonyls
2. Found: `c(C(=O)N)nn2` = amide attached to heterocycle
3. Retrosynthetic disconnection: `C(=O)N` → `C(=O)OC` + `N`
4. Precursor: Same molecule but with methyl ester instead of amide
5. Forward reaction: Ester + ammonia → amide + methanol

**Key pattern**: Amide = ester converted with ammonia

## Critical Error Pattern: gem-Diol/Hydrate Formation

### Common Mistake (ERROR #28)
- **Question**: `O=C1C(c2ccc(Br)cc2O)c2ccccc2N1C(c1ccccc1)c1ccccc1`
- **Wrong answer**: `O=C1OC(=O)c2ccc(Br)cc2O1.CN(c1ccccc1)c1ccccc1`
- **Correct answer**: `O=C1N(C(c2ccccc2)c2ccccc2)c2ccccc2C1(O)c1ccc(Br)cc1O`

### Why This Matters
- The product contains a gem-diol/hydrate: `C1(O)` - a carbon with two OH groups
- This is NOT an anhydride opening but a ketone hydrate
- The precursor is a KETONE: `C1(=O)` which adds water to form the gem-diol
- Anhydride would give a different product structure entirely

### How to Identify Ketone Hydrates
```
Product: O=C1N(C(c2ccccc2)c2ccccc2)c2ccccc2C1(O)c1ccc(Br)cc1O
         |
         C1(O) = carbon with TWO oxygen substituents
         This is a gem-diol (hydrate of a ketone)

Structure analysis:
- The imide/amide part: O=C1N(...)c2ccccc2N1
- The gem-diol part: C1(O)c1ccc(Br)cc1O
- This is an ortho-hydroxy aryl ketone that forms a hydrate

Precursor: Same structure but C1(=O) instead of C1(O)
           The ketone carbonyl adds water to form the gem-diol

SMILES distinction:
- Ketone: C1(=O) (carbon with =O double bond)
- Gem-diol: C1(O) (carbon with two single-bonded O atoms)
- Anhydride: O=C1OC(=O)... (two carbonyls connected by oxygen)

For ERROR #28:
- Correct precursor has ketone: C1(=O)
- Hydration gives: C1(O) (gem-diol)
- NOT an anhydride structure
```

### Key Principle: Count Oxygen Substituents
```
To identify gem-diol vs anhydride:
1. Look at the carbon with oxygen substituents
2. If carbon has: (=O) - it's a ketone/aldehyde
3. If carbon has: (O) and another (O) - it's a gem-diol
4. If you see: O=C1OC(=O) - it's an anhydride

Example:
- O=C1C(c2ccc(Br)cc2O)... - the C1 has ONE oxygen (=O) = ketone
- ...C1(O)c1ccc(Br)cc1O - the C1 has TWO oxygens = gem-diol
- O=C1OC(=O)c2ccc(Br)cc2O1 - TWO carbonyls with oxygen between = anhydride
```

## Critical Error Pattern: Ester vs Carboxylic Acid in Amide Formation

### Common Mistake (ID 46 - Current Training Error)
- **Product**: `CC[C@@]1(O)CC[C@@]2(Cc3ccccc3)c3ccc(C(=O)Nc4cccnc4C)cc3COC[C@H]2C1` (amide product)
- **Wrong answer**: `CC[C@@]1(O)CC[C@@]2(Cc3ccccc3)c3ccc(C(=O)O)cc3COC[@@H]2C1.Cc1cccnc1N` (carboxylic acid precursor!)
- **Correct answer**: `CC[C@@]1(O)CC[C@@]2(Cc3ccccc3)c3ccc(C(=O)Nc4cccnc4C)cc3COC(O)[C@H]2C1` (ester precursor!)

### Why This Matters
- The model used `C(=O)O` (carboxylic acid) as the precursor
- The correct precursor should be `C(=O)OC` (ester)
- The difference is ONE OXYGEN atom in the SMILES notation!
- **Carboxylic acid**: `C(=O)O` (carbonyl + hydroxyl group)
- **Ester**: `C(=O)OC` (carbonyl + methoxy group - note the extra C!)
- This is a critical distinction in retrosynthesis

### How to Identify Ester Precursor for Amide Formation
```
Amide formation retrosynthesis:
Product (amide): R-C(=O)-NR'2
                 |
                 Disconnect at C-N bond
                 |
Precursor 1 (carbonyl): R-C(=O)-OR'' (ESTER, not acid!)
Precursor 2 (amine): H-NR'2 (or NR'2)

SMILES distinction:
# WRONG - Carboxylic acid (C(=O)O):
R-C(=O)O  - Carbonyl carbon attached to hydroxyl (OH)
           No additional carbon after the oxygen
           Example: acetic acid: CC(=O)O

# CORRECT - Ester (C(=O)OC):
R-C(=O)OC - Carbonyl carbon attached to alkoxy (OR'')
           Additional carbon AFTER the oxygen
           Example: methyl acetate: CC(=O)OC

Key pattern:
- Look for the atom AFTER the carbonyl oxygen
- If it's C (carbon): ESTER
- If it's end of chain or nothing: CARBOXYLIC ACID

In the target molecule:
...c3ccc(C(=O)Nc4cccnc4C)...
            |
            Amide bond: C(=O)-N
            |
            Replace N with O to get: C(=O)OC (methyl ester)
            NOT C(=O)O (carboxylic acid)
```

### Why Esters are Common Amide Precursors
```
1. Esters are more stable and easier to handle than acid chlorides
2. Amide synthesis from esters: R-COOR' + R''NH2 → R-CONHR'' + R'OH
3. The ester oxygen (OR') becomes the leaving group (alcohol)
4. Retrosynthetic: R-CONHR'' ← R-COOR' + R''NH2

In SMILES:
- Forward: Ester (R-C(=O)OC) + Amine (HN) → Amide (R-C(=O)N) + Alcohol (OC)
- Retro: Amide (R-C(=O)N) → Ester (R-C(=O)OC) + Amine (HN)

Critical check:
- Is there a carbon AFTER the carbonyl oxygen in the ester SMILES?
- YES: C(=O)OC (ester) ✓
- NO: C(=O)O (carboxylic acid) ✗
```

### Correct Retrosynthetic Analysis for ID 46
```
Step 1: Identify the amide in product
        CC[C@@]1(O)CC[C@@]2(Cc3ccccc3)c3ccc(C(=O)Nc4cccnc4C)cc3COC[C@H]2C1
        |
        The amide: C(=O)Nc4cccnc4C
        - Carbonyl carbon bonded to nitrogen
        - Nitrogen bonded to methylpyridine

Step 2: Disconnect at amide C-N bond
        Fragment 1 (ester): CC[C@@]1(O)CC[C@@]2(Cc3ccccc3)c3ccc(C(=O)OC)cc3COC[C@H]2C1
                            |
                            NOTE: C(=O)OC (ester with methyl)
                            NOT C(=O)O (carboxylic acid)
        Fragment 2 (amine): Cc1cccnc1N
                            |
                            Methylpyridinamine

Step 3: Verify forward reaction
        Ester (C(=O)OC) + Amine (HN) → Amide (C(=O)N) + Methanol (OC)
        The ester methyl group becomes the leaving group (methanol)

Key distinction in SMILES:
- Carboxylic acid: R-C(=O)O (no carbon after O)
- Ester: R-C(=O)OC (carbon after O - this is the alcohol leaving group)

If you write C(=O)O, you're saying carboxylic acid, not ester!
```

### Common Mistake
- **Question**: `C[C@H]1C[C@@H](c2ccncc2NC(=O)c2ccc(F)c(-c3c(F)cccc3F)n2)C[C@@H](NC(=O)OC(C)(C)C)[C@H]1N`
- **Wrong answer**: Used carboxylic acid `O=C(O)c1ccc(F)c(-c2c(F)cccc2F)n1`
- **Correct answer**: Used azide `C[C@H]1C[C@@H](c2ccncc2NC(=O)c2ccc(F)c(-c3c(F)cccc3F)n2)C[C@@H](NC(=O)OC(C)(C)C)[C@H]1N=[N+]=[N-]`

### Why This Matters
- Amines can be converted to azides (R-N3) using azide sources
- Azides are versatile intermediates for further transformations
- The azide group appears as `[N+]=[N-]` in SMILES notation
- This is a functional group interconversion: amine → azide

### How to Identify Azide Formation
```
Product: ...N (amine)
          |
          Transformed to azide in precursor

SMILES pattern for azide: N=[N+]=[N-]
                           |
                           Attached to carbon or nitrogen

Transformation:
- Forward: R-NH2 + (azide source) → R-N3
- Retrosynthetic: R-N3 ← R-NH2 + (azide source)

Common azide sources:
- NaN3 (sodium azide)
- TfN3 (trifluoromethanesulfonyl azide)
- Diphenylphosphoryl azide (DPPA)

SMILES for sodium azide: [N-]=[N+]=N.[Na+]

Key distinction:
- Amine: N (attached to carbon, no explicit hydrogens shown)
- Azide: N=[N+]=[N-] (linear three-nitrogen chain)

Example:
- Product has: ...[C@H]1N (amine)
- Precursor has: ...[C@H]1N=[N+]=[N-] (azide)
- The azide is the precursor form, which converts to amine
```

## Critical Error Pattern: Carbonyl Position in Multi-Ring Systems (ID 28)

### Common Mistake (ID 28 - Current Training Error)
- **Question**: FGI with product `O=C1N(C(c2ccccc2)c2ccccc2)c2ccccc2C1(O)c1ccc(Br)cc1O`
- **Wrong answer**: `O=C1N(C(c2ccccc2)c2ccccc2)c2ccccc2C1(=O)c1ccc(Br)cc1O` (wrong ring carbon!)
- **Correct answer**: `O=C1N(C(c2ccccc2)c2ccccc2)c2ccccc2C1(=O)c1ccc(Br)cc1O` but with carbonyl on CORRECT ring carbon

### Why This Matters
- The product contains a gem-diol: `C1(O)` (carbon with two OH groups)
- This is a hydrate of a ketone
- The precursor is the same molecule with a ketone: `C1(=O)` (carbon with =O double bond)
- **Critical**: Which ring carbon has the carbonyl?
- The model placed the carbonyl on the wrong ring atom, changing the connectivity

### How to Identify Correct Carbonyl Position
```
Product: O=C1N(C(c2ccccc2)c2ccccc2)c2ccccc2C1(O)c1ccc(Br)cc1O
         |
         Structure analysis:
         |
         Part 1: O=C1N(...)c2ccccc2N1
         |      |
         |      This is an imide/amide ring system
         |      Carbonyl (O=C1) attached to nitrogen (N1)
         |
         Part 2: C1(O)c1ccc(Br)cc1O
                 |
                 This is a gem-diol attached to phenol ring
                 C1 has TWO oxygens (O) = gem-diol
                 c1ccc(Br)cc1O = phenol ring with Br

The key question: Which carbon of the amide ring connects to the gem-diol?

SMILES parsing:
O=C1N(C(c2ccccc2)c2ccccc2)c2ccccc2C1(O)c1ccc(Br)cc1O
     |                               |
     C1                               C1
     (first carbonyl carbon)          (gem-diol carbon)
     |                               |
     Connects to N                   Connects to phenol

The gem-diol C1 is a DIFFERENT carbon than the carbonyl C1!
They are connected through the ring system.

Precursor: Same structure but with C1(=O) instead of C1(O)
           The ketone carbonyl is on the SAME carbon as the gem-diol
           NOT on the amide carbonyl carbon!

SMILES comparison:
WRONG: ...c2ccccc2C1(=O)c1ccc(Br)cc1O
       |          |
       Ring       Carbon 1 has =O (ketone)
       carbon 2   This is WRONG position!

CORRECT: Need to trace connectivity to find which ring carbon
         connects to the gem-diol attachment point
```

### Step-by-Step Carbonyl Position Analysis
```
Step 1: Identify the gem-diol in product
        O=C1N(C(c2ccccc2)c2ccccc2)c2ccccc2C1(O)c1ccc(Br)cc1O
                                                    |
                                                    C1(O) = gem-diol
                                                    This carbon has two OH groups

Step 2: Find attachment point to ring system
        The gem-diol is attached at: C1 (ring closure 1)
        This C1 connects to: c1ccc(Br)cc1O (phenol ring)

Step 3: Trace back through the SMILES
        C1(O)c1ccc(Br)cc1O - the C1 closes a ring
        What does it connect to?

        Looking at: ...c2ccccc2C1(O)c1...
                    |          |
                    c2         C1
                    (ring carbon 2) (gem-diol carbon 1)

        The attachment is at: c2ccccc2 (the c2 before C1)
        This is ring carbon number 2 of the inner ring

Step 4: The carbonyl precursor should have C(=O) on the SAME carbon
        The carbon that has C1(O) in product should have C1(=O) in precursor
        NOT the carbonyl carbon of the amide (O=C1 at start)

SMILES validation:
WRONG: O=C1(=O)c2ccccc2C1(O)c1ccc(Br)cc1O
       |      |
       Carbon 1 has TWO oxygens = impossible!
       Carbon can't have both =O and connect to another ring

CORRECT: O=C1(=O) represents the amide carbonyl
         The gem-diol is on a DIFFERENT carbon
         Need to trace connectivity carefully

Key principle:
- Each ring closure number (1, 2, 3...) is a SEPARATE atom
- C1(...) at start ≠ C1(...) in middle of SMILES
- Track which carbon connects to which
```

## Critical Error Pattern: Diazotization (ID 31 - Current Training Error)

### Common Mistake
- **Question**: FGI with product `C[C@H]1C[C@@H](c2ccncc2NC(=O)c2ccc(F)c(-c3c(F)cccc3F)n2)C[C@@H](NC(=O)OC(C)(C)C)[C@H]1N`
- **Wrong answer**: `C[C@H]1C[C@@H](c2ccncc2NC(=O)c2ccc(F)c(-c3c(F)cccc3F)n2)C[C@@H](NC(=O)OC(C)(C)C)[C@H]1N`
  - **Missing**: The diazonium group `N=[N+]=[N-]` at the end
- **Correct answer**: `C[C@H]1C[C@@H](c2ccncc2NC(=O)c2ccc(F)c(-c3c(F)cccc3F)n2)C[C@@H](NC(=O)OC(C)(C)C)[C@H]1N=[N+]=[N-]`

### Why This Matters
- The model completely missed a diazotization reaction
- Amines (R-NH2) can be converted to diazonium salts (R-N₂⁺) via diazotization
- This is a **Functional Group Interconversion** (FGI) pattern
- The diazonium group `N=[N+]=[N-]` is a distinct functional group, NOT an amine

### How to Identify Diazotization Pattern
```
Product: ...[C@H]1N
          |
          Ends with amine (model answer - WRONG!)

Product: ...[C@H]1N=[N+]=[N-]
          |
          Ends with diazonium group (correct target!)

Key pattern:
- Diazotization converts: R-NH2 (amine) → R-N₂⁺ (diazonium salt)
- SMILES for diazonium: N=[N+]=[N-] (linear N≡N⁺)
- The diazonium group has formal charge: -N⁺≡N with negative charge on terminal N
- Note: N=[N+]=[N-] shows the connectivity with charges

Retrosynthetic analysis:
Product has: ...-C-N=[N+]=[N-] (diazonium on carbon)
Precursor: ...-C-N (amine)
Reaction: Diazotization with NaNO2 + HCl

SMILES distinction:
- Amine: N (nitrogen attached to carbon, no explicit charge)
- Diazonium: N=[N+]=[N-] (three nitrogens in a row with charges)

In ID #31:
- Product: ...[C@H]1N=[N+]=[N-] (diazonium on cyclohexane carbon)
- Precursor should be: ...[C@H]1N (amine)
- The diazonium is formed by diazotization of the amine
```

### Step-by-Step Diazotization Retrosynthesis
```
Step 1: Look for diazonium group in product
        Pattern: N=[N+]=[N-]
        Location: Usually at end of carbon chain or attached to ring carbon

Step 2: Identify the carbon bearing the diazonium
        The diazonium is attached to: ...[C@H]1N=[N+]=[N-]
        The carbon [C@H]1 has the diazonium group

Step 3: Disconnect - the diazonium comes from an amine
        Product: ...[C@H]1-N=[N+]=[N-]
        Precursor: ...[C@H]1-N (amine)

Step 4: Reaction type is FGI (diazotization)
        Forward: R-NH2 + NaNO2 + HCl → R-N₂⁺ Cl⁻ + H2O
        Retro: R-N₂⁺ ← R-NH2 + NaNO2 + HCl

Key indicators for diazotization:
1. Look for N=[N+]=[N-] pattern in product
2. This represents -N≡N⁺ (diazonium group)
3. Precursor has -NH2 (amine) at same position
4. Reaction type is FGI (functional group interconversion)
5. Reagent is typically NaNO2/HCl (nitrous acid generation)

Common mistake:
- Missing the diazonium entirely
- Returning the product unchanged (thinking it's not a reaction)
- Confusing diazonium with azide (N3)

Diazonium vs Azide:
- Diazonium: N=[N+]=[N-] (3 nitrogens, charged)
- Azide: N=[N+]=[N-] (3 nitrogens, same SMILES but different chemistry!)
- Context matters: Diazonium is for diazotization, azide is for Click chemistry
```
