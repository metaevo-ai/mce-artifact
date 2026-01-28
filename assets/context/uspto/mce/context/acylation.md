# Retrosynthesis Guide: Acylation

## Overview

Acylation reactions introduce acyl groups (R-C=O) to form amides, esters, or anhydrides. The key feature is formation of a new carbonyl-oxygen or carbonyl-nitrogen bond.

## Common Acylation Patterns

### 1. Amide Formation

**From acyl chloride**
- **Pattern**: R-COCl + R'NH2 → R-CONHR' + HCl
- **Retrosynthetic**: R-CONHR' → R-COCl + H2NR'

**From carboxylic acid**
- **Pattern**: R-COOH + R'NH2 → R-CONHR' + H2O
- **Requires**: Coupling agent (DCC, EDC, HATU)

**From ester**
- **Pattern**: R-COOR'' + R'NH2 → R-CONHR' + R''OH
- **Requires**: Excess amine or catalysis

### 2. Ester Formation

**From acyl chloride**
- **Pattern**: R-COCl + R'OH → R-COOR' + HCl

**From acid**
- **Pattern**: R-COOH + R'OH → R-COOR' + H2O
- **Requires**: Acid catalyst (H2SO4) or coupling agent

**From anhydride**
- **Pattern**: R-CO-O-CO-R + R'OH → R-COOR' + R-COOH

### 3. Anhydride Formation

**From acyl chloride**
- **Pattern**: R-COCl + R-COO-Na → R-CO-O-CO-R + NaCl

**From acid dehydration**
- **Pattern**: 2 R-COOH → R-CO-O-CO-R + H2O
- **Requires**: Heat, dehydrating agents

## Common Acylating Agents (SMILES)

| Reagent | SMILES | Use |
|---------|--------|-----|
| Acetyl chloride | `CC(=O)Cl` | Acetylation |
| Benzoyl chloride | `O=C(Cl)c1ccccc1` | Benzoylation |
| Acetic anhydride | `CC(=O)OC(=O)C` | Acetylation |
| Acetic acid | `CC(=O)O` | Acylation (with catalyst) |
| DCC | `C1CCCN2C1=NCC2=N` | Coupling agent |

## Retrosynthetic Pattern

For acylation reactions, break the carbonyl-nitrogen or carbonyl-oxygen bond:
- Amide: R-CONHR' → R-CO-X + H2NR' (X = Cl, OH, OR'')
- Ester: R-COOR' → R-CO-X + HOR' (X = Cl, OH, OCOR)

## Key Points

1. **Acyl chloride reactivity**: Most reactive acylating agent
2. **Stereochemistry**: Acylation doesn't typically create chiral centers
3. **Regioselectivity**: Primary amines acylate more easily than secondary

## Critical Error Pattern: Acetylating Agent Selection

### Common Mistake
- **Question**: `CCCOc1cc(F)cc(C[C@H](NC(C)=O)[C@H](O)[C@H]2CO[C@@H](OCC(C)(C)C)[C@H](C)N2C(=O)OC(C)(C)C)c1`
- **Wrong answer**: Used `CC(=O)Cl` (acetyl chloride) as acylating agent
- **Correct answer**: Used `CC(=O)OC(C)=O` (acetic anhydride) as acylating agent

### Why This Matters
- Both acetyl chloride and acetic anhydride can acetylate amines
- The choice depends on the substrate and conditions
- Acetic anhydride is often preferred for sensitive substrates or when controlled acylation is needed
- The context may indicate which reagent is expected based on reaction conditions

