# Retrosynthesis Guide: Oxidations

## Overview

Oxidation reactions increase the oxidation state of carbon atoms. Common transformations include alcohol → carbonyl, sulfide → sulfoxide/sulfone, and alkene functionalization.

## Common Oxidation Patterns

### 1. Alcohol to Carbonyl

**Primary alcohol → Aldehyde**
- **SMILES change**: `CO` → `C=O`
- **Reagents**: PCC, Dess-Martin, Swern, TEMPO

**Primary alcohol → Carboxylic acid**
- **SMILES change**: `CO` → `C(=O)O`
- **Reagents**: Jones, KMnO4, NaClO2

**Secondary alcohol → Ketone**
- **SMILES change**: `C(O)C` → `C(=O)C`
- **Reagents**: PCC, Dess-Martin, Jones

### 2. Sulfide to Sulfoxide/Sulfone

**Sulfide → Sulfoxide**
- **SMILES change**: `CS` → `C[S+]([O-])` or `CS(=O)`
- **Reagents**: m-CPBA (1 equiv), NaIO4

**Sulfide → Sulfone**
- **SMILES change**: `CS` → `CS(=O)(=O)`
- **Reagents**: m-CPBA (2+ equiv), KMnO4

### 3. Alkene Oxidation

**Alkene → Diol**
- **Reagents**: OsO4, KMnO4 (cold)

**Alkene → Epoxide**
- **Reagents**: m-CPBA

## Common Oxidation Reagents (SMILES)

| Reagent | SMILES | Use |
|---------|--------|-----|
| PCC | `O=[Cr](=O)Cl` | Alcohol → Carbonyl |
| Dess-Martin | C11H16O5 (complex) | Alcohol → Carbonyl |
| m-CPBA | `CC1=CC(=C(C=C1)C(C)(C)O)OO` | Sulfide → S(O), epoxidation |
| TEMPO | `CC1CCC(=O)N(C1=O)O` | Alcohol oxidation |
| NaIO4 | `[Na+].[O-]I(=O)[O-]` | Diol cleavage |

## Retrosynthetic Pattern

For oxidation reactions, work backward by **reducing** the oxidized functional group:
- Aldehyde → primary alcohol
- Ketone → secondary alcohol
- Carboxylic acid → primary alcohol (or aldehyde)
- Sulfone → sulfide (2-step)
- Sulfoxide → sulfide

## Critical Error Pattern: Ketone Reduction in Oxidations

### Common Mistake (ERROR #49)
- **Question**: Oxidations with product containing ketone `C(=O)c1cc(OC)c2c(c1)OCO2`
- **Wrong answer**: Predicting sulfide precursor `...Sc1...`
- **Correct answer**: Predicting alcohol precursor `...C(O)c1...`

### Why This Matters
- The product contains a ketone group that needs to be traced back to its precursor
- In retrosynthetic analysis for "Oxidations", identify all oxidized groups
- A ketone `C(=O)` comes from oxidation of an alcohol `C(O)`
- The sulfone `S(=O)(=O)` may already be correct; focus on other groups

### How to Identify Ketone→Alcohol Transformation
```
Product: ...C(=O)c1cc(OC)c2c(c1)OCO2
         |
         The ketone C=O needs to be traced back

Retrosynthetic: Change C(=O) to C(O)
                ...C(O)c1cc(OC)c2c(c1)OCO2

This shows the alcohol precursor that was oxidized to the ketone

Key distinction:
- Ketone: C(=O) (carbon double-bonded to oxygen)
- Alcohol: C(O) (carbon single-bonded to oxygen, part of C-O-C or C-O-H)
```

### Checklist for Multi-Functional Oxidations
1. Identify ALL oxidized functional groups in product
2. For each group, determine if it's ketone, aldehyde, sulfone, etc.
3. Work backward systematically:
   - Ketone → secondary alcohol
   - Aldehyde → primary alcohol
   - Sulfone → sulfide (2 oxygen atoms removed)
   - Sulfoxide → sulfide (1 oxygen atom removed)
