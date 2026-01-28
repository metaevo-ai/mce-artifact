task_instruction = '''The FINER benchmark requires mapping financial entities (numbers, percentages, text spans) in sentences to the correct US GAAP XBRL tag from a vocabulary of 139 tags. This is a challenging semantic classification task where:

- **Large vocabulary**: 139 tags with highly similar names (e.g., `InterestExpense` vs `InterestExpenseDebt`)
- **Semantic nuances**: Same entity type can map to different tags based on context (e.g., debt amounts can be `DebtInstrumentFaceAmount`, `DebtInstrumentFairValue`, or `DebtInstrumentCarryingAmount`)
- **Long tag names**: Tags can be 100+ characters, requiring careful attention to detail
- **Context dependency**: The surrounding sentence provides critical disambiguation cues

Each training sample contains:
- **question**: A sentence with a highlighted entity and the question "What is best tag for entity X in sentence: Y?"
- **target**: The correct XBRL tag
'''