### How to Identify Which Reagent to Use
```
When the product contains an acetamide (NC(C)=O):

1. Check if there's stereochemistry that might be sensitive:
   - Chiral centers may require milder conditions (anhydride)
   - Acid chlorides are more reactive but can cause racemization

2. Look for the overall reaction context:
   - Anhydride: CC(=O)OC(=O)C or CC(=O)OC(C)=O (same molecule!)
   - Acid chloride: CC(=O)Cl

3. Key difference in SMILES:
   - Anhydride: CC(=O)OC(=O)C (two carbonyls connected by oxygen)
   - Acid chloride: CC(=O)Cl (carbonyl with chlorine)

4. General guideline:
   - If uncertainty exists, acetic anhydride is often the default
   - Acid chloride used when high reactivity needed
   - Check training examples for patterns

Example disconnections:
- Product with acetamide: ...NC(C)=O...
- With acetic anhydride: ...N.CC(=O)OC(=O)C
- With acetyl chloride: ...N.CC(=O)Cl
```

## Critical Error Pattern: SMILES Connectivity in Amino Acid Derivatives (ID 44)

### Common Mistake
- **Question**: Acylation with product containing complex amino sugar derivative with acetamide
- **Wrong answer**: `CCCOc1cc(F)cc(C[C@H](N)[C@H](O)[C@H]2CO[C@@H](OCC(C)(C)C)[C@H](C)N2C(=O)OC(C)(C)C)c1`
  - Pattern: `C[C@H](N)[C@H](O)` - amine and hydroxyl on ADJACENT chiral carbons with explicit stereochemistry
- **Correct answer**: `CCCOc1cc(F)cc(CC(N)C(O)[C@H]2CO[C@@H](OCC(C)(C)C)[C@H](C)N2C(=O)OC(C)(C)C)c1`
  - Pattern: `CC(N)C(O)` - amine on one carbon, hydroxyl on SEPARATE carbon

### Why This Matters
- The model incorrectly placed the amine and hydroxyl on adjacent chiral centers
- The correct structure has them on different carbons in the chain
- **Critical**: SMILES connectivity determines molecular structure!
- Wrong connectivity = completely different molecule

### How to Identify Correct Connectivity
```
Product: ...C[C@H](NC(C)=O)[C@H](O)[C@H]2...
         |
         Acetamide on carbon 1, hydroxyl on carbon 2
         These are adjacent chiral carbons

For retrosynthesis (amide → amine):

WRONG precursor: ...C[C@H](N)[C@H](O)[C@H]2...
                 |
                 Amine and hydroxyl on adjacent carbons
                 [C@H](N) = chiral carbon with amine
                 [C@H](O) = chiral carbon with hydroxyl
                 These are TWO separate chiral centers!

CORRECT precursor: ...CC(N)C(O)[C@H]2...
                   |
                   CC(N) = carbon with amine
                   C(O) = different carbon with hydroxyl
                   These are NOT the same carbon!

SMILES parsing:

WRONG: C[C@H](N)[C@H](O)
       |    |    |
       C    N    O
       (chiral) (chiral)
       Amine and OH on DIFFERENT carbons but both chiral
       The [C@H] before N makes N's carbon chiral
       The [C@H] before O makes O's carbon chiral

CORRECT: CC(N)C(O)
         ||   ||
         C    C
         (methyl) (hydroxyl carbon)
         Amine on first carbon (CC(N))
         Hydroxyl on second carbon (C(O))
         Different connectivity!

Key pattern for amino acids/derivatives:
- Check which carbon bears the amine: CC(N) vs C[C@H](N)
- Check which carbon bears the hydroxyl: C(O) vs [C@H](O)
- The fragments (CC(N) and C(O)) connect as: CC(N)C(O)
- NOT: C[C@H](N)[C@H](O)

In ID #44:
- Product has: C[C@H](NC(C)=O)[C@H](O) (adjacent chiral centers)
- Wrong precursor: C[C@H](N)[C@H](O) (same structure)
- Correct precursor: CC(N)C(O) (amine and OH on different carbons)
- The Boc-protected part starts at [C@H]2, not before the amine

Verification:
- In correct answer, [C@H]2 appears at: ...[C@H]2CO[C@@H]...
- This is part of the bicyclic system, not connected to the amine
- The amine is on CC(N), separate from the bicyclic system
```

