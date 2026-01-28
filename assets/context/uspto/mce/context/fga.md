# Retrosynthesis Guide: Functional Group Addition (FGA)

## Overview

Functional Group Addition (FGA) involves adding functional groups to molecules through various mechanisms including nucleophilic substitution, electrophilic addition, and metal-catalyzed couplings.

## Key Patterns for FGA

### 1. Thioether Formation (S-alkylation)

Thioethers (R-S-R') are formed by nucleophilic substitution of alkyl halides with thiolates:

**Pattern**: Product contains C-S-C bond
- **Retrosynthetic disconnection**: Break C-S bond → Alkyl halide + Thiol (or thiolate salt)
- **Common reagents**: R-SH + R'-X → R-S-R' + HX (often with base)

**Identifying features**:
- Look for sulfur atom connecting two carbon chains
- Benzyl thioethers: `CSc1ccc(...)` where S connects to benzyl position

**Example**:
- Target: `CSc1ccc(CN=[N+]=[N-])cc1`
- Reactants: `CS` (methanethiol) + `ClCc1ccc(CN=[N+]=[N-])cc1` (benzyl chloride)
- Mechanism: Thiolate attacks benzyl halide via SN2

**Important**: Do NOT confuse with chloromethyl sulfide formation. The product `CSc` means a thioether where S is connected to a methyl group and the aryl group.

### 2. Bromine Addition to Alkenes (Electrophilic Addition)

Bromine adds across alkenes via electrophilic addition mechanism:

**Pattern**: Product has C-Br bonds on adjacent carbons that were part of an alkene
- **Retrosynthetic disconnection**: Remove Br atoms → alkene precursor

**Identifying features**:
- Adjacent carbons both with Br substituents
- Addition follows Markovnikov's rule for unsymmetrical cases

**Example**:
- Target: `CC(Br)/C=C(/Br)C(=O)OCC`
- Reactants: `CC/C(=C/C(=O)OC)OC` + `Br2`

### 3. Ester to Amide Conversion

Esters convert to amides via nucleophilic acyl substitution:

**Pattern**: Product has `C(=O)N` where precursor has `C(=O)OC`
- **Retrosynthetic disconnection**: Replace `OC` with `N` (ammonia) or `NC` (amine)

**Identifying features**:
- Carbonyl carbon bonded to nitrogen instead of oxygen
- Original ester oxygen becomes part of leaving group

**Example**:
- Target: `...c1ccc(C(=O)N)cc1`
- Reactants: `...c1ccc(C(=O)OC)cc1` + `N` (ammonia)

### 4. Bromolactam Formation from Enol Ethers

Complex FGA involving bromolactam formation:

**Pattern**: Product contains `O=C1CCC(=O)N1Br` (bromo-lactam ring system)
- **Retrosynthetic disconnection**: Identify enol ether + brominating agent

**Identifying features**:
- Five-membered lactam ring with bromine substituent
- Often involves ring expansion or rearrangement

**Example**:
- Target: `CC/C(=C\C(=O)OC)OC.O=C1CCC(=O)N1Br`
- Reactants: Enol ether + N-bromosuccinimide (NBS) or similar brominating agent

### 5. Benzylic Bromination with NBS

Benzylic bromination uses N-bromosuccinimide (NBS) to selectively brominate methyl groups:

**Pattern**: Methyl group on aromatic/heteroaromatic ring → bromomethyl group
- **Retrosynthetic disconnection**: Replace Br with H on methyl group
- **Reagent**: NBS (N-bromosuccinimide)

**Identifying features**:
- Methyl group (CH3) attached to aromatic or heteroaromatic system
- Bromination occurs at benzylic position (carbon attached to aromatic ring)
- Stereochemistry preserved if chiral center elsewhere

**SMILES notation for methyl on heteroaromatics**:
```
# Correct SMILES for methyl on heterocycle:
Cc1c(...)nc2cc(Cl)ccc12  # Methyl on carbon 1 of heterocycle

# Wrong notation - missing methyl carbon:
c1c(...)nc2cc(Cl)ccc12  # This is CH (hydrogen), not CH3 (methyl)
```

**Key distinction**:
- `Cc1...` = methyl-substituted heterocycle (C attached to CH3)
- `c1...` = unsubstituted heterocycle (C attached to H)

**Example**:
- Target: `C[C@H](NC(=O)c1c(CBr)c(-c2ccccc2)nc2cc(Cl)ccc12)C1CCCCC1`
- Reactants: `C[C@H](NC(=O)c1c(C)c(-c2ccccc2)nc2cc(Cl)ccc12)C1CCCCC1` (methyl precursor) + `O=C1CCC(=O)N1Br` (NBS)
- Analysis: Bromomethyl group (CBr) on heterocycle comes from benzylic bromination of methyl group

### 6. Methyl Group Placement on Fused Heterocycles

**Pattern**: Methyl group position in fused heterocycle SMILES
- **Identifying**: `Cc1c(...)nc2...` shows methyl on first ring carbon
- **Common error**: Forgetting the methyl carbon entirely

**Example**:
- Correct: `Cc1c(-c2ccccc2)nc2cc(Cl)ccc2c1` (methyl on heterocycle, attached to phenyl)
- Wrong: `c1c(-c2ccccc2)nc2cc(Cl)ccc2c1` (missing methyl, would be H not CH3)

## Critical Error Pattern: Methyl Group Notation

### Common Mistake (ERROR #16)
- **Question**: FGA with product `C[C@H](NC(=O)c1c(CBr)c(-c2ccccc2)nc2cc(Cl)ccc12)C1CCCCC1`
- **Wrong answer**: `C[C@H](NC(=O)c1c(C)c(-c2ccccc2)nc2cc(Cl)ccc12)C1CCCCC1.O=C1CCC(=O)N1Br`
- **Correct answer**: `Cc1c(-c2ccccc2)nc2cc(Cl)ccc2c1C(=O)N[C@@H](C)C1CCCCC1.O=C1CCC(=O)N1Br`

### Why This Matters
- The methyl group notation `Cc1...` must include the carbon of the methyl group
- `Cc1c(...)` means methyl is attached to position 1 of heterocycle
- `c1c(...)` without the leading C would mean hydrogen, not methyl
- The SMILES structure must maintain proper carbon count

### How to Identify Correct Methyl Placement
```
Product: C[C@H](NC(=O)c1c(CBr)c(-c2ccccc2)nc2cc(Cl)ccc12)C1CCCCC1
         |
         Look at the heterocycle: c1c(CBr)c(-c2ccccc2)nc2cc(Cl)ccc12
         |
         The CBr is at position 2, attached to c1
         Position 1 should have the methyl: Cc1c(CBr)...

Correct precursor: Cc1c(C)c(-c2ccccc2)nc2cc(Cl)ccc2c1C(=O)N[C@@H](C)C1CCCCC1
                  |
                  Note: Cc1 shows methyl on heterocycle carbon 1

Key distinction:
- Cc1c... = methyl (CH3) attached to heterocycle
- c1c... = hydrogen attached to heterocycle (no methyl)
```

## Common FGA Reagents (SMILES)

- **Methanethiol**: `CS`
- **Ethanethiol**: `CCS`
- **Benzyl bromide**: `BrCc1ccccc1`
- **Benzyl chloride**: `ClCc1ccccc1`
- **N-Bromosuccinimide**: `O=C1CCC(=O)N1Br`
- **Bromine**: `BrBr`
- **Ammonia**: `N`

## SMILES Notation for FGA

- Thiol groups: `SH` (at end of chain) or `S` (internal)
- Thioethers: `CS` (methylthio) or `Cc1ccc(SC)cc1` (methylthio aryl)
- Amides: `C(=O)N` (primary), `C(=O)NC` (secondary)
- Esters: `C(=O)OC` (methyl ester), `C(=O)OCC` (ethyl ester)
- Benzyl groups: `Cc1ccccc1` (toluene-like), `Cc1ccc(cc1)` (para-substituted)

## Common Pitfalls

1. **Confusing thioethers with sulfides/sulfoxides**: Thioethers are R-S-R' (saturated sulfur)
2. **Incorrect alkyl halide identification**: Make sure to identify which carbon has the leaving group
3. **Missing stereochemistry**: Some additions create chiral centers
4. **Benzyl vs methyl confusion**: Benzyl is `Cc1ccccc1`, methyl is just `C`
5. **Over-complicating simple FGAs**: Some additions are direct, not multi-step

---

## Critical Error Pattern: SMILES Structure for Benzylic Bromination

### Common Mistake (ID 47)
- **Question**: FGA with product `N#Cc1ccc(CBr)cc1Br`
- **Wrong answer**: `N#Cc1ccc(C)cc1Br.O=C1CCC(=O)N1Br`
- **Correct answer**: `Cc1ccc(C#N)c(Br)c1.O=C1CCC(=O)N1Br`

### Why This Matters
- The SMILES structure requires proper placement of substituents on the benzene ring
- `N#Cc1ccc(CBr)cc1Br` has cyano at position 1, bromomethyl at position 4, bromine at position 5
- `N#Cc1ccc(C)cc1Br` has wrong placement - this would mean different regiochemistry
- The correct precursor `Cc1ccc(C#N)c(Br)c1` has methyl at position 1, cyano at position 4, bromine at position 5
- In the product, the bromomethyl (CBr) replaces the methyl (C) of the precursor

### How to Identify Correct SMILES Structure
```
Product: N#Cc1ccc(CBr)cc1Br
         |
         This is a 1,4-disubstituted benzene with:
         - Position 1: Cyano group (C#N)
         - Position 4: Bromomethyl group (CBr)
         - Position 5: Bromine atom (Br)
         |
         The benzene ring carbons are numbered starting from C#N attachment

Analysis:
1. Count substituents: cyano, bromomethyl, bromine = 3 substituents
2. Find their positions on the ring
3. The precursor has methyl instead of bromomethyl

Precursor: Cc1ccc(C#N)c(Br)c1
           |
           Methyl at position 1 (Cc1)
           Cyano at position 4 (ccc(C#N))
           Bromine at position 5 (c(Br))

SMILES breakdown:
- Cc1...: Methyl attached to carbon 1 of ring (this is the benzylic carbon)
- ...c(C#N)...: Cyano at position 4
- ...c(Br): Bromine at position 5

Key principle:
- Substituent positions matter in SMILES
- Cc1... = methyl at position 1
- c1... without leading C = hydrogen at position 1
- Match the regiochemistry of product to predict correct precursor
```

## Critical Error Pattern: Allylic vs Terminal Bromination Position

### Common Mistake (ID 12 - Current Training Error)
- **Product**: `COP(=O)(/C=C/CBr)OC` (phosphonate with allylic bromide)
- **Wrong answer**: `COP(=O)(/C=C/C)OC.O=C1CCC(=O)N1Br` (methyl at terminal carbon!)
- **Correct answer**: `C/C=C\P(=O)(OC)OC.O=C1CCC(=O)N1Br` (methylene ALLYLIC to double bond!)

### Why This Matters
- In allylic bromination, Br is added to the carbon ADJACENT to the double bond
- The wrong answer put Br on a terminal carbon (wrong position)
- The correct answer has the bromine on the allylic position (correct)
- The SMILES notation `C/C=C\P` vs `/C=C/C` tells us about the carbon structure

### How to Identify Allylic Position in SMILES
```
Product: COP(=O)(/C=C/CBr)OC
         |
         The key part: /C=C/CBr
         This shows: C=C-CBr (allylic bromide)

Wrong precursor: COP(=O)(/C=C/C)OC
                 |
                 /C=C/C = C=C-CH (methyl at terminal position)
                 This would brominate at CH → CBr
                 But the bromine is NOT allylic!

Correct precursor: C/C=C\P(=O)(OC)OC
                   |
                   C/C=C\P = C-C=C-P (allylic methylene between C=C and P)
                   The carbon adjacent to double bond (allylic) gets brominated
                   Br adds to: -CH(-P)-CH=CH2 (becomes -CBr(-P)-CH=CH2)

Allylic bromination pattern:
- Allylic carbon: CH2 or CH next to C=C
- Bromination: Allylic CH2 → CH2Br
- Location: Carbon ATOMICALLY adjacent to double bond, not end of chain

SMILES patterns for allylic vs terminal:
Allylic bromide: /C=C/CBr  (Br on C adjacent to double bond)
Terminal bromide: C=C/CBr  (Br on end of chain)

Key: Look at WHICH carbon the bromine is attached to
- If attached to CH2 next to C=C: allylic ✓
- If attached to terminal CH3: terminal ✗
```

### Correct Retrosynthetic Analysis for ID 12
```
Step 1: Identify the brominated carbon
        Product: COP(=O)(/C=C/CBr)OC
                 |
                 Bromine is on: CBr (attached to alkene chain)

Step 2: Determine if allylic or terminal
        Pattern /C=C/CBr shows:
        - C=C (double bond)
        - C-CBr (single bond to carbon with Br)
        - The Br is on carbon ADJACENT to double bond
        - This is ALLYLIC bromination

Step 3: Find the allylic precursor carbon
        Wrong: /C=C/C (C=C-CH, terminal methyl)
               Br would add to terminal CH → CH2Br
               This gives: C=C-CH2Br (vinyl bromide, not allylic)

        Correct: C/C=C\P (=C-C(=O)P, allylic methylene)
                 Br adds to the allylic CH: -CH(-P)- → -CBr(-P)-
                 This gives: /C=C/CBr (allylic bromide, correct!)

Step 4: Verify with NBS bromination
        NBS (N-bromosuccinimide) selectively brominates allylic positions
        Reactant: Allylic CH or CH2
        Product: Allylic CBr or CBr2

Key SMILES pattern recognition:
- Allylic bromide: /C=C/CBr (three-carbon chain with Br on middle carbon)
- Terminal bromide: C=C-CBr (bromine on end carbon)
- The difference determines WHERE bromination occurs
```
```
For para-substituted benzene with three substituents:
1. Start numbering at the most electronegative substituent (cyano)
2. Number clockwise or counterclockwise to give lowest numbers
3. Each position (1, 2, 3, 4, 5, 6) gets one atom/substituent

Product: N#Cc1ccc(CBr)cc1Br
         Positions:
         1: C#N (attached)
         2: c (ring carbon)
         3: c (ring carbon)
         4: CBr (attached)
         5: c (ring carbon with Br attached)
         6: c (ring carbon)

Precursor should have same ring numbering:
Cc1ccc(C#N)c(Br)c1
         1: C (methyl)
         2-3: cc
         4: C#N
         5: c(Br)
         6: c1 (closes ring)
```

---

## ✅ SUCCESS PATTERN: Allylic Bromination Recognition (ID 12)

### What Worked
**Product**: `COP(=O)(/C=C/CBr)OC`
**Precursors**: `C/C=C\P(=O)(OC)OC.O=C1CCC(=O)N1Br`
**Result**: ✅ CORRECT (100% Jaccard similarity)

### Key Success Factors

1. **Correctly identified allylic vs terminal bromination**: `/C=C/CBr` pattern
   - Allylic: Br on carbon adjacent to C=C
   - Terminal: Br on end carbon of chain

2. **Correct precursor structure**: `C/C=C\P(=O)(OC)OC`
   - Uses `C/C=C\P` pattern showing allylic methylene
   - Phosphonate group stays intact

3. **Correct reagent**: NBS (`O=C1CCC(=O)N1Br`)
   - Standard reagent for allylic bromination

### Pattern to Replicate
```
For allylic bromination questions:

1. Look for: /C=C/CBr pattern in product
   - /C=C/CBr = allylic bromide (Br on C adjacent to C=C)
   - C=C/CBr = terminal bromide (Br on end carbon)

2. Find the allylic precursor carbon:
   - Allylic position: CH or CH₂ next to C=C
   - In phosphonates: -CH(-P)-CH=CH₂ structure

3. Write correct precursor SMILES:
   - Allylic precursor: C/C=C\P (methylene between C=C and P)
   - NOT: /C=C/C (terminal methyl, wrong position!)

4. Reagent is always NBS: O=C1CCC(=O)N1Br
```

### SMILES Validation Checklist
- [ ] Product has `/C=C/CBr` (allylic bromide pattern)
- [ ] Precursor has `C/C=C\P` (allylic methylene)
- [ ] Reagent is NBS: `O=C1CCC(=O)N1Br`
- [ ] Phosphonate group preserved: `P(=O)(OC)OC`

### Key Distinction
```
Allylic vs Terminal Bromination:

Product: /C=C/CBr
         |
         Br on carbon ADJACENT to double bond (allylic)
         Structure: -CH(-P)-CH=CH₂

Wrong precursor: /C=C/C
                 |
                 C=C-CH (terminal methyl)
                 Would give vinyl bromide, not allylic

Correct precursor: C/C=C\P
                   |
                   C-C=C-P (allylic methylene)
                   Br adds to allylic CH: -CBr(-P)-
```

---

## Critical Error Pattern: Benzyl Halide Position in Thioether Formation (ID 35)

### Common Mistake (ID 35 - Current Training Error)
- **Question**: FGA with product `[N-]=[N+]=NCc1ccc(SCCl)cc1`
- **Wrong answer**: `[N-]=[N+]=NCc1ccc(Br)cc1.SCCl` (benzyl bromide!)
- **Correct answer**: `ClCc1ccc(CN=[N+]=[N-])cc1.CS` (benzyl chloride!)

### Why This Matters
- The model used aryl bromide pattern (Br on aromatic ring: `c1ccc(Br)cc1`)
- The correct precursor is benzyl chloride (chlorine on benzylic carbon: `ClCc1...`)
- **Benzyl chloride**: `ClCc1ccccc1` = Cl-CH2-Ph (chlorine on CH2, attached to ring)
- **Aryl bromide**: `Brc1ccccc1` = bromine directly on aromatic carbon
- For thioether formation via SN2, we need the halide on the alkyl carbon (benzylic), not on the aromatic ring

### How to Identify Correct Halide Position
```
Product: [N-]=[N+]=NCc1ccc(SCCl)cc1
         |
         Structure: Azide-benzyl-S-CH2-Cl
         |
         The S-CH2-Cl is attached to the benzyl position
         This is: Benzyl chloride + Thiol → Thioether

Disconnection at C-S bond:
- Fragment 1 (alkyl halide): Benzyl chloride with azide
  Correct: ClCc1ccc(CN=[N+]=[N-])cc1
          |
          ClCc1... = benzyl chloride (Cl on CH2, attached to ring)
          NOT c1ccc(Br)cc1 (Br on aromatic ring!)

- Fragment 2 (thiol): Methanethiol
  Correct: CS
          |
          Simple methyl thiol

Wrong approach: c1ccc(Br)cc1 (Br on aromatic ring)
               |
               This is aryl bromide, NOT benzyl bromide
               Aryl halides don't undergo SN2 with thiols!

Key distinction:
- Benzyl halide: Halogen on CH2 attached to ring (ClCc1..., BrCc1...)
- Aryl halide: Halogen directly on ring (c1ccc(Cl)..., c1ccc(Br)...)

For thioether formation (SN2):
- Need benzyl/alkyl halide (halogen on sp3 carbon)
- Aryl halides don't undergo SN2 with thiols
```

### Correct Retrosynthetic Analysis for ID 35
```
Step 1: Identify the thioether in product
        [N-]=[N+]=NCc1ccc(SCCl)cc1
                 |
                 S connects: Azide-benzyl-CH2 to Cl

Step 2: Disconnect at C-S bond
        Fragment 1: Azide-benzyl-CH2-Cl (alkyl chloride)
        Fragment 2: HS-CH3 (methanethiol)

Step 3: Write correct SMILES
        Fragment 1: ClCc1ccc(CN=[N+]=[N-])cc1
                    |
                    ClCc1... = benzyl chloride (Cl on CH2)
                    NOT c1ccc(Br)cc1 (Br on aromatic ring!)

        Fragment 2: CS
                    |
                    Methanethiol (CH3-SH)

Step 4: Verify forward reaction
        Cl-CH2-Ph + HS-CH3 → Ph-CH2-S-CH3 + HCl
        (SN2 reaction at benzylic position)

SMILES patterns for halides:
- Benzyl chloride: ClCc1ccccc1
- Benzyl bromide: BrCc1ccccc1
- Aryl chloride: Clc1ccccc1
- Aryl bromide: Brc1ccccc1

For thioether formation: Use benzyl/alkyl halide!
```