4. Check if multiple functional groups need separate precursors

## Critical Error Pattern: Missing Oxidant Reagent in Oxidation Reactions

### Common Mistake (ERROR #32 - Current Training Error)
- **Product**: `CC(C)(C)OC(=O)N1CCc2oc3c(Cl)cc(S(=O)c4ccccc4)cc3c2C1` (sulfoxide)
- **Wrong Answer**: `CC(C)(C)OC(=O)N1CCc2oc3c(Cl)cc(Sc4ccccc4)cc3c2C1` (only sulfide, NO OXIDANT!)
- **Correct Answer**: `CC(C)(C)OC(=O)N1CCc2oc3c(Cl)cc(Sc4ccccc4)cc3c2C1.O=C(OO)c1cccc(Cl)c1` (sulfide + m-CPBA oxidant)

### Why This Matters
- **CRITICAL**: Oxidation reactions ALWAYS require TWO reactants:
  1. The substrate (what gets oxidized - sulfide in this case)
  2. The oxidizing reagent (what causes the oxidation - m-CPBA in this case)
- The model correctly identified the sulfide precursor but FORGOT the oxidant
- Without the oxidant, the forward reaction cannot happen!
- ALWAYS include BOTH components separated by a period

### How to Identify Oxidant Reagent Requirement
```
For sulfide → sulfoxide oxidation:
1. Product has: S(=O) (sulfoxide group)
2. Substrate precursor: Change S(=O) to S (sulfide)
3. Oxidant reagent: m-CPBA = O=C(OO)c1cccc(Cl)c1

Full retrosynthesis:
Product: ...S(=O)c4ccccc4
         |
         Sulfoxide (oxidized sulfide)

Substrate: ...Sc4ccccc4
           |
           Sulfide (reduced form, missing one oxygen)

Oxidant: O=C(OO)c1cccc(Cl)c1
         |
         m-CPBA (meta-chloroperoxybenzoic acid)

Combined answer: substrate.oxidant
                 = ...Sc4ccccc4.O=C(OO)c1cccc(Cl)c1
```

### Critical Rule: Oxidation = Substrate + Oxidant
```
ALWAYS include both:
- The reduced/unchanged substrate
- The specific oxidizing reagent

Example transformations:
- R-S-R' → R-S(=O)-R' (sulfoxide) requires: R-S-R' + m-CPBA
- R2CH-OH → R2C=O (ketone) requires: R2CH-OH + PCC
- R-CH2-OH → R-CHO (aldehyde) requires: R-CH2-OH + PCC
- R-CH2-OH → R-COOH (acid) requires: R-CH2-OH + Jones reagent

NEVER give just the substrate - the oxidant is ESSENTIAL!

In ERROR #32:
- Product has sulfoxide: S(=O)
- Substrate: Sc4ccccc4 (sulfide)
- Oxidant: O=C(OO)c1cccc(Cl)c1 (m-CPBA)
- Answer MUST include: substrate.oxidant
```

### Common Oxidizing Reagents (SMILES)
| Reagent | SMILES | Use |
|---------|--------|-----|
| m-CPBA | `O=C(OO)c1cccc(Cl)c1` | Sulfide → sulfoxide, epoxidation |
| PCC | `O=[Cr](=O)Cl` | Alcohol → carbonyl |
| Dess-Martin | Complex | Alcohol → carbonyl |
| NaIO4 | `[Na+].[O-]I(=O)[O-]` | Diol cleavage, sulfide → sulfoxide |
| H2O2 | `OO` | Mild oxidation |