### Common Mistake
- **Question**: `Cc1nc(NC(=O)CCCCC2CCSS2)sc1CCO[N+](=O)[O-]`
- **Wrong answer**: `Cc1nc(N)sc1CCO[N+](=O)[O-].O=C(O)CCCCC2CCSS2`
- **Correct answer**: `Cc1nc(N)sc1CCO[N+](=O)[O-].O=C(O)CCCCC1CCSS1`

### Why This Matters
- Ring numbers in SMILES (`1`, `2`, `3`) are arbitrary and denote connectivity, not specific atoms
- When creating the precursor, use the SAME ring number for atoms that connect
- The dithiolane ring: `CCSS2CCCCC(=O)NC1` needs ring number `1` if it connects to the amide nitrogen
- **Rule**: When in doubt, use `1` for the ring closure in the precursor fragment

### Correct Ring Numbering
```
Product: Cc1nc(NC(=O)CCCCC2CCSS2)sc1...
         |
         Amide bond connects N to carbonyl carbon
         Ring 2 is the dithiolane

Precursor (acid): O=C(O)CCCCC1CCSS1
                  |
                  Use ring number 1 to maintain consistency
                  (can be 1, 2, or 3 - but be consistent)

Precursor (amine): Cc1nc(N)sc1CCO[N+](=O)[O-]
                   |
                   Ring number 1 closes to sc1
```

## Critical Error Pattern: β-Keto Acid vs β-Keto Ester with Boc Protecting Group

### Common Mistake (id: 2 - Current Training Error)
- **Product**: `COCCN(C)c1cc(NC(=O)OC(C)(C)C)c(NC(=O)CC(=O)c2ccnc(-c3cc(C)no3)c2)cc1Cl`
- **Wrong Answer**: `COCCN(C)c1cc(NC(=O)OC(C)(C)C)c(N)cc1Cl.O=C(O)CC(=O)c1ccnc(-c2cc(C)no2)c1`
  - Used β-keto acid: `O=C(O)CC(=O)c1ccnc...`
- **Correct Answer**: `COCCN(C)c1cc(NC(=O)OC(C)(C)C)c(N)cc1Cl.Cc1cc(-c2cc(C(=O)CC(=O)OC(C)(C)C)ccn2)on1`
  - Used β-keto ester with Boc: `Cc1cc(-c2cc(C(=O)CC(=O)OC(C)(C)C)ccn2)on1`

### Why This Matters
- **CRITICAL**: β-Keto carbonyls are often protected as enol esters (Boc-protected) for stability
- The model predicted a free β-keto acid, but the correct precursor has the ketone protected as a Boc-enol ester
- This is NOT a simple acylation with a β-keto acid - the ketone is protected!
- The fragment `CC(=O)CC(=O)OC(C)(C)C` shows: ketone + methylene + carbonyl + Boc group

### How to Identify β-Keto Ester/Boc-Enol Patterns
```
Product fragment: ...NC(=O)CC(=O)c2ccnc(-c3cc(C)no3)c2
                  |
                  β-Keto amide pattern: NC(=O)CC(=O)-
                  Attached to heterocycle c2ccnc...

Key question: Is the ketone free (acid) or protected (ester)?

Look for the SMILES pattern in CORRECT precursor:
Cc1cc(-c2cc(C(=O)CC(=O)OC(C)(C)C)ccn2)on1
         |
         This shows:
         - Methyl-oxazole: Cc1cc...on1
         - Ketone: C(=O)
         - Methylene: CC
         - Carbonyl: CC(=O)
         - Boc protecting group: OC(C)(C)C

Pattern breakdown:
- CC(=O)OC(C)(C)C = acetyl group with Boc protecting (enolate precursor)
- This is NOT the same as O=C(O) (free carboxylic acid)

Retrosynthetic disconnection:
1. Break amide bond NC(=O)CC(=O) → amine fragment + acyl fragment
2. Amine: COCCN(C)c1cc(NC(=O)OC(C)(C)C)c(N)cc1Cl (Boc-protected amine)
3. Acyl: NOT O=C(O)CC(=O) (β-keto acid)
4. Acyl: Cc1cc(-c2cc(C(=O)CC(=O)OC(C)(C)C)ccn2)on1 (β-keto ester, Boc-protected)

SMILES distinction:
- β-Keto acid: O=C(O)CC(=O) (carboxylic acid + ketone)
- β-Keto ester with Boc: CC(=O)CC(=O)OC(C)(C)C (ketone + enol ester + Boc)

Forward reaction:
- β-Keto ester + amine → β-keto amide + Boc-protected alcohol
- The Boc group is released as (CH3)3COH
```

