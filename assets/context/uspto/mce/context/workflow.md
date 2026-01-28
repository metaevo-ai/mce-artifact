# Retrosynthesis Decision Workflow

## Step 1: Identify Reaction Type from Context

The question begins with "Context: The reaction type is ___". Use this to select your approach:

| Reaction Type | Key Pattern to Find | Typical Precursors |
|--------------|---------------------|-------------------|
| FGA | New functional group added | Alkyl halide + nucleophile |
| FGI | Same skeleton, functional group changed | Converted group + reagent |
| C-C bond formation | New C-C bond | Two coupling partners |
| Heteroatom alkylation | New C-N, C-O, or C-S bond | Nucleophile + electrophile |
| Heterocycle formation | New ring system | Cyclization precursors |
| Deprotection | Protecting group removed | Protected precursor |

## Step 2: Analyze Product SMILES Structure

### 2a. Identify Key Structural Features

For the product SMILES, identify:
- **Functional groups**: carbonyls (C=O), azides (N=[N+]=[N-]), halides (Cl, Br, I), heteroatoms (N, O, S)
- **Connectivity**: Ring systems, chain branches, substitution patterns
- **Key bonds**: Where was the bond formed?

### 2b. Map Atom Positions Carefully

**Critical**: When analyzing multi-substituted rings, track which positions have which substituents:

```
Example: N#Cc1ccc(CBr)cc1Br
         Position 1: C#N (attachment point)
         Position 2-3: cc (ring carbons)
         Position 4: CBr (bromomethyl)
         Position 5: Br (bromine on ring)

NOT: N#Cc1ccc(Br)cc1CBr (wrong positions!)
```

### 2c. Count Ring Closures

Verify ring numbers match actual connectivity:
- `c1...c1` = same ring
- `c1...c2...c2` = fused ring system
- Each `1`, `2`, `3` must have a matching closure

## Step 3: Apply Reaction-Specific Pattern

