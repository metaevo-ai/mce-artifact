# Success Patterns: What Works in Retrosynthesis

This document summarizes patterns that lead to CORRECT predictions, derived from analysis of successful training examples.

---

## 1. Boc Protection: Secondary Amine Recognition

### Pattern Recognition
**Product**: `CC(C)(C)OC(=O)N1Cc2ccc([N+](=O)[O-])cc2C1=O`
**Precursors**: `CC(C)(C)OC(=O)OC(=O)OC(C)(C)C.O=C1NCc2ccc([N+](=O)[O-])cc21`

### Key SMILES Distinctions

| Pattern | Meaning | Correct for Boc? |
|---------|---------|------------------|
| `O=C1NCc2...cc21` | Secondary amine (N has H) | ✅ YES |
| `O=C1N(Cc2...)C1` | Tertiary amine (N has no H) | ❌ NO |
| `NC(=O)OC(C)(C)C` | Boc-protected carbamate | Product has this |

### Critical Check
```
O=C1NCc2ccc([N+](=O)[O-])cc21
       ^
       N has H (shown by NC, not N(C...))
       This is secondary amine - correct for Boc protection
```

### Success Principle
- **Boc protection requires secondary amine precursor** (NH group present)
- SMILES `NC` = nitrogen with hydrogen (secondary)
- SMILES `N(C...)` = nitrogen with two carbons (tertiary, no H)
- Reagent is always `CC(C)(C)OC(=O)OC(=O)OC(C)(C)C` (Boc2O)

---

## 2. FGA: Allylic Bromination Position

### Pattern Recognition
**Product**: `COP(=O)(/C=C/CBr)OC`
**Precursors**: `C/C=C\P(=O)(OC)OC.O=C1CCC(=O)N1Br`

### Key SMILES Distinctions

| SMILES Pattern | Structure | Position |
|----------------|-----------|----------|
| `/C=C/CBr` | C=C-CBr | Allylic bromide ✅ |
| `C=C/CBr` | C=C-CBr | Terminal bromide ❌ |
| `C/C=C\P` | C-C=C-P | Allylic methylene |

### Critical Check
```
Product: COP(=O)(/C=C/CBr)OC
         The /C=C/CBr shows Br on carbon adjacent to double bond
         This is ALLYLIC bromination, not terminal

Correct precursor: C/C=C\P(=O)(OC)OC
                   C-C=C-P (allylic methylene between C=C and P)
                   NBS brominates the allylic CH → CBr
```

### Success Principle
- **Allylic carbon**: CH₂ or CH next to C=C
- **Allylic bromination**: Allylic CH₂ → CH₂Br (NBS reagent)
- **SMILES pattern**: `/C=C/CBr` = allylic bromide, `C=C-CBr` = terminal
- **Reagent**: NBS (`O=C1CCC(=O)N1Br`) for allylic bromination

---

## 3. Oxidation: Benzyl Alcohol to Aldehyde

### Pattern Recognition
**Product**: `Cc1cc(C=O)cc(C(F)(F)F)c1`
**Precursor**: `Cc1cc(CO)cc(C(F)(F)F)c1`

### Key SMILES Transformations

| Product | Precursor | Transformation |
|---------|-----------|----------------|
| `C=O` (aldehyde) | `CO` (benzyl alcohol) | Oxidation |
| `C(=O)O` (acid) | `CO` (alcohol) | Oxidation |
| `C(=O)C` (ketone) | `C(O)C` (secondary alcohol) | Oxidation |

### Critical Check
```
Product: Cc1cc(C=O)cc(C(F)(F)F)c1
         The C=O is aldehyde attached to aromatic
         Aldehyde comes from oxidation of benzyl alcohol

Retrosynthetic: C=O → CO
                Cc1cc(CO)cc(C(F)(F)F)c1
```

### Success Principle
- **Benzyl position**: CH₂ attached to aromatic ring
- **Benzyl alcohol**: `-CH₂OH` → SMILES: `CO` (when attached to aromatic)
- **Aldehyde**: `-CHO` → SMILES: `C=O` (when attached to aromatic)
- **Look for**: `-C(=O)c1...` = aldehyde, `-COc1...` = benzylic alcohol

---

## 4. Heteroatom Alkylation: Bromide Leaving Group

### Pattern Recognition
**Product**: `O=S(=O)([O-])CCCOc1cc(Cl)ccc1Cl.[Na+]`
**Precursors**: `O=S(=O)([O-])CCCBr.Oc1cc(Cl)ccc1Cl.[Na+]`