### Key Pattern for β-Keto Carbonyl Protection
```
When you see β-keto amide in product (NC(=O)CC(=O)-):

1. Check if ketone is protected as Boc-enol:
   - Protected: CC(=O)CC(=O)OC(C)(C)C (acetyl + Boc-enol)
   - Unprotected: O=C(O)CC(=O) (carboxylic acid + ketone)

2. Look for the oxazole/heterocycle attachment:
   - Product: c2ccnc(-c3cc(C)no3)c2 (ketone attached to heterocycle)
   - Precursor: Cc1cc(-c2cc(...)ccn2)on1 (same, but ketone protected)

3. Critical SMILES markers:
   - Boc protecting group: OC(C)(C)C (tert-butoxy)
   - Enol ester: CC(=O)OC(C)(C)C (acetyl enol, Boc-protected)
   - NOT: O=C(O) (free acid)

4. Always check for protecting groups on β-keto carbonyls!
   - β-Keto acids often protected as esters for stability
   - Boc is common protecting group for enols/β-keto esters
```

## Critical Error Pattern: Acylation Site Selectivity

### Common Mistake
- **Question**: Complex molecule with multiple amine sites and heterocyclic fragments
- **Wrong answer**: Assumed acylation occurs on one site, but it occurs on a different site
- **Correct answer**: Identified the correct fragment that undergoes acylation

### Why This Matters
- In molecules with multiple acylation sites, identify WHICH fragment contains the acyl group
- Look for: β-keto acids, β-keto esters, or other activated carbonyl compounds
- The acylated product contains the carbonyl from the acyl donor attached to a nitrogen

### How to Identify Acylation Sites
```
Product pattern: ...NC(=O)... (amide bond)
                  |
                  Look for which fragment contains the carbonyl carbon

Key indicators:
1. β-Keto amide: NC(=O)CC(=O)- (keto group adjacent to amide)
2. Check which fragment has the carbonyl + carbon chain pattern
3. The acyl donor fragment will have: HOOC-CH2-...-C(=O)- (if acid) or CC(=O)-...-C(=O)-OC(C)(C)C (if ester)

Example:
Product: COCCN(C)c1cc(NC(=O)OC(C)(C)C)c(NC(=O)CC(=O)c2ccnc(-c3cc(C)no3)c2)cc1Cl

Analysis:
- NC(=O)CC(=O)- is a β-keto amide pattern
- The fragment c2ccnc(-c3cc(C)no3)c2 contains the keto carbonyl
- This fragment is acylated with the β-keto ester (Boc-protected): Cc1cc(-c2cc(C(=O)CC(=O)OC(C)(C)C)ccn2)on1
- Boc protection is on a different amine site (NC(=O)OC(C)(C)C)

Retrosynthetic disconnection:
1. Break β-keto amide bond → amine fragment + β-keto ester fragment
2. Break Boc amide bond → amine fragment + Boc2O (but Boc is pre-existing)

## Critical Error Pattern: Amide Bond Disconnection in Fused Heterocyclic Systems

### Common Mistake (ERROR #3)
- **Question**: `CN(Cc1cccc(C(=O)N2CC(=O)Nc3ccccc32)c1)C(=O)OC(C)(C)C` (Boc-protected tertiary amine with fused heterocycle)
- **Wrong answer**: `CN(Cc1cccc(C(=O)N2CC(=O)Nc3ccccc32)c1).CC(C)(C)OC(=O)OC(=O)OC(C)(C)C` (disconnected Boc group, kept fused ring intact)
- **Correct answer**: `CN(Cc1cccc(C(=O)O)c1)C(=O)OC(C)(C)C.O=C1CNc2ccccc2N1` (disconnected internal amide, fused ring splits into two molecules)

### Why This Matters
- The fused benzimidazolone system (N2CC(=O)Nc3ccccc32) can undergo amide bond cleavage
- The acylation reaction formed an amide bond between two fragments that then fused
- NOT all amide bonds are protecting groups - some are the MAIN product-forming reaction
- The Boc group (C(=O)OC(C)(C)C) STAYS with one fragment; the fused ring BREAKS APART

### How to Identify Amide Bond Cleavage in Heterocyclic Systems
```
Product: CN(Cc1cccc(C(=O)N2CC(=O)Nc3ccccc32)c1)C(=O)OC(C)(C)C
         |
         Structure breakdown:
         1. Tertiary amine: CN(...)C(=O)OC(C)(C)C (Boc-protected dimethylamine)
         2. Benzyl linker: Cc1cccc(...)c1 (benzyl attached to amine)
         3. Amide bond: C(=O)N2CC(=O)Nc3ccccc32
         4. Fused heterocycle: N2CC(=O)Nc3ccccc32 (benzimidazolone)