### For FGA (Thioether Formation):
1. Look for: C-S-C pattern in product
2. Disconnect: Break C-S bond
3. Identify precursors:
   - Fragment 1: Alkyl halide (Cl-R or Br-R) where R has the halogen on the carbon
   - Fragment 2: Thiol (R'-SH) or equivalent
4. **Critical check**: Halide position
   - Benzyl chloride: `ClCc1ccccc1` (Cl on CH2, attached to ring)
   - NOT: `c1ccc(Cl)cc1` (Cl directly on ring)

### For FGI (Functional Group Interconversion):
1. Identify: What group changed?
2. Verify: Position of new vs old group
3. Common patterns:
   - Ketone → gem-diol: C(=O) → C(O) (add H2O)
   - Ester → amide: C(=O)OC → C(=O)N + N (add ammonia)
4. **Critical check**: Which carbon has the carbonyl/hydroxy?
   - Trace connectivity carefully through ring systems
   - Count atoms from attachment point

### For C-C Bond Formation:
1. Identify: What coupling created the bond?
   - Has alkyne (C#C)? → Sonogashira coupling
   - Has boronic acid (B(O)O)? → Suzuki coupling
   - Has vinyl (C=C)? → Heck or Wittig
2. Find coupling partners:
   - Sonogashira: Terminal alkyne + aryl halide
   - Suzuki: Boronic acid + aryl halide
3. **Critical check**: Alkyne vs Boronic Acid
   - Terminal alkyne: `C#C-H` or `N#CC` (cyanoacetylene)
   - Boronic acid: `B(O)O` pattern
   - NEVER confuse these!

### For Heteroatom Alkylation:
1. Look for: C-N, C-O, or C-S bond formation
2. Disconnect: Break the heteroatom bond
3. Identify: Nucleophile + electrophile with leaving group
4. **Critical check for N-methylation**: Only remove the methyl group that was ADDED
   - N-methyl: `n(C)c` → `[nH]` (remove methyl, show N-H)
   - Aromatic methoxy: `cc1OC` → KEEP (part of parent scaffold)
   - ❌ WRONG: Demethylating aromatic ethers (OC → O)
   - ✅ CORRECT: Only N-methyl is removed, aromatic methyl ethers stay
   - Reagent: Methyl iodide (CI)

### For Heterocycle Formation:
1. Identify: What heterocycle? (pyrrole, thiazole, oxadiazole, etc.)
2. Match: Standard synthesis pattern
   - Paal-Knorr pyrrole: 1,4-diketone + amine (NO O in ring!)
   - Hantzsch thiazole: thioamide + α-halo carbonyl
   - 1,3,4-Oxadiazole: nitrile + acyl compound (HAS O in ring!)
3. Find: Cyclization precursors

**⚠️ CRITICAL ERROR CHECK - Heterocycle Type**:
```
Did you check for OXYGEN in the ring?
├─ YES: "oc" or "co" pattern → 1,3,4-Oxadiazole (nitrile cyclization)
└─ NO: "nnn" pattern → 1,2,4-Triazole (different precursors!)

Common mistake: Confusing oxadiazole (has O) with triazole (no O)
Product: c1ccc(-c2nc(CCCCCCc3nnn[nH]3)oc2-...)cc1
         |
         "oc" = O-C = OXYGEN in ring → OXADIAZOLE
         NOT triazole (which has "nnn", no oxygen)
```

### For Deprotection:
1. Identify: What protecting group? (benzyl, Boc, etc.)
2. Recall: Protected form is the precursor
3. Forward: Protection; Retro: Add protecting group back

**⚠️ CRITICAL ERROR CHECK - Ester vs Carboxylic Acid**:
```
For amide formation retrosynthesis:
├─ Product has: C(=O)N (amide)
└─ Precursor should be: C(=O)OC (ESTER) NOT C(=O)O (ACID!)

Check the atom AFTER carbonyl oxygen:
├─ If C (carbon): ESTER ✓ (correct precursor)
└─ If nothing/end: CARBOXYLIC ACID ✗ (wrong!)

Example: CC(=O)OC = methyl ester (CH3-CO-O-CH3)
         CC(=O)O  = acetic acid  (CH3-CO-OH)
```

**⚠️ CRITICAL ERROR CHECK - Methyl Group Position**:
```
For FGA bromination questions:
├─ Product has: CBr (bromomethyl) on heterocycle
└─ Precursor has: Cc1c... (methyl CH3 on heterocycle carbon 1)

Check SMILES notation:
├─ Cc1c... = methyl attached to position 1 ✓
└─ c1c...  = hydrogen at position 1 ✗ (missing methyl!)

Example: Cc1c(CBr)c(...)nc2cc(Cl)ccc12
         |
         Leading Cc1 = methyl on heterocycle carbon 1
         NOT C[C@H](NC(=O)c1c(C)c(...)) which is wrong position
```

## Step 4: Verify SMILES Syntax

Before finalizing:

### 4a. Check Atom Connectivity
- [ ] All atoms properly connected?
- [ ] Parentheses balanced?
- [ ] Ring closures numbered correctly?

### 4b. Verify Functional Group Position
- [ ] Halide on correct atom (benzylic vs aromatic)?
- [ ] Carbonyl on correct ring carbon?
- [ ] Heteroatoms in right positions?

### 4c. Confirm Reaction Logic
- [ ] Would these precursors react to give product?
- [ ] Leaving groups appropriate?
- [ ] Coupling partners chemically compatible?

## Step 5: Format Answer

- Separate precursors with periods (`.`)
- No spaces around periods
- Match SMILES notation from similar examples in training data

## Quick Reference Flowchart

```
Is product an alkyne (C#C)?
├─ YES → Sonogashira coupling
│        → Partner 1: Terminal alkyne (C#C)
│        → Partner 2: Aryl halide (Cl, Br, I)
│
├─ NO → Does product have boronic acid (B(O)O)?
│       ├─ YES → Suzuki coupling
│       │       → Partner 1: Boronic acid
│       │       → Partner 2: Aryl halide
│       │
│       ├─ NO → Is this Heterocycle Formation?
│       │       ├─ YES → Does ring have "oc" or "co" (O + N)?
│       │       │       ├─ YES → 1,3,4-Oxadiazole (nitrile cyclization)
│       │       │       └─ NO → Check for "nnn" (triazole) or other
│       │       └─ NO → Is this FGA/FGI/Deprotection?
│       │               ├─ FGA → Identify added group, find nucleophile + electrophile
│       │               ├─ FGI → Is it amide formation?
│       │               │       ├─ YES → Ester C(=O)OC NOT acid C(=O)O!
│       │               │       └─ NO → Other FGI patterns
│       │               └─ Deprotection → Add protecting group back

⚠️ CRITICAL CHECKS BEFORE SUBMITTING:
1. Heterocycle: Does it have O (oxadiazole "oc") or just N (triazole "nnn")?
2. Amide FGI: Precursor is C(=O)OC (ester) NOT C(=O)O (acid)!
3. FGA bromination: Methyl is Cc1c... NOT c1c... (missing methyl)!

🚨 WILLIAMSON ETHER CRITICAL CHECK (ID 5 Error):
   1. Is the nucleophile PHENOL (O on aromatic) or KETONE (c(=O))?
      - Phenol: "O" at end of aromatic = Ar-OH (CORRECT)
      - Ketone: "c(=O)" = Ar-C=O (WRONG for Williamson!)
   2. Is the halide BENZYL (CBr on ring) or ALKYL (Br on chain)?
      - Benzyl: CBr attached to aromatic = Ar-CH2-Br (CORRECT)
      - Alkyl: Br-CC = wrong position (WRONG!)
```