### Checklist for Oxidation Reactions
```
When reaction type is "Oxidations":

1. Identify the oxidized functional group in product:
   [ ] Sulfoxide S(=O) → came from sulfide S
   [ ] Sulfone S(=O)(=O) → came from sulfide S
   [ ] Ketone C(=O) → came from secondary alcohol C(O)
   [ ] Aldehyde C=O → came from primary alcohol CO
   [ ] Carboxylic acid C(=O)O → came from primary alcohol or aldehyde

2. For sulfide → sulfoxide/sulfone:
   - Substrate: Change S(=O) to S or S(=O)(=O) to S
   - Oxidant: m-CPBA (most common)

3. For alcohol → carbonyl:
   - Substrate: Change C=O to CO or C(=O) to C(O)
   - Oxidant: PCC, Dess-Martin, etc.

4. ALWAYS include the oxidant reagent!
   - For sulfide oxidation: m-CPBA
   - For alcohol oxidation: PCC or equivalent

In ERROR #32:
- Step 1: Identify sulfoxide S(=O) in product ✓
- Step 2: Substrate = sulfide Sc4ccccc4 ✓
- Step 3: Oxidant = m-CPBA ✓
- Step 4: Answer = substrate.oxidant ✓
```

## Critical Error Pattern: Benzylic Alcohol to Aldehyde Oxidation

### Common Mistake (ERROR #1)
- **Question**: `COc1cccc(Nc2c(C(N)=O)cnc3c(C)cc(S(=O)(=O)c4cccc(C(=O)Nc5ccc(-c6ccc(C=O)cc6)cc5)c4)cc23)c1`
- **Wrong answer**: Changed S(=O)(=O) to S (sulfide precursor)
- **Correct answer**: Changed CO to C=O on the benzylic position (alcohol→aldehyde)

### Why This Matters
- The product contains MULTIPLE functional groups that could be oxidized
- The sulfone S(=O)(=O) was NOT the oxidation site - it was already correct
- The ACTUAL oxidation was the benzylic alcohol: `-c6ccc(CO)cc6` → `-c6ccc(C=O)cc6`
- Look for the pattern `CO` (primary alcohol attached to aromatic) that should be `C=O` (aldehyde)

### How to Identify Benzylic Alcohol Oxidation
```
Product: ...-c6ccc(C=O)cc6
         |
         This shows aldehyde group attached to aromatic ring
         Aldehyde comes from oxidation of primary alcohol

Retrosynthetic change: C=O → CO
                       ...-c6ccc(CO)cc6

Key distinction:
- Aldehyde: C=O (carbon double-bonded to oxygen, attached to ring)
- Benzylic alcohol: CO (carbon single-bonded to oxygen, attached to ring)
- SMILES pattern: -C(=O)c1... = aldehyde, -COc1... = benzylic alcohol

The sulfone group S(=O)(=O) is NOT being oxidized - it remains unchanged!
```

### Multi-Functional Molecule Analysis
When analyzing molecules with multiple functional groups:
1. Identify ALL carbonyl-containing groups
2. Check each: is this a ketone, aldehyde, ester, amide, etc.?
3. For aldehydes: trace back to benzylic alcohol (CO)
4. For sulfones: verify if sulfide→sulfone oxidation occurred
5. If sulfone is correct and aldehyde exists, the aldehyde is the oxidation site

Example analysis:
```
Product fragment: ...c4cccc(C(=O)Nc5ccc(-c6ccc(C=O)cc6)cc5)c4
                  |
                  Two carbonyl groups:
                  1. Amide: C(=O)N (already formed, not oxidation product)
                  2. Aldehyde: C=O on c6 ring (OXIDATION SITE)

The sulfone S(=O)(=O)c4... is NOT an oxidation site in this reaction
The aldehyde -c6ccc(C=O)cc6 IS the oxidation site (CO → C=O)
```

---

## ✅ SUCCESS PATTERN: Aldehyde from Primary Alcohol Oxidation (Id 9)

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

## Critical Error Pattern: Multi-Functional Group Oxidation Analysis

