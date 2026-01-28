# Debt and Credit Subset

This subset focuses on financial tags related to debt instruments, credit facilities, and loan-related financial reporting.

## Dataset Statistics

- **Training samples**: 200
- **Validation samples**: 100
- **Test samples**: 100
- **Total tags**: 12

## Selected Tags

This subset covers the following 12 debt and credit-related financial tags:

1. **DebtInstrumentInterestRateStatedPercentage** - The stated interest rate on debt instruments
2. **DebtInstrumentFaceAmount** - The face value/principal amount of debt
3. **LineOfCreditFacilityMaximumBorrowingCapacity** - Maximum borrowing limit on credit lines
4. **DebtInstrumentBasisSpreadOnVariableRate1** - Basis point spread on variable rate debt
5. **DebtInstrumentCarryingAmount** - Book value of debt on balance sheet
6. **DebtInstrumentRedemptionPricePercentage** - Redemption price as percentage of face value
7. **LongTermDebtFairValue** - Fair value of long-term debt
8. **LongTermDebt** - Long-term debt amounts
9. **LettersOfCreditOutstandingAmount** - Outstanding letters of credit
10. **LineOfCredit** - Credit line amounts
11. **LineOfCreditFacilityCurrentBorrowingCapacity** - Current borrowing capacity on credit facilities
12. **DebtInstrumentUnamortizedDiscount** - Unamortized discount on debt instruments

## Tag Distribution

### Training Set
- DebtInstrumentInterestRateStatedPercentage: 41
- DebtInstrumentFaceAmount: 35
- LineOfCreditFacilityMaximumBorrowingCapacity: 35
- DebtInstrumentBasisSpreadOnVariableRate1: 27
- DebtInstrumentCarryingAmount: 9
- DebtInstrumentRedemptionPricePercentage: 9
- LongTermDebtFairValue: 9
- LongTermDebt: 7
- LettersOfCreditOutstandingAmount: 7
- LineOfCredit: 7
- LineOfCreditFacilityCurrentBorrowingCapacity: 8
- DebtInstrumentUnamortizedDiscount: 6

### Validation Set
- DebtInstrumentInterestRateStatedPercentage: 26
- DebtInstrumentFaceAmount: 18
- LineOfCreditFacilityMaximumBorrowingCapacity: 21
- DebtInstrumentBasisSpreadOnVariableRate1: 11
- DebtInstrumentCarryingAmount: 6
- DebtInstrumentRedemptionPricePercentage: 3
- LongTermDebtFairValue: 3
- LongTermDebt: 2
- LettersOfCreditOutstandingAmount: 2
- LineOfCredit: 5
- LineOfCreditFacilityCurrentBorrowingCapacity: 1
- DebtInstrumentUnamortizedDiscount: 2

### Test Set
- DebtInstrumentInterestRateStatedPercentage: 27
- DebtInstrumentFaceAmount: 16
- LineOfCreditFacilityMaximumBorrowingCapacity: 16
- DebtInstrumentBasisSpreadOnVariableRate1: 13
- DebtInstrumentCarryingAmount: 7
- DebtInstrumentRedemptionPricePercentage: 1
- LongTermDebtFairValue: 1
- LongTermDebt: 8
- LettersOfCreditOutstandingAmount: 2
- LineOfCredit: 6
- LineOfCreditFacilityCurrentBorrowingCapacity: 2
- DebtInstrumentUnamortizedDiscount: 1

## Data Format

Each line in the JSONL files contains:
```json
{
  "question": "What is best tag for entity \"<value>\" in sentence: \"<sentence>\"",
  "target": "<tag_name>",
  "context": ""
}
```

## Usage

This subset can be used for:
- Training specialized models for debt and credit-related financial entity classification
- Evaluating model performance on a focused financial domain
- Comparing performance between full dataset and domain-specific subset
- Fine-tuning models for debt instrument analysis

## Sampling Method

- Stratified sampling was used to maintain proportional tag distribution
- Random seed: 42 (for reproducibility)
- Samples were shuffled within each split
