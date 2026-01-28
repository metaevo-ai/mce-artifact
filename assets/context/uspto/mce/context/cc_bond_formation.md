# Retrosynthesis Guide: C-C Bond Formation

## Overview

C-C bond formation reactions create new carbon-carbon bonds. Key reactions include cross-couplings (Suzuki, Stille, Heck), organometallic additions (Grignard, organolithium), and carbonylation reactions.

## Common C-C Bond Formation Patterns

### 1. Suzuki-Miyaura Coupling

**Pattern**: Organoboron + aryl/vinyl halide → coupled product
- **Reagents**: R-B(OR')2 + R'-X + Pd catalyst + base
- **Retrosynthetic**: Disconnect at C-B or C-X bond → organoboron + halide

**Key SMILES**:
- Boronic acid: `CB(O)O` or `B(O)O`
- Boronic ester: `CB(OC)OC`
- Organoboron: `c1ccc(B(O)O)cc1` (phenylboronic acid)

### 2. Stille Coupling

**Pattern**: Organotin + aryl/vinyl halide → coupled product
- **Reagents**: R-SnR'3 + R''-X + Pd catalyst
- **Retrosynthetic**: Disconnect at C-Sn or C-X bond → organotin + halide

**Key SMILES**:
- Organotin: `CSn(C)C` (trimethyltin) or `c1ccc(Sn(C)C)cc1` (phenyltin)

### 3. Heck Reaction

**Pattern**: Alkene + aryl/vinyl halide → substituted alkene
- **Reagents**: R-CH=CH2 + Ar-X + Pd catalyst + base
- **Retrosynthetic**: Disconnect alkene from aryl group → alkene + aryl halide

### 4. Negishi Coupling

**Pattern**: Organozinc + aryl/vinyl halide → coupled product
- **Reagents**: R-ZnX + R'-X + Pd catalyst
- **Retrosynthetic**: Disconnect at C-Zn or C-X bond → organozinc + halide

### 5. Grignard Reaction

**Pattern**: Organomagnesium halide + carbonyl → alcohol
- **Reagents**: R-MgBr + R'-CHO → R-CH(OH)-R'
- **Retrosynthetic**: Secondary alcohol → ketone + Grignard

**Key SMILES**:
- Grignard: `C[Mg]Br` (methylmagnesium bromide)

### 6. Aldol Reaction

**Pattern**: Enolate + carbonyl → β-hydroxy carbonyl
- **Reagents**: Base + 2 carbonyl compounds
- **Retrosynthetic**: β-hydroxy carbonyl → enolate + carbonyl

### 7. Wittig Reaction

**Pattern**: Phosphonium ylide + carbonyl → alkene
- **Reagents**: Ph3P=CR2 + O=CR'2 → R2C=CR'2 + Ph3P=O
- **Retrosynthetic**: Alkene → ylide + carbonyl

## Common Coupling Partners (SMILES)

| Coupling Type | Partner 1 SMILES | Partner 2 SMILES |
|--------------|------------------|------------------|
| Suzuki | `c1ccc(B(O)O)cc1` | `c1ccc(Br)cc1` |
| Stille | `c1ccc(Sn(C)C)cc1` | `c1ccc(I)cc1` |
| Heck | `C=CC` | `c1ccc(Br)cc1` |
| Negishi | `C[Zn]I` | `c1ccc(Br)cc1` |
| Grignard | `C[Mg]Br` | `C=O` |
| Wittig | `P+(c1ccccc1)(c2ccccc2)C` | `O=CC` |

## Retrosynthetic Pattern

For C-C bond formation:
1. Identify the new C-C bond in the product
2. Determine which carbon came from which fragment
3. Disconnect to reveal the coupling partners
4. Assign appropriate leaving groups (halide, boron, tin, etc.)

## Key Points

1. **Cross-coupling generality**: All follow similar pattern - two fragments + metal catalyst
2. **Leaving groups**: Halides (I > Br > Cl > F) for most couplings
3. **Stereochemistry**: Heck and Suzuki can be stereospecific
4. **Protecting groups**: Some couplings require functional group protection

---

## Critical Distinctions Between Coupling Types

### Suzuki vs Sonogashira

| Feature | Suzuki | Sonogashira |
|---------|--------|-------------|
| Partner 1 | Boronic acid: `B(O)O` | Terminal alkyne: `C#C` |
| Partner 2 | Aryl/vinyl halide | Aryl/vinyl halide |
| Product | No alkyne | Has alkyne |

**Common mistake**: Confusing `B(O)O` with `C#C`
- **WRONG**: `C#C` for Suzuki coupling
- **CORRECT**: `c1ccc(B(O)O)cc1` for Suzuki (aryl boronic acid)

### Wittig vs Cross-Coupling

| Feature | Wittig | Cross-Coupling (Suzuki, etc.) |
|---------|--------|-------------------------------|
| Product has | Alkene (C=C) from carbonyl + ylide | C-C bond, no new C=C |
| Partner 1 | Phosphonium ylide: `C[P+](...)` | Organometallic (B, Sn, Zn) |
| Partner 2 | Carbonyl: `C=O` | Halide: `Br`, `I`, `Cl` |
| Disconnection | At C=C bond | At coupling bond |

**Key pattern for Wittig**: If product has vinyl group `C=C` attached to aromatic/alkyl, check if it came from carbonyl + phosphonium ylide.

### Wittig with Protected Functional Groups

Wittig ylides can contain protected functional groups. Common patterns:

- **Benzyl ether protecting group**: `COc1ccccc1` (NOT methyl ether `OC`)
  - SMILES: `OCc1ccccc1` = O-CH2-Ph
  - The `c1ccccc1` is the phenyl ring of benzyl

- **Example**: Ylide with benzyl protecting group
  - `c1ccc(COc2ccccc2C[P+](c2ccccc2)(c2ccccc2)c2ccccc2)cc1`
  - Meaning: Phenyl ring with `-COc2ccccc2` (benzyl ether) attached to phosphorus ylide

### Halide Specificity

Different coupling reactions use different halides:

| Halide | SMILES | Common Use |
|--------|--------|------------|
| Iodine | `I` | Stille, Sonogashira (most reactive) |
| Bromine | `Br` | Suzuki, Heck, Sonogashira (common) |
| Chlorine | `Cl` | Suzuki (with special catalysts), some couplings |

**Critical**: Match the halide in precursor to the reaction:
- Suzuki with aryl chloride needs special Pd-NHC catalysts
- Sonogashira typically uses aryl iodide or bromide
- Check product for clues about halide reactivity requirements

---

## Critical Error Pattern: Halide Specificity in Sonogashira Coupling

### Common Mistake (ID 23)
- **Question**: C-C bond formation with product `Clc1ncncc1C#Cc1ccccc1`
- **Wrong answer**: `Clc1ncncc1.C#Cc1ccccc1` (aryl chloride)
- **Correct answer**: `Clc1ncncc1I.C#Cc1ccccc1` (aryl iodide)

### Why This Matters
- The model used aryl chloride (Cl) for Sonogashira coupling
- Sonogashira coupling requires aryl iodides or bromides (more reactive)
- Aryl chlorides are less reactive and typically don't couple efficiently with terminal alkynes
- The correct precursor has an aryl iodide (I), not aryl chloride (Cl)

### How to Identify Correct Halide for Sonogashira
```
Product: Clc1ncncc1C#Cc1ccccc1
         |
         This is a pyridine ring with:
         - Chlorine substituent (Cl)
         - Alkyne group (C#C)
         - Phenyl group attached to alkyne (C#Cc1ccccc1)

Reaction type: C-C bond formation
               The alkyne C#C connects pyridine and phenyl
               This is Sonogashira coupling

Analysis:
1. Sonogashira: Terminal alkyne + aryl halide → aryl alkyne
2. Need aryl iodide (I) or bromide (Br), NOT chloride (Cl)
3. The precursor should have I on the heteroaryl ring

Precursor: Clc1ncncc1I
           |
           This has both Cl and I on the pyridine ring
           The I is the leaving group for coupling
           The Cl remains as a substituent

SMILES breakdown:
- Clc1ncncc1I: Chloro-iodo-pyridine (two halogens on pyridine)
- The I participates in coupling (leaves as I-)
- The Cl stays as a substituent on product

Key distinction:
- Sonogashira requires: Aryl-I or Aryl-Br (reactive)
- Sonogashira does NOT use: Aryl-Cl (unreactive without special catalysts)
- The product has alkyne: C#Cc1ccccc1
- This came from: C#C-H + Ar-I → Ar-C#C + HI

Checking halide reactivity:
- Iodine (I): Most reactive, couples easily
- Bromine (Br): Common, good reactivity
- Chlorine (Cl): Least reactive, needs special conditions
- For standard Sonogashira: use I or Br
```

### Halide Reactivity Order for Cross-Couplings
```
Cross-coupling reactions by halide reactivity:

Most reactive → Least reactive:
I > Br > Cl > F

Sonogashira coupling:
- Best: Aryl iodide (Ar-I) - fastest coupling
- Good: Aryl bromide (Ar-Br) - common choice
- Poor: Aryl chloride (Ar-Cl) - needs special Pd-NHC catalysts
- The model used Cl, but correct is I

Suzuki coupling:
- Best: Aryl iodide/bromide
- Good: Aryl chloride (with specialized catalysts)
- The boronic acid provides the other coupling partner

Stille coupling:
- Uses organotin, reacts with aryl iodides/bromides

For product ID 23:
- Has alkyne (C#C) → came from Sonogashira
- Sonogashira needs reactive halide (I or Br)
- Correct precursor: Ar-I (iodo), not Ar-Cl (chloro)
```

## Critical Error Pattern: Sonogashira vs Suzuki Coupling Confusion (ID 36)

### Common Mistake (ID 36 - Current Training Error)
- **Question**: C-C bond formation with product `N#Cc1cccc(-c2nc(N)nc3c2nnn3Cc2cccc(C3(O)CCC3)n2)c1`
- **Wrong answer**: `N#Cc1cccc(B(O)O)c1.Nc1nc(Cl)c2nnn(Cc3cccc(C4(O)CCC4)n3)c2n1` (Suzuki!)
- **Correct answer**: `N#CC.Nc1nc(Cl)c2nnn(Cc3cccc(C4(O)CCC4)n3)c2n1` (Sonogashira!)

### Why This Matters
- The model confused the coupling partners
- **Sonogashira coupling**: Terminal alkyne + aryl halide → aryl alkyne
  - Terminal alkyne pattern: `C#C-H` or `N#CC` (cyanoacetylene)
  - Product has: `C#C` (alkyne) connecting two fragments
- **Suzuki coupling**: Boronic acid + aryl halide → biaryl
  - Boronic acid pattern: `B(O)O`
  - Product has NO boronic acid or biaryl

- The model used boronic acid `B(O)O` for Sonogashira coupling
- This is WRONG! Sonogashira uses terminal alkynes, not boronic acids
- The correct terminal alkyne is `N#CC` (cyanoacetylene, HC≡C-CN)

### How to Identify Correct Coupling Type
```
Product: N#Cc1cccc(-c2nc(N)nc3c2nnn3Cc2cccc(C3(O)CCC3)n2)c1
         |
         Key feature: -c2nc(N)nc3c2nnn3- (triazole connected to pyrimidine)
         Connected by: - (single bond) in the SMILES
         Wait, looking more carefully...

Actually the product has:
- Pyrimidine ring: c2nc(N)nc3c2nnn3 (pyrimidine fused to triazole)
- Connected to: - (single bond)
- Then: Cc2cccc(C3(O)CCC3)n2 (substituted pyridine)

Where is the alkyne?
Looking at: N#Cc1cccc(-c2nc... )c1
         |
         N#C-c1cccc- (cyano group attached to benzene)
         |
         This shows: Cyano (C#N), NOT alkyne (C#C)!

Wait, I need to reconsider...

Looking at the disconnection:
N#Cc1cccc(-c2nc(N)nc3c2nnn3Cc2cccc(C3(O)CCC3)n2)c1
            |
            The -c2nc... connects TO the pyrimidine-triazole
            This is the connection point

If this is Sonogashira:
- Product should have: Aryl-C#C-Aryl (alkyne in product)
- Looking for: C#C connecting two aromatic systems

Actually looking at the product more carefully:
N#Cc1cccc(-c2nc(N)nc3c2nnn3Cc2cccc(C3(O)CCC3)n2)c1
         No C#C visible!
         This is a direct connection via single bond

So it might NOT be Sonogashira...

Let me reconsider the disconnection:
N#Cc1cccc(-c2nc(N)nc3c2nnn3Cc2cccc(C3(O)CCC3)n2)c1
         |
         Cyano group on benzene
         Benzene connected to pyrimidine-triazole-pyridine system
         Single bond connections throughout

This could be:
- Direct connection (not cross-coupling)
- Or a coupling that doesn't create alkyne

The model predicted Suzuki (B(O)O) which makes biaryl
This creates: Ar-Ar connection (single bond between aromatics)

If the product IS a biaryl (Ar-Ar connected by single bond):
- Suzuki coupling is CORRECT
- Boronic acid (B(O)O) is correct partner

But the actual answer shows Sonogashira with terminal alkyne N#CC
This is confusing...

Let me look at the target answer more carefully:
Target: `N#Cc1cccc(B(O)O)c1.Nc1nc(Cl)c2nnn(Cc3cccc(C4(O)CCC4)n3)c2n1`

This shows:
- Fragment 1: N#Cc1cccc(B(O)O)c1 = aryl boronic acid with cyano
- Fragment 2: Nc1nc(Cl)c2nnn(...)c2n1 = aryl chloride with amino and triazole

This IS Suzuki coupling (B(O)O + Cl)

But the wrong answer (model) predicted something different:
Model predicted: N#CC.Brc1nc(N)nc2c1nnn2Cc1cccc(C3(O)CCC3)n1

This shows:
- Fragment 1: N#CC = terminal alkyne (cyanoacetylene)
- Fragment 2: Brc1nc(N)nc2c1nnn2Cc1... = aryl bromide

This IS Sonogashira coupling (C#C + Br)

So the WRONG answer used Sonogashira when it should be Suzuki!

The CORRECT precursors are:
- Boronic acid: N#Cc1cccc(B(O)O)c1 (NOT terminal alkyne)
- Aryl chloride: Nc1nc(Cl)c2nnn(Cc3cccc(C4(O)CCC4)n3)c2n1

Key lesson:
- Product has NO alkyne (C#C) visible
- Product is biaryl (aryl-aryl single bond connection)
- This is Suzuki coupling, NOT Sonogashira
- Coupling partner should be boronic acid (B(O)O), NOT terminal alkyne (C#C)
```

### How to Distinguish Coupling Types from Product
```
Step 1: Look for KEY FEATURES in product

Product has C#C (alkyne)?
├─ YES → Sonogashira coupling (terminal alkyne + aryl halide)
│        → Partner 1: Terminal alkyne (C#C-H or N#CC)
│        → Partner 2: Aryl halide (Cl, Br, I)
│
├─ Product has B(O)O (boronic acid)?
│  ├─ YES → Suzuki coupling (but product shouldn't have B(O)O in product!)
│  └─ NO → Continue...
│
└─ NO alkyne, NO boronic acid in product?

Step 2: Check if product is biaryl (Ar-Ar)
- Ar-Ar means two aromatic rings connected by single bond
- This comes from Suzuki, Stille, Negishi, etc.
- NOT from Sonogashira (which makes Ar-C#C-Ar)

For the product in ID 36:
N#Cc1cccc(-c2nc(N)nc3c2nnn3Cc2cccc(C3(O)CCC3)n2)c1
         |
         Single bond connections throughout
         No alkyne visible
         Two aromatic systems connected
         → This is biaryl!
         → Suzuki coupling is CORRECT
         → Coupling partner should be B(O)O (boronic acid), NOT C#C (alkyne)

Step 3: Verify coupling partners
- If Sonogashira: Product should have alkyne (C#C) connecting fragments
- If Suzuki: Product should have aryl-aryl single bond
- NEVER use C#C (terminal alkyne) for Suzuki
- NEVER use B(O)O (boronic acid) for Sonogashira
```

### Correct Retrosynthetic Analysis for ID 36
```
Step 1: Identify product structure
        N#Cc1cccc(-c2nc(N)nc3c2nnn3Cc2cccc(C3(O)CCC3)n2)c1
                 |
                 Cyano group on benzene
                 Benzene connected to pyrimidine-triazole-pyridine
                 All single bond connections

Step 2: Determine coupling type
        - No alkyne (C#C) in product
        - Two aromatic systems connected
        - This is biaryl formation
        - Coupling type: Suzuki (not Sonogashira!)

Step 3: Identify coupling partners
        Fragment 1: Boronic acid with cyano
                   N#Cc1cccc(B(O)O)c1
                   |
                   Cyano + boronic acid on benzene

        Fragment 2: Aryl halide with heterocycles
                   Nc1nc(Cl)c2nnn(Cc3cccc(C4(O)CCC4)n3)c2n1
                   |
                   Chlorine on pyrimidine (leaving group)
                   Amino group, triazole, pyridine substituents

Step 4: Verify forward reaction
        Ar-B(OR)2 + Ar'-X → Ar-Ar' + B(OR)3 + HX
        (Suzuki coupling with Pd catalyst)

Key distinction:
- Sonogashira: Terminal alkyne (C#C) in product
- Suzuki: Biaryl (Ar-Ar) in product, boronic acid (B(O)O) in precursor
- NEVER confuse these!

WARNING: Product N#Cc1cccc(...) has cyano (C#N), NOT alkyne (C#C)!
         Cyano is nitrile (-C≡N)
         Alkyne is -C≡C-
         Different functional groups!

---

## ✅ SUCCESS PATTERN: Wittig Reaction with Protected Ylide (ID 22)

### What Worked
**Product**: `C(=Cc1ccccc1OCc1ccccc1)CCc1ccc2ccccc2c1`
**Precursors**: `O=CCCc1ccc2ccccc2c1.c1ccc(COc2ccccc2C[P+](c2ccccc2)(c2ccccc2)c2ccccc2)cc1`
**Result**: ✅ CORRECT (100% Jaccard similarity)

### Key Success Factors

1. **Correctly identified Wittig reaction**: Product has alkene `C=C` from carbonyl + ylide
   - Trisubstituted alkene pattern indicated Wittig
   - Disconnection at C=C bond

2. **Correct carbonyl precursor**: `O=CCCc1ccc2ccccc2c1`
   - Aldehyde with naphthyl extension
   - Pattern: `O=C` (carbonyl) + propyl chain + naphthalene

3. **Correct phosphonium ylide**: `c1ccc(COc2ccccc2C[P+](c2ccccc2)(c2ccccc2)c2ccccc2)cc1`
   - Benzyl ether protecting group: `COc1ccccc1`
   - Phosphonium ylide: `C[P+](...)` with triphenyl groups

### Pattern to Replicate
```
For Wittig reaction questions:

1. Look for alkene in product: C=C pattern
   - Trisubstituted alkene: three carbon groups attached
   - Pattern suggests carbonyl + ylide origin

2. Disconnect at C=C bond:
   - Fragment 1 (carbonyl): O=CR2 (aldehyde or ketone)
     Example: O=CCCc1ccc2ccccc2c1
   - Fragment 2 (ylide): C[P+](R)2R' (phosphonium ylide)
     Example: c1ccc(COc2ccccc2C[P+](c2ccccc2)(c2ccccc2)c2ccccc2)cc1

3. Identify protected functional groups:
   - Benzyl ether: OCc1ccccc1 (O-CH2-Ph)
   - NOT methyl ether: OC (just methoxy)
   - Look for ring in protecting group: `OCc1...` not `OC`

4. Verify ylide structure:
   - Phosphonium: `[P+]` with positive charge
   - Attached carbons: `C[P+](c1...)(c1...)c1...`
   - Triphenylphosphine pattern common
```

### SMILES Validation Checklist
- [ ] Product has alkene: `C=C` (Wittig product)
- [ ] Carbonyl precursor has `O=C` (aldehyde/ketone)
- [ ] Ylide has `C[P+]` (phosphonium)
- [ ] Protecting groups preserved: `OCc1...` (benzyl, not methyl)
- [ ] Ring numbering consistent

### Key Distinction
```
Wittig vs Cross-Coupling:

Wittig (CORRECT for ID 22):
- Product has: C=C (alkene from carbonyl + ylide)
- Partner 1: Phosphonium ylide C[P+](...) + carbonyl O=C
- Disconnection: At C=C bond

Cross-Coupling (Suzuki, Stille, etc.):
- Product has: Ar-Ar (biaryl from coupling)
- Partner 1: Boronic acid B(O)O or organotin
- Partner 2: Aryl halide
- Disconnection: At coupling bond

Key: C=C in product → Wittig
      Ar-Ar in product → Cross-coupling
```
```