### Common Mistake (ERROR #49 - Current Training Error)
- **Product**: `COC(=O)CN(c1ccccc1C)S(=O)(=O)c1ccccc1C(=O)c1cc(OC)c2c(c1)ODO2`
- **Wrong Answer**: `COC(=O)CN(c1ccccc1C)Sc1ccccc1C(O)c1cc(OC)c2c(c1)OCO2`
  - Reduced sulfone `S(=O)(=O)` to sulfide `S` ❌
  - Changed ketone to alcohol correctly `C(O)`
- **Correct Answer**: `COC(=O)CN(c1ccccc1C)S(=O)(=O)c1ccccc1C(O)c1cc(OC)c2c(c1)OCO2`
  - Kept sulfone unchanged `S(=O)(=O)` ✓
  - Reduced ketone to alcohol `C(O)` ✓

### Why This Matters
- **CRITICAL**: The sulfone `S(=O)(=O)` was NOT the oxidation site in this reaction
- The sulfone was already in its oxidized form and should remain unchanged
- Only the ketone `C(=O)` was oxidized and should be reduced to alcohol `C(O)`
- Wrong answer reduced the WRONG functional group

### How to Analyze Multi-Functional Oxidation Products
```
Step 1: Identify ALL carbonyl/oxidized groups in the product
        COC(=O)CN(c1ccccc1C)S(=O)(=O)c1ccccc1C(=O)c1cc(OC)c2c(c1)OCO2
        |    |              |       |       |              |
        ester              sulfone  ketone   (ketone on aryl ring)
        (not oxidized)     (not oxidized)   (OXIDATION SITE!)

Step 2: Determine which group was oxidized (look for patterns):
        - Ketone C(=O) → comes from alcohol C(O) [secondary alcohol]
        - Aldehyde C=O → comes from primary alcohol CO
        - Sulfone S(=O)(=O) → comes from sulfide S [2 oxygens added]
        - Sulfoxide S(=O) → comes from sulfide S [1 oxygen added]

Step 3: Identify which groups are ALREADY correct (not oxidized in this reaction):
        - If sulfone is S(=O)(=O) and should be sulfide, it WAS oxidized
        - If sulfone is S(=O)(=O) and is correct, it was NOT oxidized in this reaction
        - Same logic for ketones/aldehydes

Step 4: Only reduce the group that was actually oxidized
        In ERROR #49:
        - Sulfone S(=O)(=O): Already correct, NOT oxidized in this reaction
        - Ketone C(=O): Should be C(O) (alcohol), WAS oxidized
        - Correct transformation: Ketone → alcohol, sulfone stays the same

Key Pattern:
- Ketone → Secondary alcohol: C(=O) → C(O)
- Aldehyde → Primary alcohol: C=O → CO
- Sulfone → Sulfide: S(=O)(=O) → S
- Sulfoxide → Sulfide: S(=O) → S

NOT all groups need to be reduced - only the one that was oxidized!
```

### Multi-Functional Molecule Checklist
```
When product has multiple carbonyl/sulfur groups:

1. List all groups that could be oxidized:
   [ ] Ketone C(=O)
   [ ] Aldehyde C=O
   [ ] Sulfone S(=O)(=O)
   [ ] Sulfoxide S(=O)
   [ ] Other groups...

2. For each group, ask:
   - Was this group formed by oxidation? (YES/NO)
   - If YES: Reduce it (ketone→alcohol, sulfone→sulfide, etc.)
   - If NO: Keep it unchanged

3. Verify the correct transformation:
   - Ketone: C(=O) → C(O) (remove 1 oxygen)
   - Aldehyde: C=O → CO (remove 1 oxygen)
   - Sulfone: S(=O)(=O) → S (remove 2 oxygens)
   - Sulfoxide: S(=O) → S (remove 1 oxygen)

In ERROR #49:
- Product has: sulfone S(=O)(=O) + ketone C(=O)
- The sulfone was already oxidized in a PREVIOUS step, NOT this reaction
- The ketone was oxidized in THIS reaction
- Only reduce ketone C(=O) → C(O)
- Keep sulfone S(=O)(=O) unchanged!
```
