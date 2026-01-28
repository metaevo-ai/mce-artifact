task_instruction = '''The USPTO-50k benchmark requires predicting precursor reactants for single-step retrosynthesis reactions. This is a challenging chemical synthesis task where:

- **SMILES notation**: Molecules are represented using SMILES (Simplified Molecular-Input Line-Entry System) strings
- **Retrosynthesis**: Given a product molecule, predict the reactant molecules needed to synthesize it in one step
- **Reaction types**: Various reaction types including C-C bond formation, Heteroatom alkylation and arylation, Reductions, Deprotections, Acylation, Oxidations, Heterocycle formation, etc.
- **Chemical knowledge**: Requires understanding of organic chemistry reaction mechanisms and functional group transformations

Each training sample contains:
- **question**: A SMILES string of the product molecule and the reaction type
- **target**: The SMILES string(s) of the precursor reactants (separated by periods if multiple)
'''

