# Quick Reference: Critical Patterns from Training Errors

**These patterns caused errors in training - prioritize checking these!**

---

## 🚨 CRITICAL: Training Error #1 - FGI Amide Formation (ID 46)

**Pattern**: Product has amide → Precursor is ESTER (not carboxylic acid!)

```
WRONG:  Product amide C(=O)N → Precursor: C(=O)O (carboxylic acid)
RIGHT:  Product amide C(=O)N → Precursor: C(=O)OC (methyl ester)
```

**SMILES Distinction**:
```
# WRONG - Carboxylic acid (C(=O)O):
R-C(=O)O  - Carbonyl carbon attached to hydroxyl (OH)
           No additional carbon after the oxygen
           Example: acetic acid: CC(=O)O

# CORRECT - Ester (C(=O)OC):
R-C(=O)OC - Carbonyl carbon attached to alkoxy (OR'')
           Additional carbon AFTER the oxygen
           Example: methyl acetate: CC(=O)OC
```

**How to Check**:
1. Look at the atom AFTER the carbonyl oxygen
2. If it's C (carbon): ESTER ✓
3. If it's end of chain/nothing: CARBOXYLIC ACID ✗

**Example from Training**:
- Product: `...C(=O)Nc4cccnc4C...` (amide)
- Correct Precursor: `...C(=O)OC...` (METHYL ester, not acid!)
- The extra `C` after `O` is critical!

---

## 🚨 CRITICAL: Training Error #2 - FGA Methyl Position (ID 16)

**Pattern**: Methyl group notation in fused heterocycle SMILES

```
WRONG:  Methyl on wrong carbon (missing leading C)
RIGHT:  Cc1c... (methyl CH3 attached to heterocycle carbon 1)
```

**SMILES Distinction**:
```
# CORRECT - Methyl on heterocycle:
Cc1c(CBr)c(-c2ccccc2)nc2cc(Cl)ccc12
|
The leading Cc1 means: methyl (CH3) attached to position 1 of heterocycle

# WRONG - Missing methyl carbon:
c1c(CBr)c(-c2ccccc2)nc2cc(Cl)ccc12
|
No leading C means: hydrogen (H) at position 1, no methyl!
```

**Key Rule**: `Cc1...` = methyl, `c1...` = hydrogen

**Example from Training**:
- Product: `C[C@H](NC(=O)c1c(CBr)c(...))` (methyl is on heterocycle!)
- Correct Precursor: `Cc1c(C)c(-c2ccccc2)nc2cc(Cl)ccc2c1C(=O)N[C@@H](C)C1CCCCC1`
- Note: `Cc1c(...)` shows methyl on heterocycle carbon 1
- NOT: `C[C@H](NC(=O)c1c(C)c(...)` which puts methyl on wrong atom

---

## 🚨 CRITICAL: Training Error #3 - Heterocycle Type (ID 10)

**Pattern**: 1,3,4-Oxadiazole vs N-Alkylated 1,2,4-Triazole

```
WRONG:  Saw C-N bond, assumed N-alkylation of triazole
RIGHT:  Recognized oxadiazole formation from nitrile cyclization
```

**How to Identify 1,3,4-Oxadiazole**:
```
Product: c1ccc(-c2nc(CCCCCCc3nnn[nH]3)oc2-c2ccccc2)cc1
         |
         The "oc" pattern = O-C (oxygen attached to carbon in ring)
         This indicates OXYGEN in the heterocycle = OXADIAZOLE

Look for: c2nc(... )oc2 (oxadiazole ring with O and N)
NOT:     c2ncn[nH]2 (pyrrole/triazole, no O in ring)
```

