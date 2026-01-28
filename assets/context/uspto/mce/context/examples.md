# Retrosynthesis Examples by Reaction Type

## Deprotection Examples

### Example 1: Benzyl Ether Deprotection (Phenol)

**Target**: `O=C(NCC(=O)N1CCN(C(=O)c2ccccc2C(F)(F)F)CC1)c1ccc(-c2ccccc2O)cc1`

**Analysis**:
- The product has a free phenol group: `-c2ccccc2O`
- Reaction type: Deprotections
- This phenol was protected as a benzyl ether
- Benzyl ether SMILES pattern: `OCc1ccccc1`

**Precursor**: `O=C(NCC(=O)N1CCN(C(=O)c2ccccc2C(F)(F)F)CC1)c1ccc(-c2ccccc2OCc2ccccc2)cc1`

**Key insight**: The phenol is protected as BENZYL ETHER (`OCc1ccccc1`), not methyl ether (`OC`). The benzyl protecting group has the ring structure `c1ccccc1`.

**Forward reaction**: Hydrogenolysis with H2/Pd removes the benzyl group, revealing the phenol.

---

## FGA Examples

### Example 1: Thioether Formation

**Target**: `CSc1ccc(CN=[N+]=[N-])cc1`

**Analysis**:
- Product contains thioether: `C-S-aryl` bond
- Thioethers are formed by alkylation of thiols
- Pattern: R-S-R' comes from R-X + R'-SH (or salt)

**Precursor**: `CS + ClCc1ccc(CN=[N+]=[N-])cc1`

**Key insight**: The thioether is formed from methanethiol (`CS`) and a benzyl chloride derivative. The SMILES `CSc1...` means the sulfur connects a methyl group to the aryl ring.

**Forward reaction**: Thiolate attacks benzyl halide via SN2 mechanism.

---

### Example 2: Ester to Amide Conversion

**Target**: `CCNc1nccc2c1c(C(=O)N)nn2-c1cccc(C#C[C@]2(O)CCN(C)C2=O)c1`

**Analysis**:
- Product has amide: `C(=O)N` attached to heterocycle
- Reaction type: FGI (ester to amide)
- Amide comes from ester + ammonia

**Precursor**: `CCNc1nccc2c1c(C(=O)OC)nn2-c1cccc(C#C[C@]2(O)CCN(C)C2=O)c1.N`

**Key insight**: Replace `OC` (methoxy in ester) with `N` (ammonia). The SMILES `C(=O)OC` → `C(=O)N` shows the transformation.

**Forward reaction**: Ester + ammonia → amide + methanol

---

## Heterocycle Formation Examples

### Example 1: Hantzsch Thiazole Synthesis

**Target**: `CCOC(=O)c1sc(C)nc1-c1ccc(C)cc1`

**Analysis**:
- Product is a thiazole with ester and tolyl substituents
- Thiazole formed via Hantzsch synthesis
- Requires thioamide + α-halo carbonyl

**Components**:
1. **Thioacetamide**: `CC(N)=S` (gives methyl at C2 position)
2. **Ethyl 2-bromo-3-oxo-4-(p-tolyl)butanoate**: `CCOC(=O)C(Br)C(=O)c1ccc(C)cc1`

**Key insight**: The α-halo carbonyl MUST have correct SMILES structure:
- Correct: `CCOC(=O)C(Br)C(=O)` = ethyl 2-bromo-3-oxobutanoate
- Structure: CH3-CH(Br)-C(=O)-O-CH2-CH3
- The bromine is at position 2 (alpha to the ester carbonyl)

**Precursor**: `CC(N)=S.CCOC(=O)C(Br)C(=O)c1ccc(C)cc1`

**Forward reaction**: Hantzsch thiazole synthesis - condensation of thioamide with α-halo carbonyl.

---

## FGI Examples

### Example 1: Ester to Amide

**Target**: `...C(=O)N...` (amide attached to molecule)

**Analysis**:
- Carbonyl carbon bonded to nitrogen (amide)
- Precursor has carbonyl bonded to oxygen (ester)
- Transformation requires ammonia

**Precursor**: `...C(=O)OC... + N`

**Key SMILES patterns**:
- Ester: `C(=O)OC` (methyl ester)
- Amide: `C(=O)N` (primary amide)
- Ammonia: `N`

**Forward reaction**: Nucleophilic acyl substitution with ammonia.

---

## Common Mistakes Analysis

### Mistake 1: Benzyl vs Methyl Ether

**WRONG**: Predicting `-c2ccccc2OC` (methyl ether) for a deprotection

**CORRECT**: `-c2ccccc2OCc2ccccc2` (benzyl ether)

**Why**: Benzyl protecting group has the benzene ring attached: `O-CH2-Ph` = `OCc1ccccc1`

---

### Mistake 2: Wrong Thioether Precursor

**WRONG**: `NCCc1ccc(SH)cc1.ClCCl` (trying to add SCCl group)

**CORRECT**: `CS + ClCc1ccc(...)cc1` (alkyl halide + thiol)

**Why**: Thioethers form by SN2 of thiolate on alkyl halide, not by adding chloromethyl sulfide

---

### Mistake 3: Malformed α-Halo Carbonyl SMILES

**WRONG**: `BrC(C(=O)OCC)=O` (incorrect structure)

**CORRECT**: `CCOC(=O)C(Br)C(=O)` (ethyl 2-bromo-3-oxobutanoate)

**Why**: The SMILES must show the correct connectivity: bromo on carbon alpha to ester

---

### Mistake 4: Missing Ammonia in Ester→Amide

