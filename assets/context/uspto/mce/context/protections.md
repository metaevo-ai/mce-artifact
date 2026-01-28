# Retrosynthesis Guide: Protections

## Overview

Protection reactions involve masking functional groups to prevent them from reacting during synthesis. The retrosynthetic analysis involves identifying the protected form and determining what protecting group was added.

## Common Protecting Groups

### 1. Boc (tert-Butoxycarbonyl)

**Pattern**: Secondary amine protected as carbamate
- **SMILES**: `NC(=O)OC(C)(C)C`
- **Reagent**: Boc2O or Boc-ON
- **Deprotection**: TFA, HCl

### 2. Cbz (Benzyloxycarbonyl)

**Pattern**: Amine protected as carbamate with benzyl group
- **SMILES**: `NC(=O)OCc1ccccc1`
- **Reagent**: Cbz-Cl
- **Deprotection**: H2, Pd/C

### 3. Benzyl Ether

**Pattern**: Alcohol/phenol protected as benzyl ether
- **SMILES**: `OCc1ccccc1`
- **Reagent**: BnBr, Ag2O
- **Deprotection**: H2, Pd/C

### 4. Methyl Ether

**Pattern**: Alcohol/phenol protected as methyl ether
- **SMILES**: `OC`
- **Reagent**: MeI, Ag2O
- **Deprotection**: BBr3

### 5. Silyl Ethers

**Pattern**: Alcohol protected as silyl ether
- **SMILES**: `OSi(C)(C)C` (TMS), `OSi(C)(C)C(C)(C)C` (TBS)
- **Reagent**: TMSCl, TBSCl
- **Deprotection**: TBAF, acid

## Key Distinctions

| Protecting Group | SMILES Pattern | Deprotects With |
|-----------------|----------------|-----------------|
| Benzyl ether | `OCc1ccccc1` | H2/Pd |
| Methyl ether | `OC` | BBr3 |
| Boc | `C(C)(C)C` (on N) | TFA |
| Cbz | `C(=O)OCc1ccccc1` | H2/Pd |

## Common Pitfalls

1. **Missing the ring in benzyl**: `OCc1ccccc1` has a ring, `OC` doesn't
2. **Confusing Boc and Cbz**: Boc has tert-butyl, Cbz has benzyl
3. **Forgetting carbonyl in carbamates**: `NC(=O)O...` not just `NCO`

## Critical Error Pattern: Secondary vs Tertiary Amine in Boc Protection

### Common Mistake (ERROR #17)
- **Question**: Protection with product `CC(C)(C)OC(=O)N1Cc2ccc([N+](=O)[O-])cc2C1=O`
- **Wrong answer**: `O=C1N(Cc2ccc([N+](=O)[O-])cc2)C1.CC(C)(C)OC(=O)OC(=O)OC(C)(C)C`
- **Correct answer**: `CC(C)(C)OC(=O)OC(=O)OC(C)(C)C.O=C1NCc2ccc([N+](=O)[O-])cc21`

### Why This Matters
- Boc protection requires a **secondary amine** (NH), not a tertiary amine (N)
- The lactam precursor must have a secondary amine for Boc to add
- SMILES notation for secondary amine: `O=C1NC...1` (N has H)
- SMILES notation for tertiary amine: `O=C1N(...)C1` (N has no H)

### How to Identify Secondary vs Tertiary Amine
```
Lactam structure: O=C1NCc2ccc([N+](=O)[O-])cc21
                  |
                  The N has: 1 bond to C1 (ring), 1 bond to C (CH2), 1 H
                  This is a secondary amine - correct for Boc protection

SMILES patterns:
- Secondary amine (correct for Boc): O=C1NCc2...cc21
                                      ^N has H (shown by NC, not N(C...))

- Tertiary amine (WRONG for Boc): O=C1N(Cc2...)cc2)C1
                                  ^N has two carbons attached (no H)

Key distinction:
- O=C1NC...1 = secondary amine (N-H in lactam)
- O=C1N(...)1 = tertiary amine (N in lactam, no H)
```