Key question: Which amide bond is the acylation site?

Analysis:
1. The Boc group C(=O)OC(C)(C)C is a protecting group on the tertiary amine
2. The amide bond in N2CC(=O)Nc3ccccc32 connects the benzyl group to the fused ring
3. This is an INTERNAL amide bond that was formed during the reaction
4. Retrosynthetically: BREAK this amide bond

Retrosynthetic disconnection:
1. Break amide bond between C(=O) and N2
2. Fragment 1: CN(Cc1cccc(C(=O)O)c1)C(=O)OC(C)(C)C
               |
               Benzyl with carboxylic acid + Boc-protected tertiary amine
               The C(=O)N becomes C(=O)O (carboxylic acid)

3. Fragment 2: O=C1CNc2ccccc2N1
               |
               Benzimidazolone (fused ring system)
               The N2 becomes part of the fused ring N1

How to identify:
- Look for fused ring systems with amide patterns: N2CC(=O)Nc3...
- The C(=O)N bond may connect the ring to an external fragment
- When disconnected, the C(=O)N becomes C(=O)O (acid) + N in ring
- The Boc protecting group stays with the amine fragment, NOT with the heterocycle

SMILES patterns:
- Fused heterocycle with amide: N2CC(=O)Nc3ccccc32
- After disconnection (acid fragment): C(=O)O where C(=O)N was
- After disconnection (heterocycle fragment): O=C1CNc2ccccc2N1 (ring closes to N1)
```

### Disconnection Strategy for Fused Heterocyclic Amides
```
When analyzing products with fused heterocyclic amides:

1. Identify the fused ring system:
   - Benzimidazolone: N2CC(=O)Nc3ccccc32
   - Indole: c1ccc2c(c1)cc[nH]2
   - Other fused systems with amide connectivity

2. Check if amide connects ring to external fragment:
   - Pattern: ...C(=O)N2CC(=O)Nc3...
   - The N2 is part of the ring, connected to external carbonyl

3. Determine disconnection point:
   - Is this a protecting group (Boc, Cbz) or a product-forming amide?
   - Protecting groups: on amines, removable under specific conditions
   - Product-forming amides: connect two fragments, formed in the reaction

4. For ERROR #3:
   - Boc C(=O)OC(C)(C)C = protecting group on tertiary amine (STAYS)
   - Amide C(=O)N2 = connection between benzyl and fused ring (BREAKS)
   - Disconnect C(=O)N2 → C(=O)O + N2 (becomes N1 in ring)

Key distinction:
- Protecting group amide: -N-C(=O)OC(C)(C)C (removable as single unit)
- Product amide: ...C(=O)-N< (connects two fragments, breaks into two molecules)