**WRONG**: Only predicting the carboxylic acid, missing ammonia

**CORRECT**: Predict both ester and ammonia as reactants

**Why**: FGI ester→amide requires ammonia as a reactant/reagent

---

## Quick Reference: SMILES for Common Reagents

| Reagent | SMILES | Use |
|---------|--------|-----|
| Methanethiol | `CS` | Thioether formation |
| Thioacetamide | `CC(N)=S` | Hantzsch thiazole |
| Benzyl chloride | `ClCc1ccccc1` | Benzylation |
| NBS | `O=C1CCC(=O)N1Br` | Bromination |
| Ammonia | `N` | Amide formation |
| H2, Pd/C | (reagent, not SMILES) | Benzyl deprotection |
| BBr3 | (reagent, not SMILES) | Methyl ether deprotection |

---

## Error Analysis: Learning from Mistakes

This section documents common prediction errors and how to avoid them.

### ERROR #33: Allylic vs Vinyl Chloride

**Question**: Heteroatom alkylation
- **Product**: `COC(=O)c1c(C=O)c(C)c(C)n1CC=C(Cl)Cl`
- **Wrong**: `ClC=C(Cl)Cl` (vinyl chloride)
- **Correct**: `ClCC=C(Cl)Cl` (allylic chloride)

**Root Cause**: Confused allylic chloride with vinyl chloride

**Analysis**:
- Product has `CC=C(Cl)Cl` attached to nitrogen
- This means: CH2-CH=CCl2 (allylic chain)
- The halide must be `Cl-CH2-CH=CCl2` (allylic chloride)
- `ClC=C(Cl)Cl` would be vinyl chloride (Cl on sp2 carbon)

**SMILES Interpretation**:
```
ClCC=C(Cl)Cl
- Cl attached to CH2 (saturated, allylic position)
- CH2 attached to C=C
- C attached to two Cl atoms

ClC=C(Cl)Cl
- Cl attached directly to sp2 carbon (vinyl)
- No CH2 between Cl and double bond
```

---

### ERROR #49: Ketone vs Sulfide in Multi-Functional Oxidation

**Question**: Oxidations
- **Product**: `COC(=O)CN(c1ccccc1C)S(=O)(=O)c1ccccc1C(=O)c1cc(OC)c2c(c1)OCO2`
- **Wrong**: `COC(=O)CN(c1ccccc1C)Sc1ccccc1C(=O)c1cc(OC)c2c(c1)OCO2` (reduced ketone to sulfide)
- **Correct**: `COC(=O)CN(c1ccccc1C)S(=O)(=O)c1ccccc1C(O)c1cc(OC)c2c(c1)OCO2` (ketone reduced to alcohol)

**Root Cause**: Reduced the wrong functional group

**Analysis**:
- Product has ketone `C(=O)c1cc(OC)c2c(c1)OCO2`
- Wrong answer reduced this to sulfide `Sc1...`
- Correct answer reduces ketone to alcohol `C(O)c1...`
- The sulfone group was already correct

**Key Pattern**:
```
Identify ALL oxidized groups in product:
- Ketone C(=O) → comes from alcohol C(O)
- Sulfone S(=O)(=O) → comes from sulfide S
- Aldehyde C=O → comes from primary alcohol CO

For retrosynthesis, work backward for EACH group:
- Ketone → secondary alcohol
- Aldehyde → primary alcohol
- Sulfone → sulfide (remove 2 oxygens)
```

---

### ERROR #16: Missing Methyl Group in Heterocycle

**Question**: Functional group addition (FGA)
- **Product**: `C[C@H](NC(=O)c1c(CBr)c(-c2ccccc2)nc2cc(Cl)ccc12)C1CCCCC1`
- **Wrong**: `C[C@H](NC(=O)c1c(C)c(-c2ccccc2)nc2cc(Cl)ccc12)C1CCCCC1.O=C1CCC(=O)N1Br`
- **Correct**: `Cc1c(-c2ccccc2)nc2cc(Cl)ccc2c1C(=O)N[C@@H](C)C1CCCCC1.O=C1CCC(=O)N1Br`

**Root Cause**: Wrong SMILES structure for methyl-substituted heterocycle

**Analysis**:
- Wrong answer has methyl on wrong part of molecule
- Correct answer has `Cc1c(...)` showing methyl on heterocycle
- SMILES `Cc1c` = methyl attached to heterocycle carbon 1
- SMILES `c1c` = hydrogen (no methyl)

**Key Pattern**:
```
Methyl on heterocycle: Cc1c(...)nc2cc(Cl)ccc2c1
                       ^
                       This C is the methyl carbon

NOT: c1c(...)nc2cc(Cl)ccc2c1
     ^ No methyl, just hydrogen

Always count carbons: Cc1 means CH3 attached to position 1
```

---

### ERROR #30: Cyclic Ketal Precursor Identification

**Question**: Heterocycle formation
- **Product**: `CC1(COc2ccc(OCc3ccccc3)cc2)CO1`
- **Wrong**: `O=C.O(Cc1ccccc1)c1ccc(O)cc1` (formaldehyde + phenol)
- **Correct**: `C=C(C)COc1ccc(OCc2ccccc2)cc1.O=C(OO)c1cccc(Cl)c1` (enol ether + peracid)

**Root Cause**: Treated as simple acetal instead of cyclic ketal

**Analysis**:
- Product is 1,3-dioxolane (cyclic ketal)
- `CO1...CO1` shows 5-membered ring with two oxygens
- Methyl substituent (CC1) suggests acetone source
- Wrong answer used formaldehyde (would give CH2, not CH3)