### Correct Boc Protection Precursor
```
Product: CC(C)(C)OC(=O)N1Cc2ccc([N+](=O)[O-])cc2C1=O
         |
         Boc-protected lactam (carbamate on nitrogen)

Precursor 1 (amine): O=C1NCc2ccc([N+](=O)[O-])cc21
                     Secondary amine (lactam NH)
                     The nitro group is on the phenyl ring

Precursor 2 (reagent): CC(C)(C)OC(=O)OC(=O)OC(C)(C)C
                       Boc2O (di-tert-butyl dicarbonate)

Forward reaction: Boc2O reacts with lactam NH to form carbamate
                  Releases CO2 and tert-butanol
```

## Critical Error Pattern: SMILES Numbering for Bicyclic Systems

### Common Mistake
- **Question**: `CC(C)(C)OC(=O)N1CCn2c(cc3ccccc32)C1`
- **Wrong answer**: `CC(C)(C)OC(=O)OC(=O)OC(C)(C)C.O=C1CCn2c(cc3ccccc32)C1`
- **Correct answer**: `CC(C)(C)OC(=O)OC(=O)OC(C)(C)C.c1ccc2c(c1)cc1n2CCNC1`

### Why This Matters
- The same bicyclic structure can be written with different SMILES numbering schemes
- `O=C1CCn2c(cc3ccccc32)C1` and `c1ccc2c(c1)cc1n2CCNC1` represent the same molecule
- When the correct answer uses a different numbering, both are valid but the expected one must be used

### How to Handle Bicyclic System Numbering
```
Product: CC(C)(C)OC(=O)N1CCn2c(cc3ccccc32)C1
         |
         N1 connects to: CC (CH2-CH2), n2 (indole nitrogen), C1 (closure)

Key features of the bicyclic system:
- Piperazine ring: N1-CC-C1 (six-membered with two nitrogens)
- Fused to indole: n2-c(cc3ccccc32)
- The indole is fused at positions 2 and 3 of piperazine

Valid precursor SMILES options:
Option 1: O=C1CCn2c(cc3ccccc32)C1
          |    |
          C1   n2 (nitrogen in indole ring)
          Closes at position 1 (piperazine carbon)

Option 2: c1ccc2c(c1)cc1n2CCNC1
          |    |    |    |
          c1   c2   n2   CCNC1
          Starts from indole phenyl, closes at nitrogen

Both represent: piperazine fused to indole

Rule: When in doubt about numbering, use the format that matches
      known examples or canonical SMILES patterns for the ring system
```

### Identifying Bicyclic Ring Systems
```
Common fused systems:
1. Indole-piperazine: Two nitrogen atoms, benzene fused to pyrrole fused to piperazine
2. Benzimidazole: Benzene fused to imidazole
3. Indoline: Reduced indole (benzene fused to pyrrolidine)

Look for:
- Multiple nitrogen atoms (n, N)
- Ring closures (1, 2, 3) that connect different rings
- Aromatic vs non-aromatic character in different rings
```

## Critical Error Pattern: Amine Protonation State in Boc Protection (ERROR #25)

### Common Mistake (ERROR #25)
- **Question**: `COC(=O)[C@@H](NC(=O)OC(C)(C)C)c1ccccc1C`
- **Wrong answer**: `COC(=O)[C@@H](N)c1ccccc1C.CC(C)(C)OC(=O)OC(=O)OC(C)(C)C`
- **Correct answer**: `CC(C)(C)OC(=O)OC(=O)OC(C)(C)C.COC(=O)[C@@H]([NH3+])c1ccccc1C`

### Why This Matters
- The wrong answer used `N` for the free amine
- The correct answer uses `[NH3+]` (protonated/ammonium form)
- In USPTO-50k retrosynthesis, amine reactants often appear as `[NH3+]` when they are part of amino acid esters
- The Boc protecting group reagent is `CC(C)(C)OC(=O)OC(=O)OC(C)(C)C` (Boc2O)