**Key Distinction**:
```
1,3,4-Oxadiazole:
- Ring: O-C-N-C-N (oxygen and nitrogen adjacent)
- SMILES: c1ncoc1, c1noc[nH]1
- Formation: Nitrile + acyl compound OR cyclization
- Key: OXYGEN in the ring (from carbonyl)

Paal-Knorr Pyrrole:
- Ring: C-C-C-C-N (all carbons except one nitrogen)
- SMILES: c1cc[nH]c1
- Formation: 1,4-Diketone + amine
- Key: NO oxygen in ring

1,2,4-Triazole:
- Ring: C-N-N-C-N (three nitrogens)
- SMILES: c1nnn[nH]1
- Formation: Various (hydrazide + nitrile, etc.)
- Key: THREE nitrogens, no oxygen
```

**Example from Training**:
- Product: `c1ccc(-c2nc(CCCCCCc3nnn[nH]3)oc2-c2ccccc2)cc1`
- Contains: `c2nc(...)oc2` = oxadiazole ring (has O!)
- Correct Precursor: `N#CCCCCCCc1nc(-c2ccccc2)c(-c2ccccc2)o1` (nitrile cyclization)
- LLM Wrong Answer: `BrCCCCCC.c1nnn[nH]1` (N-alkylation of triazole)

---

## Quick Decision Tree

```
Does product have heterocycle?
├─ YES → Does ring have O and N adjacent (oc, co)?
│       ├─ YES → 1,3,4-Oxadiazole (nitrile cyclization)
│       └─ NO → Does ring have three N (nnn)?
│               ├─ YES → 1,2,4-Triazole
│               └─ NO → Check other heterocycles (thiazole, pyrrole, etc.)
└─ NO → Check other reaction types
```

---

## C-C Bond Formation: Suzuki vs Sonogashira