**Key Pattern**:
```
Cyclic ketal: CC1(COc2...)CO1
              |
              CC1 = methyl substituent on dioxolane
              CO1 = oxygen closes ring with second oxygen

Cyclic ketal retrosynthesis:
1. Identify ring: 1,3-dioxolane (5-membered)
2. Substituents tell you carbonyl source:
   - CH2 substituent → formaldehyde
   - CC1 (methyl) → acetone
3. Find diol with remaining substituents
4. Peracid or acid catalyst is reagent
```

---

### ERROR #17: Secondary vs Tertiary Amine in Boc Protection

**Question**: Protections
- **Product**: `CC(C)(C)OC(=O)N1Cc2ccc([N+](=O)[O-])cc2C1=O`
- **Wrong**: `O=C1N(Cc2ccc([N+](=O)[O-])cc2)C1.CC(C)(C)OC(=O)OC(=O)OC(C)(C)C`
- **Correct**: `CC(C)(C)OC(=O)OC(=O)OC(C)(C)C.O=C1NCc2ccc([N+](=O)[O-])cc21`

**Root Cause**: Wrong SMILES for secondary amine in lactam

**Analysis**:
- Boc protection requires secondary amine (N-H)
- Wrong answer has tertiary amine: `O=C1N(Cc2...)C1` (N has no H)
- Correct answer has secondary amine: `O=C1NCc2...21` (N has H)
- SMILES `NC` means N-C with N-H; `N(C)` means N without H

**Key Pattern**:
```
Boc protection precursor:
- Must have N-H (secondary amine)
- SMILES: O=C1NCc2ccc([N+](=O)[O-])cc21
          ^N-H shown by NC, not N(C)

NOT tertiary amine:
- SMILES: O=C1N(Cc2...)cc2)C1
          ^N has two carbons, no H

Check nitrogen in SMILES:
- NC... = secondary amine (has H)
- N(C)... = tertiary amine (no H)
```

---

## Summary: Common Error Categories

1. **SMILES Notation Errors**
   - Allylic vs vinyl chloride (`ClCC=C` vs `ClC=C`)
   - Missing methyl carbon (`Cc1c` vs `c1c`)
   - Secondary vs tertiary amine (`NC` vs `N(C)`)

2. **Functional Group Misidentification**
   - Reducing wrong group in multi-functional molecules
   - Confusing acetal types (simple vs cyclic)
   - Missing multiple oxidized groups

3. **Precursor Structure Errors**
   - Wrong carbonyl source for protecting groups
   - Incorrect diol/carbonyl combination
   - Missing reagent in two-component reactions

4. **Retrosynthetic Logic**
   - Working backward from wrong functional group
   - Not considering all substituents
   - Ignoring reaction type context

---

## Current Iteration Errors (iter1_sub4)

### ERROR #28: gem-Diol vs Anhydride Misidentification

**Question**: Functional group interconversion (FGI)
- **Product**: `O=C1C(c2ccc(Br)cc2O)c2ccccc2N1C(c1ccccc1)c1ccccc1`
- **Wrong**: `O=C1OC(=O)c2ccc(Br)cc2O1.CN(c1ccccc1)c1ccccc1`
- **Correct**: `O=C1N(C(c2ccccc2)c2ccccc2)c2ccccc2C1(O)c1ccc(Br)cc1O`

**Root Cause**: Confused ketone hydrate (gem-diol) with anhydride opening

**Analysis**:
- Product has gem-diol: `C1(O)` - carbon with TWO OH groups
- Wrong answer treated as anhydride opening: `O=C1OC(=O)c2...` (incorrect structure)
- Correct answer has ketone precursor: `C1(=O)` which hydrates to `C1(O)`
- Anhydride would give TWO carbonyls, not gem-diol

**Key Pattern**:
```
gem-Diol identification:
- C1(O) = carbon with two single-bonded oxygens (hydrated ketone)
- C1(=O) = carbon with one double-bonded oxygen (ketone)

Anhydride identification:
- O=C1OC(=O)... = two carbonyls connected by oxygen

For ERROR #28:
- Product has: C1(O)c1ccc(Br)cc1O (gem-diol on aryl ring)
- Precursor has: C1(=O) (ketone)
- Hydration: ketone + water → gem-diol
```

---

### ERROR #45: Ethyl vs Benzyl Ester in Deprotection

**Question**: Deprotections
- **Product**: `C[C@@H]1C[C@H](NC(=O)OC(C)(C)C)C(=O)N1CC(=O)O`
- **Wrong**: `C[C@@H]1C[C@H](NC(=O)OC(C)(C)C)C(=O)N1CC(=O)OCc1ccccc1`
- **Correct**: `CCOC(=O)CN1C(=O)[C@@H](NC(=O)OC(C)(C)C)C[C@H]1C`

**Root Cause**: Wrong ester protecting group (benzyl vs ethyl)

**Analysis**:
- Wrong answer used benzyl ester: `CC(=O)OCc1ccccc1` (malformed)
- Correct answer uses ethyl ester: `CCOC(=O)CN1...`
- Benzyl ester has phenyl ring: `C(=O)OCc1ccccc1`
- Ethyl ester has two carbons: `CCOC(=O)`
- The ester is on the side chain nitrogen