### How to Identify Correct Amine SMILES Format
```
Product: COC(=O)[C@@H](NC(=O)OC(C)(C)C)c1ccccc1C
         |
         This is a protected amino acid ester
         The amine is Boc-protected: NC(=O)OC(C)(C)C
         The ester is methyl: COC(=O)
         The amino acid is phenylalanine derivative: [C@@H](...)

Precursor analysis:
1. The protected form has: NC(=O)OC(C)(C)C (Boc on nitrogen)
2. The deprotected form should have: [NH3+] or N
3. For amino acid precursors in USPTO-50k: use [NH3+]

Correct SMILES breakdown:
- [NH3+]: protonated ammonium form (common for amino acid precursors)
- c1ccccc1C: phenyl ring with methyl (phenylalanine side chain)
- [C@@H]([NH3+]): chiral alpha-carbon with ammonium
- COC(=O)[C@@H](...): methyl ester of the amino acid

Wrong SMILES pattern:
- N: simple nitrogen (works for some amines but not amino acids in USPTO-50k)
- [NH3+]: ammonium ion (correct for amino acid esters)

Key distinction:
- Simple amines (aniline, benzylamine): N
- Amino acids/amino acid esters: [NH3+]
- The stereochemistry is at [C@@H] or [C@H] - this is an amino acid

For ERROR #25:
- Correct precursor: COC(=O)[C@@H]([NH3+])c1ccccc1C + Boc2O
- The [NH3+] indicates the ammonium form of the amino group
- This reacts with Boc2O to form the carbamate: NC(=O)OC(C)(C)C
```

### Key Principle: Amino Acid Precursor Format
```
In USPTO-50k retrosynthesis:
1. Boc-protected amino acids use [NH3+] for the free amine
2. The [NH3+] indicates it's the protonated form
3. The chiral center is marked with [C@@H] or [C@H]
4. The ester is typically methyl (COC(=O)) or ethyl (CCOC(=O))

Common pattern:
- Protected: COC(=O)[C@@H](NC(=O)OC(C)(C)C)...
- Precursor: COC(=O)[C@@H]([NH3+])... + Boc2O

SMILES check:
- [NH3+] - correct for amino acid precursors
- N - correct for simple amines (aniline, etc.)
```

---

## ✅ SUCCESS PATTERN: Secondary Amine Recognition (ID 17)

### What Worked
**Product**: `CC(C)(C)OC(=O)N1Cc2ccc([N+](=O)[O-])cc2C1=O`
**Precursors**: `CC(C)(C)OC(=O)OC(=O)OC(C)(C)C.O=C1NCc2ccc([N+](=O)[O-])cc21`
**Result**: ✅ CORRECT (100% Jaccard similarity)

### Key Success Factors

1. **Correctly identified secondary amine**: `O=C1NCc2...cc21`
   - SMILES `NC` indicates nitrogen with hydrogen (secondary)
   - Different from `N(C...)` which would be tertiary

2. **Correct Boc reagent**: `CC(C)(C)OC(=O)OC(=O)OC(C)(C)C`
   - Always use Boc2O for Boc protection reactions

3. **Proper nitro group placement**: `[N+](=O)[O-]` on aromatic ring

### Pattern to Replicate
```
For Boc protection questions:

1. Look for carbamate pattern in product: NC(=O)OC(C)(C)C
2. Find the nitrogen that is protected
3. Check if it's secondary (has H) or tertiary (no H)
   - Secondary: O=C1NC... (N has H, shown by NC)
   - Tertiary: O=C1N(...) (N has two carbons, no H)
4. Boc requires secondary amine precursor
5. Precursor should have: O=C1NC... (not O=C1N(...))
```

### SMILES Validation Checklist
- [ ] Protected product has: `NC(=O)OC(C)(C)C` (carbamate)
- [ ] Precursor has: `NC` (secondary amine, not tertiary)
- [ ] Reagent is: `CC(C)(C)OC(=O)OC(=O)OC(C)(C)C` (Boc2O)
- [ ] Ring numbering consistent throughout

---

## Critical Error Pattern: Boc Protection Site (Amine vs Heterocycle Nitrogen)

### Common Mistake (ID 40)
- **Question**: Protection with product `COc1cccc(F)c1C1CCN(c2cnn(C(=O)OC(C)(C)C)c(=O)c2Br)CC1`
- **Wrong answer**: `C1CCNCC1.O=C(Cl)c1cnn(C(=O)OC(C)(C)C)c(=O)c1Br`
- **Correct answer**: `CC(C)(C)OC(=O)OC(=O)OC(C)(C)C.COc1cccc(F)c1C1CCN(c2cn[nH]c(=O)c2Br)CC1`