| Feature | Suzuki | Sonogashira |
|---------|--------|-------------|
| Product | No alkyne | Has alkyne (C#C) |
| Partner 1 | `B(O)O` (boronic acid) | `C#C` (terminal alkyne) |
| Partner 2 | Aryl halide | Aryl halide |

**Common Mistake**: Confusing `B(O)O` with `C#C`
- WRONG: Using alkyne for Suzuki
- CORRECT: `c1ccc(B(O)O)cc1` for Suzuki

---

## Thioether Formation (FGA)

**Pattern**: R-S-R' → R-X + R'-SH

**Critical Halide Position**:
- Benzyl chloride: `ClCc1ccccc1` (Cl on CH2, attached to ring)
- NOT: `c1ccc(Cl)cc1` (Cl directly on aromatic carbon)

---

## Ketone Hydrate (FGI)

**Pattern**: Ketone + H2O → Gem-diol

**SMILES Distinction**:
- Ketone: `C(=O)` (carbon with double bond to oxygen)
- Gem-diol: `C(O)` (carbon with two single-bonded oxygens)

**Critical**: Verify which ring carbon has the carbonyl!
- Trace connectivity from attachment point
- Count ring positions carefully

---

## Halide Reactivity Order

```
I > Br > Cl > F (most to least reactive)
```

**For Sonogashira**: Use I or Br, NOT Cl (unless special catalyst)
- WRONG: `Clc1ncncc1` (aryl chloride)
- CORRECT: `Ic1ncncc1` (aryl iodide) or `Brc1ncncc1` (aryl bromide)

---

## Protecting Group Distinction

| Pattern | Meaning | Example |
|---------|---------|---------|
| `OCc1ccccc1` | Benzyl ether | O-CH2-Ph protecting group |
| `OC` | Methyl ether | Simple methyl |
| `OC(=O)c1ccccc1` | Phenol ester | O-C(=O)-Ph (benzoate) |
| `C(=O)OC` | Ester carbonyl | R-C(=O)O-CH3 |
| `C(=O)N` | Amide carbonyl | R-C(=O)NH2 |

---

## SMILES Position Markers

**For multi-substituted rings, numbering matters**:
```
N#Cc1ccc(CBr)cc1Br
├─ Position 1: C#N (attachment)
├─ Positions 2-3: cc
├─ Position 4: CBr
└─ Position 5: Br

NOT equivalent to:
N#Cc1ccc(Br)cc1CBr (different regiochemistry!)
```

---

## Functional Group Abbreviations

| SMILES | Group |
|--------|-------|
| `C#N` | Nitrile |
| `[N+]=[N-]` | Azide |
| `C(=O)OC` | Ester |
| `C(=O)N` | Amide |
| `CS` | Thioether (methyl) |
| `ClCc1ccccc1` | Benzyl chloride |
| `BrCc1ccccc1` | Benzyl bromide |

---

## Common Error Checklist

Before submitting:
- [ ] Is halide on correct atom (benzylic vs aromatic)?
- [ ] Is carbonyl on correct ring carbon?
- [ ] Is carbonyl an ester (C(=O)OC) NOT acid (C(=O)O) for amide formation?
- [ ] Does heterocycle have O (oxadiazole) or not (triazole)?
- [ ] Is methyl group position correct (Cc1... vs c1...)?
- [ ] Are ring numbers consistent?
- [ ] Are parentheses balanced?
- [ ] Does forward reaction make chemical sense?

---

## ✅ Success Patterns (100% Accuracy in Training)

These patterns worked - use as reference:

### 1. Hantzsch Thiazole Synthesis (ID 37 - CORRECT)
```
Product: CCOC(=O)c1sc(C)nc1-c1ccc(C)cc1
Precursors: CC(N)=S.CCOC(=O)C(Br)C(=O)c1ccc(C)cc1

Key: Thioacetamide + α-halo carbonyl → thiazole
     Br is on carbon alpha to carbonyl: C(Br)C(=O)
```

### 2. Acylation - Amide Bond Formation (ID 3 - CORRECT)
```
Product: CN(Cc1cccc(C(=O)N2CC(=O)Nc3ccccc32)c1)C(=O)OC(C)(C)C
Precursors: CN(Cc1cccc(C(=O)O)c1)C(=O)OC(C)(C)C.O=C1CNc2ccccc2N1

Key: Break amide C(=O)-N bond
     Fragment 1: Carboxylic acid C(=O)O
     Fragment 2: Amine (benzimidazolone nitrogen)
```

---

## 🚨 CRITICAL: Training Error #4 - Diazotization (ID 31)

**Pattern**: Amine → Diazonium salt via FGI (diazotization)

```
WRONG:  Return product unchanged (missed diazotization)
RIGHT:  Product has diazonium group N=[N+]=[N-] → Precursor is amine N
```

**SMILES Distinction**:
```
# Diazonium salt:
N=[N+]=[N-]
|
Linear three-nitrogen chain with formal charges
Represents: -N≡N⁺ (diazonium group attached to carbon)

# Amine:
N (in SMILES context)
|
Simple nitrogen attached to carbon (no explicit H shown)
Represents: -NH2 (amine group)

In SMILES notation:
- Product: ...[C@H]1N=[N+]=[N-] (diazonium on carbon)
- Precursor: ...[C@H]1N (amine)
- Reaction: Diazotization with NaNO2 + HCl
```

**How to Identify**:
1. Look for `N=[N+]=[N-]` pattern in product
2. This indicates diazonium group (NOT azide!)
3. Precursor is the amine at the same position
4. Reaction type: FGI (Functional Group Interconversion)

**Key Distinction - Diazonium vs Azide**:
```
Diazonium (diazotization):
- SMILES: N=[N+]=[N-]
- Chemistry: R-NH2 + HNO2 → R-N₂⁺
- Use: Sandmeyer reactions, coupling

Azide (Click chemistry):
- SMILES: N=[N+]=[N-] (same notation!)
- Chemistry: R-X + NaN3 → R-N3
- Use: 1,3-dipolar cycloaddition

Context determines interpretation:
- If reaction type is FGI: diazonium
- If reaction type is FGA: azide
```

**Example from Training**:
- Product: `...C[C@H]1N=[N+]=[N-]` (diazonium on cyclohexane)
- Correct Precursor: `...C[C@H]1N` (amine)
- LLM Wrong Answer: `...C[C@H]1N` (returned amine, missed diazotization!)

---

## 🚨 CRITICAL: Training Error #5 - SMILES Connectivity (ID 44)

**Pattern**: Amino acid derivative connectivity - amine and hydroxyl positions

```
WRONG:  C[C@H](N)[C@H](O) - amine and OH on adjacent chiral carbons
RIGHT:  CC(N)C(O) - amine on one carbon, OH on separate carbon
```

**SMILES Distinction**:
```
# WRONG - Adjacent chiral centers:
C[C@H](N)[C@H](O)
|    |    |
C    N    O
(chiral) (chiral)
Amine and OH are on DIFFERENT carbons but BOTH chiral
The [C@H] before N makes that carbon chiral
The [C@H] before O makes that carbon chiral

# CORRECT - Separate carbons:
CC(N)C(O)
||   ||
C    C
(methyl) (hydroxyl carbon)
Amine on first carbon (CC(N))
Hydroxyl on second carbon (C(O))
Different connectivity!
```

**How to Identify**:
1. Parse the SMILES to identify each carbon
2. CC(N) = methyl with amine (one carbon)
3. C(O) = carbon with hydroxyl (second carbon)
4. These connect as CC(N)C(O), NOT C[C@H](N)[C@H](O)

**Critical Rule**:
- CC(N) = one carbon with amine
- C[C@H](N) = TWO carbons, second one chiral with amine
- Check how many carbons are between functional groups!

**Example from Training**:
- Product: `...C[C@H](NC(C)=O)[C@H](O)[C@H]2...` (adjacent stereocenters)
- Wrong Precursor: `...C[C@H](N)[C@H](O)[C@H]2...` (same structure)
- Correct Precursor: `...CC(N)C(O)[C@H]2...` (different connectivity!)
- The bicyclic system starts at [C@H]2, not at the amine

**Verification**:
- In correct answer, [C@H]2 appears at: `...[C@H]2CO[C@@H]...`
- This is part of the bicyclic sugar system
- The amine CC(N) is separate, on the side chain

---

## 🚨 CRITICAL: Training Error #6 - Heterocycle SMILES Numbering (ID 33)

**Pattern**: N-Alkylated heterocycle - SMILES starting position and ring numbering

```
WRONG:  COC(=O)c1c(C=O)c(C)c(C)[nH]1 (ester on wrong ring position)
RIGHT:  COC(=O)c1[nH]c(C)c(C)c1C=O (ester on correct carbon, numbering matches)
```

**SMILES Distinction**:
```
# WRONG - Wrong starting position:
COC(=O)c1c(C=O)c(C)c(C)[nH]1
├─ Ring starts at c1 (carbon 1)
├─ Position 1: c1 (carbon with ester COC(=O))
├─ Position 2: c(C=O) (carbon with aldehyde)
├─ Position 3: c(C) (methyl)
├─ Position 4: c(C) (methyl)
└─ Position 5: [nH]1 (nitrogen closes ring)

This represents the ester attached to carbon 1, aldehyde on carbon 2.

# CORRECT - Correct starting position:
COC(=O)c1[nH]c(C)c(C)c1C=O
├─ Ring starts at c1 (carbon 1)
├─ Position 1: c1 (carbon with ester COC(=O))
├─ Position 2: [nH] (nitrogen)
├─ Position 3: c(C) (methyl)
├─ Position 4: c(C) (methyl)
└─ Position 5: c1C=O (aldehyde closes to carbon 1)

This represents the ester attached to carbon 1, aldehyde closes to carbon 1.
```

**Key Issue - Ring Connectivity**:
```
Product: COC(=O)c1c(C=O)c(C)c(C)n1CC=C(Cl)Cl
         |
         The ring connectivity is: C1-C2-C3-C4-C5-N1
         - Carbon 1: Has ester (COC(=O))
         - Carbon 2: Has aldehyde (C=O)
         - Carbon 3: Has methyl
         - Carbon 4: Has methyl
         - Carbon 5: Is nitrogen, attached to allylic chloride

In LLM wrong answer:
- COC(=O)c1c(C=O)c(C)c(C)[nH]1
- This implies aldehyde is on carbon 2, not closing back to carbon 1

In correct answer:
- COC(=O)c1[nH]c(C)c(C)c1C=O
- This has nitrogen at position 2, aldehyde closes to position 1
- The numbering convention matches the expected answer format
```

**How to Identify Correct Numbering**:
1. Trace the ring from the attachment point (where COC(=O) attaches)
2. Follow the ring path to identify each atom's position
3. Ensure the closing atom (with ring number) matches the actual connectivity
4. The carbonyl (aldehyde) should close to the carbon with the ester

**Critical Rule**:
- In SMILES, `c1[...]c1X` means X closes to position 1
- `c1[...]c2...c2` means second carbon closes to position 2
- Match the ring closure number to the actual atom position!

**Example from Training**:
- Product: `COC(=O)c1c(C=O)c(C)c(C)n1CC=C(Cl)Cl` (5-membered heterocycle)
- Wrong Precursor: `COC(=O)c1c(C=O)c(C)c(C)[nH]1.ClCC=C(Cl)Cl`
- Correct Precursor: `COC(=O)c1[nH]c(C)c(C)c1C=O.ClCC=C(Cl)Cl`
- The heterocycle is numbered starting from the carbon with ester
- The aldehyde (C=O) closes back to that same carbon
- The nitrogen is at position 2 in the ring (adjacent to attachment point)

**Verification**:
- Product has: ring with ester at position 1, aldehyde at position 2 (relative)
- Precursor should mirror this connectivity
- The `c1[...]c1C=O` pattern shows aldehyde closing to carbon 1
- NOT `c1c(C=O)...` which puts aldehyde as a substituent

---

## ✅ SMILES Canonicalization Equivalence (ID 18 - CORRECT prediction!)

**Pattern**: Different SMILES notations for the same chemical structure are EQUIVALENT

```
# These are SEMANTICALLY EQUIVALENT nitro group notations:

[N+](=O)[O-]c1cccc2c(Cl)nccc12
        |
        Nitro group with N+ and two O atoms

O=[N+]([O-])c1cccc2c(Cl)nccc12
        |
        Same nitro group, different notation order
```

**Key Point**: If your reasoning is chemically correct, different SMILES notation is NOT an error!

**When checking correctness**:
1. Is the chemical reasoning correct? (e.g., nitro→amine reduction)
2. Does the SMILES represent the right functional groups?
3. Are all atoms and bonds in the right places?

If all are YES, the prediction is correct even if notation differs.

**Example from Training (ID 18)**:
- Model answer: `[N+](=O)[O-]c1cccc2c(Cl)nccc12` (nitro compound)
- Target: `O=[N+]([O-])c1cccc2c(Cl)nccc12` (same nitro compound)
- Reasoning: Correctly identified nitro→amine reduction
- Result: ✅ This prediction is CORRECT (not an error!)

---

## ✅ Stereochemistry Notation Variations (ID 48 - CORRECT prediction!)

**Pattern**: `/` and `\` in SMILES indicate alkene stereochemistry, but different notations can represent the same structure

```
# These can represent the same alkene geometry:

/C=C(/OC)    vs    \C(=C\C(=O)OC)
|  |  |              |  |  |
/  =  /              \  =  /
```

**Key Points**:
1. `/` and `\` are directional markers for E/Z stereochemistry
2. Different notations can represent chemically identical structures
3. The underlying connectivity is what matters, not the slash direction

**When checking correctness**:
1. Is the carbon skeleton correct?
2. Are the functional groups in the right places?
3. Is the bromination position correct (allylic vs terminal)?
4. Is the reagent correct (NBS)?

If all are YES, the prediction is correct even if stereochemical notation differs.

**Example from Training (ID 48)**:
- Model answer: `COC(=O)/C=C(/OC)C(C).O=C1CCC(=O)N1Br`
  - Alkene with ester and methoxy substituents
  - Allylic bromination (C(C)Br next to C=C)
  - NBS reagent
- Target: `CC/C(=C\C(=O)OC)OC.O=C1CCC(=O)N1Br`
  - Same structure, different stereochemical notation
  - Same NBS reagent
- Reasoning: Correctly identified allylic bromination pattern
- Result: ✅ This prediction is CORRECT (not an error!)

**Critical Check**: Focus on CONNECTIVITY and FUNCTIONAL GROUPS, not just stereochemical notation!

---

## 🚨 CRITICAL: Phenol vs Ketone + Benzyl vs Alkyl Halide (ID 5 - REAL ERROR)

**Pattern**: Williamson ether synthesis requires PHENOL (Ar-OH) and BENZYL BROMIDE (CBr on ring)

```
WRONG:  c(=O)           = Ketone carbonyl (Ar-C=O)
RIGHT:  O (on aromatic) = Phenol hydroxyl (Ar-OH)

WRONG:  CCOC(C)CBr      = Bromide on alkyl chain
RIGHT:  c1ccc(CBr)cc1   = Benzyl bromide (CBr attached to aromatic ring)
```

**SMILES Distinction**:

```
# Ketone on aromatic (NOT a phenol):
c(=O)   - Aromatic carbon with carbonyl double bond (C=O)
         Example: c2cnn(C(C)(C)C)c(=O)c2Cl
         The (=O) indicates carbonyl oxygen attached to aromatic carbon

# Phenol (hydroxy on aromatic) - CORRECT nucleophile for ether formation:
O       - Hydroxyl group attached to aromatic ring
         Example: CC(C)(C)n1ncc(O)c(Cl)c1=O
         The "O" at end of aromatic chain is phenolic oxygen

# Benzyl bromide (bromine on CH2 attached to aromatic):
CBr     - CH2-Br attached to aromatic ring
         Example: c1ccc(CBr)cc1
         The CBr is the benzylic position (reactive for SN2)

# Alkyl bromide (bromine on terminal carbon):
BrC     - Bromine attached to end of alkyl chain
         Example: CCCBr
         Less reactive, wrong position for benzyl ether synthesis
```

**Example from Training (ID 5)**:

Product: `CCOC(C)COc1ccc(COc2cnn(C(C)(C)C)c(=O)c2Cl)cc1`
         |
         Ether bond: -O- connecting ethoxy chain to benzyl position

Model WRONG Answer: `CCOC(C)CBr.Oc1ccc(COc2cnn(C(C)(C)C)c(=O)c2Cl)cc1`
                    |
                    1. Used alkyl bromide (CBr on ethoxy chain)
                    2. Kept carbonyl `c(=O)` as if it were phenol

Model CORRECT Answer: `CC(C)(C)n1ncc(O)c(Cl)c1=O.CCOC(C)COc1ccc(CBr)cc1`
                      |
                      1. Phenol: `CC(C)(C)n1ncc(O)c(Cl)c1=O` (O is hydroxyl!)
                      2. Benzyl bromide: `CCOC(C)COc1ccc(CBr)cc1` (CBr on aromatic ring!)

**Verification Checklist**:
- [ ] Is the nucleophile a phenol (Ar-OH) with `O` on aromatic, NOT a ketone (Ar-C=O)?
- [ ] Is the halide a benzyl bromide (CBr on aromatic ring) for SN2, NOT alkyl bromide?
- [ ] Does the ether disconnect at the benzyl position (Ar-O-CH2-Ar)?
- [ ] Are all substituents preserved correctly?