**Key Pattern**:
```
Ester SMILES patterns:
- Ethyl ester: CCOC(=O) = CH3-CH2-O-C(=O)-
- Benzyl ester: C(=O)OCc1ccccc1 = C(=O)-O-CH2-Ph
- Methyl ester: COC(=O) = CH3-O-C(=O)-

In ERROR #45:
- Precursor: CCOC(=O)CN1C(=O)[C@@H]...
- The ethyl ester is on the CN (aminomethyl) group
- Product has free acid: CC(=O)O from deprotection
```

---

### ERROR #25: Amine Protonation State in Boc Protection

**Question**: Protections
- **Product**: `COC(=O)[C@@H](NC(=O)OC(C)(C)C)c1ccccc1C`
- **Wrong**: `COC(=O)[C@@H](N)c1ccccc1C.CC(C)(C)OC(=O)OC(=O)OC(C)(C)C`
- **Correct**: `CC(C)(C)OC(=O)OC(=O)OC(C)(C)C.COC(=O)[C@@H]([NH3+])c1ccccc1C`

**Root Cause**: Wrong SMILES for amine in amino acid precursor

**Analysis**:
- Wrong answer used `N` for free amine
- Correct answer uses `[NH3+]` (protonated ammonium form)
- This is a protected amino acid ester (phenylalanine derivative)
- Amino acid precursors in USPTO-50k use `[NH3+]`

**Key Pattern**:
```
Amino acid vs simple amine:
- Simple amine (aniline, etc.): N
- Amino acid/amino acid ester: [NH3+]

In ERROR #25:
- Precursor: COC(=O)[C@@H]([NH3+])c1ccccc1C
- [NH3+] = ammonium form of amino group
- [C@@H] = chiral alpha-carbon
- COC(=O) = methyl ester
- c1ccccc1C = phenylalanine side chain
```

---

### ERROR #26: Hydrazine Cyclization Precursor

**Question**: Heterocycle formation
- **Product**: `Cc1ccc(Cl)c2c3c([nH]c12)CCNC3.Cl`
- **Wrong**: `CC(=O)O.c1ccc(Cl)cc1-c1c2c([nH]c1)CCNC2`
- **Correct**: `Cc1ccc(Cl)cc1NN.Cl.O=C1CCNCC1`

**Root Cause**: Failed to identify hydrazine + lactam cyclization

**Analysis**:
- Wrong answer used acetic acid and malformed aryl fragment
- Correct answer uses aryl hydrazine: `Cc1ccc(Cl)cc1NN`
- The `NN` at the end indicates hydrazine (two nitrogens)
- Plus lactam: `O=C1CCNCC1` (piperidinone)

**Key Pattern**:
```
Hydrazine precursor identification:
- Look for NN in SMILES (two nitrogens in a row)
- Ar-NN = aryl hydrazine
- Hydrazines cyclize with carbonyls to form N-heterocycles

In ERROR #26:
- Precursor 1: Cc1ccc(Cl)cc1NN (aryl hydrazine)
- Precursor 2: O=C1CCNCC1 (lactam/piperidinone)
- Forward: Hydrazine + lactam → fused indole-piperazine

NOT: Acetic acid (CC(=O)O) - wrong cyclization partner
```

---

## Current Iteration Errors (iter1_sub5)

### ERROR #41: Wittig vs Suzuki for Vinyl Groups

**Question**: C-C bond formation
- **Product**: `C=Cc1c(F)ccc(C2(CC)OCCO2)c1OC`
- **Wrong**: `c1c(F)ccc(Br)c1OC.C=C[C@H]1CCO[C@H](CC)O1` (Suzuki: bromoaryl + vinyl boron)
- **Correct**: `CCC1(c2ccc(F)c(C=O)c2OC)OCCO1.C[P+](c1ccccc1)(c1ccccc1)c1ccccc1` (Wittig)

**Root Cause**: Treated vinyl group as coming from Suzuki coupling instead of Wittig reaction

**Analysis**:
- Product has vinyl group: `C=Cc1...` (vinyl attached to aromatic)
- Wrong answer disconnected at wrong bond (assumed Suzuki coupling)
- Correct answer uses Wittig:
  - Carbonyl precursor: `CCC1(...)C=O(...)OCCO1` (ketone with dioxane substituent)
  - Ylide: `C[P+](c1ccccc1)(c1ccccc1)c1ccccc1` (phosphonium ylide)
  - The ylide attacks carbonyl to form alkene

**Key Pattern**:
```
Vinyl group retrosynthesis:
- Product has: C=C (vinyl/alkene)
- Question: Was this from Suzuki (coupling) or Wittig (olefination)?

Wittig indicators:
- Product has C=C formed from carbonyl + phosphonium ylide
- Ylide SMILES: C[P+](...)(...)... (phosphorus with positive charge)
- Carbonyl SMILES: C=O (ketone/aldehyde)

Suzuki indicators:
- Product has C-C bond from organoboron + halide
- Boron SMILES: B(O)O (boronic acid)
- No C=C formed (alkene already present)

In ERROR #41:
- Product: C=C attached to aromatic → suggests Wittig disconnection
- Precursor 1: CCC1(...)C=O (ketone precursor)
- Precursor 2: C[P+](...) (phosphonium ylide)

NOT: C=C[...] + bromoaryl (Suzuki would not form this vinyl)
```

---

### ERROR #36: Boronic Acid (B(O)O) vs Alkyne (C#C) in Suzuki Coupling

**Question**: C-C bond formation
- **Product**: `N#Cc1cccc(-c2nc(N)nc3c2nnn3Cc2cccc(C3(O)CCC3)n2)c1`
- **Wrong**: `C#C.Brc1cccc(-c2nc(N)nc3c2nnn3Cc2cccc(C3(O)CCC3)n2)c1` (Sonogashira: acetylene + aryl bromide)
- **Correct**: `N#Cc1cccc(B(O)O)c1.Nc1nc(Cl)c2nnn(Cc3cccc(C4(O)CCC4)n3)c2n1` (Suzuki)