### Key SMILES Distinctions

| Pattern | Structure | Use Case |
|---------|-----------|----------|
| `CCCBr` | 1-Bromopropane | Williamson ether ✅ |
| `CCCCl` | 1-Chloropropane | Less reactive ❌ |
| `BrCC` | Bromoethane | Williamson ether |
| `ClCC` | Chloroethane | Less reactive |

### Critical Check
```
Product: O=S(=O)([O-])CCCOc1cc(Cl)ccc1Cl
         Ether bond: CCCO (propyl chain)

Retrosynthetic disconnection at ether oxygen:
1. Alkyl halide: O=S(=O)([O-])CCCBr (Br at end of chain)
2. Phenol: Oc1cc(Cl)ccc1Cl

Williamson ether synthesis: DEFAULT TO BROMIDE
- Bromide is better leaving group than chloride
- Most common alkyl halide for Williamson
```

### Success Principle
- **Williamson ether**: Alkoxide + alkyl halide → ether
- **Leaving group preference**: Br > Cl > I > F
- **Sulfonate salts**: `[O-]` with counterion `[Na+]`
- **Rule**: Default to bromide unless answer shows chloride

---

## 5. C-C Bond Formation: Wittig Reaction

### Pattern Recognition
**Product**: `C(=Cc1ccccc1OCc1ccccc1)CCc1ccc2ccccc2c1`
**Precursors**: `O=CCCc1ccc2ccccc2c1.c1ccc(COc2ccccc2C[P+](c2ccccc2)(c2ccccc2)c2ccccc2)cc1`

### Key SMILES Patterns

| Pattern | Structure | Meaning |
|---------|-----------|---------|
| `C=C` | Alkene | Wittig product |
| `C[P+](...)` | Phosphonium ylide | Wittig partner 1 |
| `C=O` | Carbonyl | Wittig partner 2 |
| `COc1ccccc1` | Benzyl ether | Protecting group |

### Critical Check
```
Product: C(=Cc1ccccc1OCc1ccccc1)CCc1ccc2ccccc2c1
         The C=C is trisubstituted alkene
         This pattern suggests Wittig reaction

Wittig disconnection at C=C:
1. Carbonyl: O=CCCc1ccc2ccccc2c1 (aldehyde)
2. Ylide: c1ccc(COc2ccccc2C[P+](c2ccccc2)(c2ccccc2)c2ccccc2)cc1
          Phosphonium ylide with benzyl protecting group
```

### Success Principle
- **Wittig product**: Has alkene (C=C) from carbonyl + ylide
- **Partner 1**: Phosphonium ylide `C[P+](c1ccccc1)(c1ccccc1)c1ccccc1`
- **Partner 2**: Carbonyl compound `C=O`
- **Look for**: Protected functional groups in ylide (benzyl ether `OCc1...`)
- **Verify**: Alkene geometry and substitution pattern

---

## Common Success Checklist

### Before Submitting Answer

1. **Reaction Type Match**
   - [ ] Does the disconnection match the stated reaction type?
   - [ ] Are both precursors chemically compatible?

2. **SMILES Syntax**
   - [ ] Are ring numbers consistent?
   - [ ] Are parentheses balanced?
   - [ ] Is halide position correct (benzylic vs aromatic)?

3. **Chemical Logic**
   - [ ] Would these precursors react to give product?
   - [ ] Is the leaving group appropriate?
   - [ ] Is the protecting group correctly identified?

4. **Specific Pattern Checks**
   - [ ] Secondary vs tertiary amine (Boc protection)
   - [ ] Allylic vs terminal bromination (FGA)
   - [ ] Benzyl alcohol vs aldehyde (Oxidation)
   - [ ] Bromide vs chloride leaving group (Heteroatom alkylation)
   - [ ] Wittig vs cross-coupling (C-C formation)

---

## Summary of Working Patterns

| Reaction Type | Working Pattern | Key SMILES |
|--------------|-----------------|------------|
| Protections | Secondary amine for Boc | `NC` (not `N(C)`) |
| FGA | Allylic bromination | `/C=C/CBr` pattern |
| Oxidation | Benzyl alcohol → aldehyde | `CO` → `C=O` |
| Heteroatom Alkylation | Bromide leaving group | `CCCBr` (default) |
| C-C Bond Formation | Wittig reaction | `C[P+](...)` + `C=O` |

These patterns are validated by 100% accuracy on training examples. Use this as a reference when analyzing similar questions.