### Why This Matters
- The model disconnected the amide bond on the heterocycle (c2cnn(...)c(=O)c2Br)
- The correct Boc protection is on the piperidine nitrogen (C1CCN(...)CC1)
- The heterocycle has a free NH (not protected) - note `c2cn[nH]c(=O)c2Br`
- The piperidine nitrogen is the site of Boc protection

### How to Identify Correct Boc Protection Site
```
Product: COc1cccc(F)c1C1CCN(c2cnn(C(=O)OC(C)(C)C)c(=O)c2Br)CC1
         |
         Structure breakdown:
         - COc1cccc(F)c1: Anisole with fluorine (methoxyphenyl)
         - C1CCN(...)CC1: Piperidine ring (six-membered with N)
         - c2cnn(C(=O)OC(C)(C)C)c(=O)c2Br: Pyrazine/pyrimidine heterocycle
         - The nitrogen in piperidine has: C(=O)OC(C)(C)C (Boc group)

Key observation:
- The piperidine nitrogen (in C1CCN...) has the Boc protecting group
- The heterocycle nitrogen (in c2cn[nH]...) has NH (free, not protected)
- Note: [nH] indicates the heterocycle nitrogen has H (free)

SMILES analysis:
- C1CCN(c2...)CC1: Piperidine with substituent on nitrogen
- The (c2...) means the heterocycle is attached to N
- c2cn[nH]c(=O)c2: Heterocycle with free NH (note [nH])
- The [nH] shows the heterocycle nitrogen is NOT protected

Precursor 1 (amine): COc1cccc(F)c1C1CCN(c2cn[nH]c(=O)c2Br)CC1
                     |
                     Piperidine with free NH (not Boc-protected)
                     The heterocycle attached to N has [nH] (free)

Precursor 2 (reagent): CC(C)(C)OC(=O)OC(=O)OC(C)(C)C
                       Boc2O (di-tert-butyl dicarbonate)

Forward reaction:
- Boc2O reacts with piperidine nitrogen (NH)
- Forms carbamate: NC(=O)OC(C)(C)C (Boc-protected)
- The heterocycle nitrogen stays as [nH] (free, not protected)

Wrong vs Right:
- Wrong: C1CCNCC1 (free piperidine) + O=C(Cl)c1cnn(Boc)c(=O)c1Br (Boc on heterocycle)
         The model Boc'd the wrong nitrogen (heterocycle instead of piperidine)

- Right: Piperidine with free NH (on N) + Boc2O → Boc-protected piperidine
         The heterocycle stays with free [nH]
```

### Identifying Protected vs Unprotected Nitrogens
```
In SMILES, nitrogen protection state is shown by:

Protected (Boc):
- NC(=O)OC(C)(C)C: Amide nitrogen with Boc carbamate
- The N is part of: N-C(=O)-O-C(C)(C)C
- No [nH] shown (H is replaced by Boc)

Unprotected (NH):
- [nH]: Heterocycle nitrogen with H (free)
- N at end of chain: Simple amine, often [NH3+] for amino acids
- N in ring without [nH]: Could be tertiary (no H)

Boc protection pattern:
- Protected amine: NC(=O)OC(C)(C)C (carbamate)
- Protected amide: NC(=O)R (no Boc group, just amide)
- Free amine: N, [NH2], [NH3+]

For product ID 40:
- Piperidine N: Has C(=O)OC(C)(C)C → Boc-protected
- Heterocycle N: Has [nH] → free NH, not protected
- The model incorrectly protected the heterocycle instead
```

---

## ✅ SUCCESS PATTERN: Boc Protection on Secondary Amine (ID 40 - CORRECT)

### What Worked
**Product**: `COc1cccc(F)c1C1CCN(c2cnn(C(=O)OC(C)(C)C)c(=O)c2Br)CC1`
**Precursors**: `CC(C)(C)OC(=O)OC(=O)OC(C)(C)C.COc1cccc(F)c1C1CCN(c2cn[nH]c(=O)c2Br)CC1`
**Result**: ✅ CORRECT (100% Jaccard similarity)