**Root Cause**: Confused boronic acid `B(O)O` with terminal alkyne `C#C`

**Analysis**:
- Wrong answer used `C#C` (acetylene) for Sonogashira
- Correct answer uses `B(O)O` (boronic acid) for Suzuki
- Boronic acid SMILES: `N#Cc1cccc(B(O)O)c1` = aryl boronic acid with cyano substituent
- Halide: aryl chloride `Nc1nc(Cl)c2nnn(...)c2n1` (NOT bromide)

**Key Pattern**:
```
Identifying coupling partners by SMILES:

Boronic acid (Suzuki):
- SMILES: B(O)O or CB(O)O
- Examples: c1ccc(B(O)O)cc1 (phenylboronic acid)
- Product: N#Cc1cccc(B(O)O)c1 (4-cyano-phenylboronic acid)

Terminal alkyne (Sonogashira):
- SMILES: C#C
- Examples: C#C (acetylene), R-C#C (terminal alkyne)
- Product would have C#C- aryl bond (alkyne in product)

In ERROR #36:
- Correct precursor 1: N#Cc1cccc(B(O)O)c1 (aryl BORONIC ACID, not alkyne)
- Correct precursor 2: Nc1nc(Cl)c2nnn(...)c2n1 (aryl CHLORIDE, not bromide)
- Reaction: Suzuki coupling (boron + halide)

NOT: C#C (Sonogashira would give different product)
```

---

### ERROR #22: Wittig with Benzyl Protected Ylide

**Question**: C-C bond formation
- **Product**: `C(=Cc1ccccc1OCc1ccccc1)CCc1ccc2ccccc2c1`
- **Wrong**: `O=C(Cc1ccc2ccccc2c1)c1ccccc1OCc1ccccc1.P(Cc1ccc2ccccc2c1)(C)(C)C` (incorrect ylide)
- **Correct**: `O=CCCc1ccc2ccccc2c1.c1ccc(COc2ccccc2C[P+](c2ccccc2)(c2ccccc2)c2ccccc2)cc1`

**Root Cause**: Failed to recognize benzyl protecting group in Wittig ylide

**Analysis**:
- Product has stilbene-like structure with benzyl ether: `C(=Cc1ccccc1OCc1ccccc1)`
- The `OCc1ccccc1` is benzyl ether (NOT methyl ether `OC`)
- Correct ylide has benzyl protecting group: `c1ccc(COc2ccccc2C[P+](...)cc1`
- The ylide connects via the aromatic ring, with `-COc2ccccc2` as benzyl protecting group

**Key Pattern**:
```
Benzyl ether vs methyl ether in SMILES:

Benzyl ether protecting group:
- SMILES: OCc1ccccc1
- Structure: O-CH2-Ph (oxygen connected to CH2, then phenyl)
- The `c1ccccc1` after `OC` indicates phenyl ring of benzyl

Methyl ether:
- SMILES: OC
- Structure: O-CH3 (no phenyl ring)

In ERROR #22:
- Product: C(=Cc1ccccc1OCc1ccccc1)CCc1...
- The OCc1ccccc1 = BENZYL ETHER (benzyl protected phenol/alcohol)
- Correct ylide: c1ccc(COc2ccccc2C[P+](...)cc1
- The `COc2ccccc2` = benzyl ether attached to phosphorus ylide
- Precursor 1: O=CCCc1ccc2ccccc2c1 (aldehyde/ketone with naphthyl)
- Precursor 2: c1ccc(COc2ccccc2C[P+](...))cc1 (ylide with benzyl protecting group)

NOT: P(C)(C) (simple phosphine, need phosphonium ylide C[P+](...))
```

---

### ERROR #13: Alkene Hydrogenation in Reductions

**Question**: Reductions
- **Product**: `CCCCOC(=O)CCc1cc(CO[Si](C)(C)C(C)(C)C)cc(OC)n1`
- **Wrong**: `CCCCOC(=O)CCc1cc(C(=O)OCC)cc(OC)n1` (ester reduction instead of alkene)
- **Correct**: `CCCCOC(=O)/C=C/c1cc(CO[Si](C)(C)C(C)(C)C)cc(OC)n1`

**Root Cause**: Reduced ester instead of recognizing alkene hydrogenation

**Analysis**:
- Product has saturated chain: `CCCCOC(=O)CCc1...` (ethyl-aryl with propyl chain)
- Precursor has alkene in chain: `/C=C/` (the double bond that was hydrogenated)
- The ester `CCCCOC(=O)` stays the same, only alkene is reduced
- SMILES `/C=C/` in middle of chain indicates alkene that was hydrogenated

**Key Pattern**:
```
Alkene hydrogenation retrosynthesis:

Hydrogenation pattern:
- Product has: CC (saturated chain with substituent)
- Precursor has: /C=C/ (alkene in chain, shown with / bonds)
- Reaction: H2/Pd hydrogenation of alkene to alkane

SMILES notation for hydrogenation:
- Saturated: CC (single bond between carbons)
- Unsaturated: /C=C/ (double bond, with stereo chemistry indicators)
- The `/` indicates stereochemistry but also signals double bond

In ERROR #13:
- Product: CCCCOC(=O)CCc1... (saturated propyl chain attached to ester)
- Precursor: CCCCOC(=O)/C=C/c1... (alkene in chain, ester stays same)
- Key transformation: /C=C/ → CC (hydrogenation)
- The TBDMS protecting group (CO[Si](C)(C)C(C)(C)C) stays unchanged

NOT: Ester reduction (would change C(=O)OR to CH2OH)
```

