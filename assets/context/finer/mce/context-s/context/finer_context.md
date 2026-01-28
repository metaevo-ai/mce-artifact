# Financial Entity Recognition Context

## Task Overview
Given a sentence from financial documents and a specific numeric entity, identify the correct XBRL tag.

## Tag Definitions

### 1. Interest Rate Tags

**DebtInstrumentInterestRateStatedPercentage**
- Fixed/stated rates on notes/bonds: "5.25% Senior Notes"
- "interest at X% per annum"
- NOT for LIBOR rate values

**DebtInstrumentBasisSpreadOnVariableRate1**
- Margin/spread on variable rate: "LIBOR plus 1.75%", "margin of 2.00%"
- "LIBOR was X%" → use this tag

### 2. Debt Amount Tags

**DebtInstrumentFaceAmount**
- Principal/face amount at issuance
- Terms: "principal amount", "aggregate principal amount", "face amount"
- Examples: "$575.0 million aggregate principal amount"
- Derivative notional: "total notional of interest rate swaps was $300.0 million"

**DebtInstrumentCarryingAmount**
- Current book value on balance sheet
- Terms: "balance", "outstanding", "carrying amount", "as of [date]"
- Examples: "balance was $273.4 million"

**LongTermDebt**
- Total long-term debt balance
- "balance of the [Named Term Loan]" → use this tag
- "carrying amount of the mortgage notes" → use this tag
- Examples: "balance of the 2016 Term Loan was $273.4 million"

**LongTermDebtFairValue**
- Fair/market value of long-term debt
- Terms: "fair value", "market value"
- Examples: "fair value of $649.7 million"

**DebtInstrumentUnamortizedDiscount**
- Remaining unamortized discount on debt
- Terms: "unamortized discount", "OID"

### 3. Credit Facility Tags

**LineOfCreditFacilityMaximumBorrowingCapacity**
- Maximum/total facility limit (ceiling, not current usage)
- Phrases: "borrowing capacity", "facility of", "revolving credit facility"
- Examples:
  - "$1.99 billion revolving credit facility"
  - "$2.25 billion unsecured revolving credit facility"
  - "$335 million secured revolving credit facility"
  - "$525,000 revolving credit facility"
  - "$45.0 million revolving credit facility"
  - "$16.0 million Tranche A loan revolving loan facility"
  - "borrowing capacity of $250 million"

**LineOfCreditFacilityCurrentBorrowingCapacity**
- Currently available/unused capacity OR facility size with outstanding/available figures
- Terms: "available", "unused", "current borrowing capacity"
- Examples: "$400.0 million facility with $90.5 million outstanding and $309.5 million unused"

**LineOfCredit**
- Outstanding borrowings OR bank guarantee amounts
- Terms: "outstanding borrowings", "bank guarantees", "indebtedness"
- Examples:
  - "$0.4 million of bank guarantees outstanding"
  - "$100.7 million outstanding revolving loans under the credit facility"
  - "$49.6 million of indebtedness"
  - "$17.0 million letter of credit as of [date] with no outstanding balance"
  - "no outstanding balance on the Credit Agreement"

### 4. Other Tags

**LettersOfCreditOutstandingAmount**
- Amount of outstanding letters of credit
- Examples: "$41.8 million of letters of credit outstanding"

**DebtInstrumentRedemptionPricePercentage**
- Percentage of par for redemption/repurchase OR issue price percentages
- Examples: "redeemable at 102.313%", "issue price of 99.78% of face value"

## Critical Disambiguation Rules

### Rule 1: Interest Rates
- LIBOR rate values → DebtInstrumentBasisSpreadOnVariableRate1
- Fixed/stated rates on notes/bonds → DebtInstrumentInterestRateStatedPercentage
- Margin/spread on variable rate → DebtInstrumentBasisSpreadOnVariableRate1

### Rule 2: Debt Amounts
- Issuance/principal amount → DebtInstrumentFaceAmount
- Current balance/book value → DebtInstrumentCarryingAmount
- Fair/market value → LongTermDebtFairValue
- "balance of [Named Term Loan]" → LongTermDebt
- Generic/unclear → LongTermDebt
- Issue price percentage → DebtInstrumentRedemptionPricePercentage
- Derivative notional → DebtInstrumentFaceAmount

### Rule 3: Credit Facilities
- "of up to $X" or standalone facility amount → LineOfCreditFacilityMaximumBorrowingCapacity
- "$X available" → LineOfCreditFacilityCurrentBorrowingCapacity
- "$X facility with $Y outstanding" → LineOfCreditFacilityCurrentBorrowingCapacity
- "$X outstanding borrowings" (no facility context) → LineOfCredit
- Bank guarantees outstanding → LineOfCredit
- Letters of credit outstanding → LettersOfCreditOutstandingAmount

### Rule 4: Context is King
- Read the full sentence to understand what the number represents
- "$X revolving credit facility" (standalone) = Maximum capacity
- "$X outstanding borrowings" = Current usage

## Common Patterns

### Facility Descriptions
"$X revolving credit facility" (standalone) → LineOfCreditFacilityMaximumBorrowingCapacity
"$X unsecured revolving credit facility" → LineOfCreditFacilityMaximumBorrowingCapacity
"$X secured revolving credit facility" → LineOfCreditFacilityMaximumBorrowingCapacity
"$X credit facility that matures in [date]" → LineOfCreditFacilityMaximumBorrowingCapacity
"$X revolving line of credit" → LineOfCreditFacilityMaximumBorrowingCapacity
"$X facility of up to" → LineOfCreditFacilityMaximumBorrowingCapacity
"$X available" → LineOfCreditFacilityCurrentBorrowingCapacity
"$X facility with $Y outstanding" → LineOfCreditFacilityCurrentBorrowingCapacity
"$X outstanding borrowings" → LineOfCredit
"$X of indebtedness" → LineOfCredit
"$X outstanding in revolver borrowings" → LineOfCredit
"$X letter of credit with no outstanding balance" → LineOfCredit

### Interest Rate Descriptions
"X% Senior Notes" → DebtInstrumentInterestRateStatedPercentage
"LIBOR plus X%" → DebtInstrumentBasisSpreadOnVariableRate1
"LIBOR was X%" → DebtInstrumentBasisSpreadOnVariableRate1

### Debt Issuance
"issued $X principal amount" → DebtInstrumentFaceAmount
"total notional of interest rate swaps" → DebtInstrumentFaceAmount
"balance of the [Named Term Loan]" → LongTermDebt
"carrying amount of the mortgage notes" → LongTermDebt
"balance was $X" → DebtInstrumentCarryingAmount
"fair value of $X" → LongTermDebtFairValue
"issue price of X%" → DebtInstrumentRedemptionPricePercentage

### Credit Instruments
"bank guarantees outstanding" → LineOfCredit
"letters of credit outstanding" → LettersOfCreditOutstandingAmount