### Key Success Factors

1. **Correctly identified which nitrogen is protected**: Piperidine nitrogen (not heterocycle)
2. **Recognized Boc group**: `C(=O)OC(C)(C)C` pattern on nitrogen
3. **Kept heterocycle free**: `[nH]` shows free NH on heterocycle
4. **Used correct reagent**: Boc2O (`CC(C)(C)OC(=O)OC(=O)OC(C)(C)C`)

### Pattern to Replicate
```
For Boc protection questions:

1. Identify ALL nitrogens in the product:
   - Count the nitrogens
   - Note their connectivity (which atoms they're attached to)

2. Determine which nitrogen has the Boc group:
   - Look for: NC(=O)OC(C)(C)C (carbamate on nitrogen)
   - The N should be followed by C(=O)OC(C)(C)C

3. The protected nitrogen in precursor:
   - Has NH (shown as N in chain, [nH] in heterocycles)
   - NOT already protected with Boc

4. Unprotected nitrogens:
   - Stay as [nH] (heterocycle with NH)
   - Stay as N (if simple amine)

5. Reagent is Boc2O: CC(C)(C)OC(=O)OC(=O)OC(C)(C)C
```

### SMILES Validation Checklist
- [ ] Identify the nitrogen with Boc: NC(=O)OC(C)(C)C
- [ ] Verify the Boc-protected nitrogen was NH in precursor
- [ ] Check other nitrogens are free: [nH] or N
- [ ] Use Boc2O as the reagent

### Example Analysis for ID 40
```
Product: COc1cccc(F)c1C1CCN(c2cnn(C(=O)OC(C)(C)C)c(=O)c2Br)CC1
         |
         Step 1: Identify nitrogens
         - Piperidine N: Has C(=O)OC(C)(C)C attached
         - Heterocycle N: Has [nH] (free NH)

         Step 2: Determine which is protected
         - Piperidine N: Has Boc group (NC(=O)OC(C)(C)C)
         - Heterocycle N: Free (just [nH])

         Step 3: Write precursors
         - Amine precursor: COc1cccc(F)c1C1CCN(c2cn[nH]c(=O)c2Br)CC1
                           (piperidine has N, heterocycle has [nH])
         - Reagent: CC(C)(C)OC(=O)OC(=O)OC(C)(C)C (Boc2O)
```

---

## ✅ SUCCESS PATTERN: Boc Protection on Benzylamine (ID 0 - CORRECT)

### What Worked
**Product**: `CC(C)(C)OC(=O)NCCc1ccc(N)cc1`
**Precursors**: `CC(C)(C)OC(=O)OC(=O)OC(C)(C)C.NCCc1ccc(N)cc1`
**Result**: ✅ CORRECT (100% Jaccard similarity)

### Key Success Factors

1. **Recognized Boc-protected benzylamine**: `NC(=O)OC(C)(C)C` pattern
2. **Identified correct precursor**: Free amine `NCCc1ccc(N)cc1` (4-aminophenethylamine)
3. **Used correct reagent**: Boc2O
4. **Preserved both amine groups**: Benzylamine and aniline remain in precursor

### Pattern to Replicate
```
For Boc protection on molecules with multiple amines:

1. Identify ALL amine groups:
   - Aliphatic amine: NCCc1... (benzylamine)
   - Aromatic amine: c1ccc(N)cc1 (aniline)

2. Determine which amine is protected:
   - Boc forms carbamates: NC(=O)OC(C)(C)C
   - Usually aliphatic amines react faster than aromatic

3. The protected amine in precursor:
   - Has free NH (N in SMILES)
   - Will react with Boc2O

4. Unprotected amines:
   - Stay as N or [NH2] in precursor
   - Both can be present in the same molecule

5. Reagent is Boc2O: CC(C)(C)OC(=O)OC(=O)OC(C)(C)C
```

### SMILES Validation Checklist
- [ ] Identify Boc pattern: NC(=O)OC(C)(C)C
- [ ] Verify precursor has free amine at that position
- [ ] Check other amines are preserved
- [ ] Use Boc2O as the reagent