---

### ERROR #34: Wrong Halide in Sonogashira Coupling

**Question**: C-C bond formation
- **Product**: `N#Cc1cccc(C#CC2(O)CCN(C(=O)Cc3ccc(-n4cnnn4)cc3)CC2)c1`
- **Wrong**: `N#Cc1cccc(I)c1.C#CC1(O)CCN(C(=O)Cc2ccc(-n3cnnn3)cc2)CC1` (aryl IODIDE)
- **Correct**: `C#CC1(O)CCN(C(=O)Cc2ccc(-n3cnnn3)cc2)CC1.N#Cc1cccc(Br)c1` (aryl BROMIDE)

**Root Cause**: Used iodide instead of bromide for Sonogashira coupling

**Analysis**:
- Wrong answer used aryl iodide: `N#Cc1cccc(I)c1` (iodine substituent)
- Correct answer uses aryl bromide: `N#Cc1cccc(Br)c1` (bromine substituent)
- Both fragments have terminal alkynes (C#C) - correct for Sonogashira
- Only difference is halide identity (Br vs I)

**Key Pattern**:
```
Halide identification in coupling:

Common halide SMILES:
- Iodine: I (aryl iodide)
- Bromine: Br (aryl bromide)
- Chlorine: Cl (aryl chloride)

When halide matters:
1. Check product for halide-reactive functional groups
2. Consider reaction conditions (some couplings prefer certain halides)
3. Match precursor halide to reaction type

Sonogashira typical halides:
- Aryl iodide (I): Most reactive, works with most conditions
- Aryl bromide (Br): Common, good balance of reactivity/stability
- Aryl chloride (Cl): Less reactive, needs special catalysts

In ERROR #34:
- Product has terminal alkyne: C#CC2(O)... (alkyne on cyclohexane)
- Product has cyano aryl: N#Cc1cccc... (aryl with nitrile)
- Precursor 1: C#CC1(O)CCN(...)CC1 (terminal alkyne)
- Precursor 2: N#Cc1cccc(Br)c1 (aryl BROMIDE, not iodide)
- Reaction: Sonogashira coupling (terminal alkyne + aryl halide)

NOT: N#Cc1cccc(I)c1 (iodide - wrong halide for this reaction)
```

---

## Current Iteration Errors (iter2_sub4)

### ERROR #42: Fused Ring Ester Deprotection - Wrong SMILES Numbering

**Question**: Deprotections
- **Product**: `CC(C)(C)n1nc(-c2ccncc2)c2c1CCC(C(=O)O)C2` (carboxylic acid on fused bicyclic system)
- **Wrong Answer**: `CC(C)(C)n1nc(-c2ccncc2)c2c1CCC(C(=O)OC)C2`
- **Correct Answer**: `COC(=O)C1CCc2c(c(-c3ccncc3)nn2C(C)(C)C)C1`

**Root Cause**: Used incorrect SMILES numbering and ester pattern

**Analysis**:
- Product has carboxylic acid: `C(=O)O` on cyclohexane ring fused to pyrazole
- Wrong answer tried to add methyl ester using `C(=O)OC` pattern in same SMILES numbering
- Correct answer uses completely different SMILES representation:
  - Starts from cyclohexane: `C1` (bridgehead carbon)
  - Uses `COC(=O)` pattern (methyl ester, not `C(=O)OC`)
  - Correct ring fusion numbering: `C1CCc2c(...)nn2C(C)(C)C`

**Key Pattern**:
```
Fused ring ester deprotection:

1. Identify carboxylic acid in product: C(=O)O
   - Product: ...CCC(C(=O)O)C2 (acid on cyclohexane ring)

2. Determine ester type:
   - Methyl ester: COC(=O) or C(=O)OC (same meaning, different position)
   - Ethyl ester: CCOC(=O) or C(=O)OCC
   - Benzyl ester: C(=O)OCc1ccccc1

3. Match SMILES numbering to correct ring connectivity:
   - Pyrazole-cyclohexane fusion requires specific numbering
   - Ester position determined by bridgehead and fusion points
   - May need to renumber from different starting atom

In ERROR #42:
- Wrong: Used pyrazole numbering for ester attachment
- Correct: Renumbered from cyclohexane, used COC(=O) pattern
- Key: `COC(=O)C1...` shows ester at bridgehead position

SMILES distinction:
- Wrong: C(=O)OC (ester, but wrong position)
- Correct: COC(=O) (same ester, different SMILES order)
```

---

### ERROR #49: Multi-Functional Oxidation - Reduced Wrong Functional Group

**Question**: Oxidations
- **Product**: `COC(=O)CN(c1ccccc1C)S(=O)(=O)c1ccccc1C(=O)c1cc(OC)c2c(c1)OCO2`
- **Wrong Answer**: `COC(=O)CN(c1ccccc1C)Sc1ccccc1C(O)c1cc(OC)c2c(c1)OCO2`
  - Reduced sulfone to sulfide: S(=O)(=O) → S ❌
- **Correct Answer**: `COC(=O)CN(c1ccccc1C)S(=O)(=O)c1ccccc1C(O)c1cc(OC)c2c(c1)OCO2`
  - Kept sulfone unchanged: S(=O)(=O) ✓
  - Reduced ketone to alcohol: C(=O) → C(O) ✓

**Root Cause**: Reduced the WRONG functional group in multi-functional molecule

**Analysis**:
- Product has TWO potentially oxidizable groups:
  1. Sulfone: S(=O)(=O) (already fully oxidized, NOT from this reaction)
  2. Ketone: C(=O) (oxidation product, WAS from this reaction)
- Wrong answer reduced sulfone (already correct)
- Correct answer reduced ketone (was actually oxidized)

**Key Pattern**:
```
Multi-functional oxidation analysis:

Step 1: Identify ALL oxidizable groups in product:
        - Ketone: C(=O)
        - Aldehyde: C=O
        - Sulfone: S(=O)(=O)
        - Sulfoxide: S(=O)

Step 2: Determine which group was actually oxidized:
        - Look for patterns: C(=O) → C(O) (ketone→alcohol)
        - C=O → CO (aldehyde→primary alcohol)
        - S(=O)(=O) → S (sulfone→sulfide)
        - S(=O) → S (sulfoxide→sulfide)

Step 3: Identify which groups are ALREADY correct:
        - If group is already in oxidized form AND not the transformation site
        - It was NOT oxidized in THIS reaction
        - Keep it UNCHANGED

Step 4: Only reduce the group that was actually oxidized:
        In ERROR #49:
        - Sulfone S(=O)(=O): Already correct, NOT this reaction
        - Ketone C(=O): Was oxidized, reduce to C(O)
        - Result: Keep sulfone, reduce ketone

CRITICAL: NOT all carbonyl/sulfur groups need reduction!
```

---

### SUCCESS PATTERNS (iter2_sub4)

These predictions were CORRECT - learn from them!

#### SUCCESS #9: Aldehyde from Primary Alcohol Oxidation
- **Product**: `O=CC12CC3CC(CC(C3)C1)C2`
- **Precursor**: `OCC12CC3CC(CC(C3)C1)C2`
- **Key**: Aldehyde `O=C` → primary alcohol `OCC`

#### SUCCESS #14: Oxime Formation (FGI)
- **Product**: `CC(C)(C)c1cc(C=NO)c(O)c(-c2ccc(C(F)(F)F)nc2)c1`
- **Precursor**: `CC(C)(C)c1cc(C=O)c(O)c(-c2ccc(C(F)(F)F)nc2)c1.NO`
- **Key**: Oxime `C=NO` → aldehyde `C=O` + hydroxylamine `NO`

#### SUCCESS #19: Benzyl Ether Deprotection
- **Product**: `O=C(NCC(=O)N1CCN(C(=O)c2ccccc2C(F)(F)F)CC1)c1ccc(-c2ccccc2O)cc1`
- **Precursor**: `O=C(NCC(=O)N1CCN(C(=O)c2ccccc2C(F)(F)F)CC1)c1ccc(-c2ccccc2OCc2ccccc2)cc1`
- **Key**: Phenol `-O` → benzyl ether `OCc1ccccc1`

---

## Current Iteration Errors (iter2_sub6)

### ERROR #31: Missed Diazotization (FGI)

**Question**: Functional group interconversion (FGI)
- **Product**: `C[C@H]1C[C@@H](c2ccncc2NC(=O)c2ccc(F)c(-c3c(F)cccc3F)n2)C[C@@H](NC(=O)OC(C)(C)C)[C@H]1N=[N+]=[N-]`
- **Wrong Answer**: `C[C@H]1C[C@@H](c2ccncc2NC(=O)c2ccc(F)c(-c3c(F)cccc3F)n2)C[C@@H](NC(=O)OC(C)(C)C)[C@H]1N`
- **Correct Answer**: Same as product (with diazonium group)

**Root Cause**: Model completely missed diazotization reaction

**Analysis**:
- Product has diazonium group: `N=[N+]=[N-]` at the end
- Wrong answer returned product with amine: `N` (missing diazonium!)
- This is diazotization: amine → diazonium salt
- Reaction type: FGI (Functional Group Interconversion)

**Key Pattern**:
```
Diazotization retrosynthesis:

1. Look for diazonium group in product: N=[N+]=[N-]
   - Linear three-nitrogen chain with charges
   - Attached to carbon in the molecule

2. Identify the carbon bearing diazonium:
   Product: ...[C@H]1N=[N+]=[N-]
   The carbon [C@H]1 has the diazonium group

3. Retrosynthetic disconnection:
   Product: ...[C@H]1-N=[N+]=[N-] (diazonium)
   Precursor: ...[C@H]1-N (amine)
   Reaction: Diazotization with NaNO2 + HCl

4. Forward reaction:
   R-NH2 + NaNO2 + 2HCl → R-N₂⁺ Cl⁻ + NaCl + 2H2O

SMILES patterns:
- Diazonium: N=[N+]=[N-] (three nitrogens, charged)
- Amine: N (nitrogen attached to carbon)

In ERROR #31:
- Product: ...[C@H]1N=[N+]=[N-] (diazonium on cyclohexane)
- Precursor should be: ...[C@H]1N (amine)
- LLM returned: ...[C@H]1N (amine, missed the reaction!)

Common mistake:
- Thinking the product IS the precursor (no transformation)
- Missing the diazonium group entirely
- Confusing diazonium with azide (context matters!)
```

### ERROR #44: Wrong SMILES Connectivity (Acylation)

**Question**: Acylation and related processes
- **Product**: `CCCOc1cc(F)cc(C[C@H](NC(C)=O)[C@H](O)[C@H]2CO[C@@H](OCC(C)(C)C)[C@H](C)N2C(=O)OC(C)(C)C)c1`
- **Wrong Answer**: `CCCOc1cc(F)cc(C[C@H](N)[C@H](O)[C@H]2CO[C@@H](OCC(C)(C)C)[C@H](C)N2C(=O)OC(C)(C)C)c1.CC(=O)OC(=O)C`
- **Correct Answer**: `CC(=O)OC(C)=O.CCCOc1cc(F)cc(CC(N)C(O)[C@H]2CO[C@@H](OCC(C)(C)C)[C@H](C)N2C(=O)OC(C)(C)C)c1`

**Root Cause**: Wrong SMILES connectivity for amino acid derivative

**Analysis**:
- Wrong precursor has: `C[C@H](N)[C@H](O)` (amine and OH on adjacent chiral carbons)
- Correct precursor has: `CC(N)C(O)` (amine on one carbon, OH on separate carbon)
- These represent DIFFERENT molecular structures!

**Key Pattern**:
```
SMILES connectivity for amino acid derivatives:

WRONG: C[C@H](N)[C@H](O)
       |    |    |
       C    N    O
       (chiral) (chiral)
       Amine and OH are on DIFFERENT carbons but BOTH chiral
       The [C@H] before N makes that carbon chiral
       The [C@H] before O makes that carbon chiral

CORRECT: CC(N)C(O)
         ||   ||
         C    C
         (methyl) (hydroxyl carbon)
         Amine on first carbon (CC(N))
         Hydroxyl on second carbon (C(O))
         Different connectivity!

Critical rule:
- CC(N) = one carbon with amine (methylamine-like)
- C[C@H](N) = TWO carbons, second one chiral with amine
- The pattern CC(N)C(O) has amine on one C, OH on the NEXT C
- NOT C[C@H](N)[C@H](O) which has N and OH on adjacent stereocenters

In ERROR #44:
- Product: ...C[C@H](NC(C)=O)[C@H](O)[C@H]2...
           |              |
           Acetamide      OH
           on carbon 1    on carbon 2
           (adjacent stereocenters)

- Wrong precursor: ...C[C@H](N)[C@H](O)[C@H]2...
                   |    |    |
                   N    O    (same adjacency - WRONG!)

- Correct precursor: ...CC(N)C(O)[C@H]2...
                     ||   ||
                     N    O
                     (different carbons - CORRECT!)

How to verify:
1. Count the carbons between functional groups
2. CC(N) has amine on carbon 1
3. C(O) has OH on carbon 2
4. Connect as CC(N)C(O)
5. NOT C[C@H](N)[C@H](O) which implies [C@H]-N and [C@H]-O
```

---

## Current Iteration Errors (iter2_sub7)

### ERROR #33: Heterocycle SMILES Numbering (Heteroatom Alkylation)

**Question**: Heteroatom alkylation and arylation
- **Product**: `COC(=O)c1c(C=O)c(C)c(C)n1CC=C(Cl)Cl`
- **Wrong Answer**: `COC(=O)c1c(C=O)c(C)c(C)[nH]1.ClCC=C(Cl)Cl`
- **Correct Answer**: `COC(=O)c1[nH]c(C)c(C)c1C=O.ClCC=C(Cl)Cl`

**Root Cause**: Wrong SMILES starting position and ring numbering for N-alkylated heterocycle

**Analysis**:
- Product has 5-membered heterocycle with ester, aldehyde, and two methyl substituents
- Nitrogen is alkylated with allylic chloride (CC=C(Cl)Cl)
- Wrong precursor put aldehyde as a substituent: `c1c(C=O)...`
- Correct precursor has aldehyde as ring closure: `c1C=O` (closes to carbon 1)

**SMILES Interpretation**:
```
Product ring connectivity:
- Carbon 1: Has methyl ester COC(=O) attached
- Carbon 2: Has aldehyde C=O (relative position)
- Carbon 3: Has methyl C
- Carbon 4: Has methyl C
- Carbon 5: Is nitrogen (N), attached to allylic chloride

WRONG Precursor:
COC(=O)c1c(C=O)c(C)c(C)[nH]1
├─ Ring: c1 (ester) → c2(C=O) → c3(C) → c4(C) → [nH]1
├─ Aldehyde is SUBSTITUENT on carbon 2
└─ Nitrogen closes ring to position 1

CORRECT Precursor:
COC(=O)c1[nH]c(C)c(C)c1C=O
├─ Ring: c1 (ester) → [nH]2 → c3(C) → c4(C) → c1C=O
├─ Nitrogen is at position 2
└─ Aldehyde CLOSES ring to position 1

Key distinction:
- c1c(C=O)... = aldehyde attached as substituent
- c1[...]c1C=O = aldehyde closes ring to position 1
- Ring closure must match the attachment point!
```

**Key Pattern**:
```
Heterocycle SMILES numbering rules:

1. Start from the carbon with exocyclic groups (ester, etc.)
2. Follow the ring path: c1 → next atom → next atom → ...
3. Ring closure must use the SAME number as the starting carbon
4. Substituents (like aldehyde) can be:
   - Attached groups: c1c(X) means X attached to position 1
   - Ring closures: c1[...]c1X means X closes ring at position 1

For product COC(=O)c1c(C=O)c(C)c(C)n1CC=C(Cl)Cl:
- Ester attaches at carbon 1
- Aldehyde should close to carbon 1 (c1C=O)
- NOT be a substituent (c1c(C=O))

SMILES pattern to remember:
- Substituent: c1c(X) means X attached to position 1
- Closure: c1[...]c1X means X closes ring at position 1
```
