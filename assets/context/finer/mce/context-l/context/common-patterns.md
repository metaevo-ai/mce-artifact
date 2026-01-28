# Common Patterns and Correct Tags

## Pattern 1: Percentage + "plus/above/margin" = Basis Spread

### WRONG Pattern (from training errors):
- Entity: "3.75", "1.750", "2"
- Context: "plus a margin of 3.75%", "1.750% above LIBOR", "LIBOR plus 2%"
- LLM Answer: `DebtInstrumentInterestRateStatedPercentage`, `DebtInstrumentInterestRateEffectivePercentage`, `LineOfCreditFacilityInterestRateAtPeriodEnd`
- **ERROR**: Confusing margin/basis spread with total rate

### RIGHT Pattern (correct tags):
- Entity: Any percentage
- Context contains: "plus", "above", "margin"
- **ALWAYS** use: `DebtInstrumentBasisSpreadOnVariableRate1`

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 3.75 | "plus a margin of 3.75%" | BasisSpread |
| 1.750 | "1.750% above LIBOR" | BasisSpread |
| 2 | "LIBOR plus 2%" | BasisSpread |
| 1.000 | "rates of 1.000% to 1.750% above LIBOR" | BasisSpread |

---

## Pattern 2: Facility Setup/Increase = Maximum Capacity

### WRONG Pattern (from training errors):
- Entity: "600.0", "60", "2.25", "1.8"
- Context: "commitments of $600.0 million", "up to $60 million", "$2.25 billion facility", "$1.8 billion" capacity
- LLM Answer: `LineOfCredit`, `LettersOfCreditOutstandingAmount`
- **ERROR**: Confusing facility capacity limits with other debt amounts

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context contains: "up to $X", "$X billion revolving credit facility", "increased to $X", "commitments of $X"
- **ALWAYS** use: `LineOfCreditFacilityMaximumBorrowingCapacity`

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 600.0 | "total term loan commitments of $600.0 million" | MaximumBorrowingCapacity |
| 60 | "permitted to issue up to $60 million" | MaximumBorrowingCapacity |
| 2.25 | "$2.25 billion unsecured revolving credit facility" | MaximumBorrowingCapacity |
| 1.8 | "capacity... of $1.8 billion" | MaximumBorrowingCapacity |
| 1.0 | "$1.0 billion revolving credit agreement" | DebtInstrumentFaceAmount |

---

## Pattern 3: Outstanding Borrowings = Carrying Amount (NOT Current Capacity)

### WRONG Pattern (from training errors):
- Entity: "70.0", "273.4"
- Context: "$70.0 million outstanding borrowings", "balance of the 2016 Term Loan was $273.4 million"
- LLM Answer: `LineOfCreditFacilityCurrentBorrowingCapacity`, `DebtInstrumentCarryingAmount`
- **ERROR**: When borrowings are debt instruments, use LongTermDebt or DebtInstrumentCarryingAmount, NOT facility capacity tags

### RIGHT Pattern (correct tags):
- Entity: Dollar amount of actual borrowings
- Context: "outstanding borrowings under [term loan]", "balance of [term loan]"
- **Use**: `LongTermDebt` (for general term loan balance) or `DebtInstrumentCarryingAmount` (for instrument-specific)

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 70.0 | "$70.0 million outstanding borrowings" (Senior Secured) | DebtInstrumentCarryingAmount |
| 273.4 | "balance of the 2016 Term Loan was $273.4 million" | LongTermDebt |
| 0.7 | "$0.7 billion of repurchase agreements... considered long-term" | LongTermDebtFairValue |

---

## Pattern 4: Fair Value of Debt = LongTermDebtFairValue

### WRONG Pattern (from training errors):
- Entity: "649.7"
- Context: "fair value of these Notes... were $649.7 million"
- LLM Answer: `DebtInstrumentFairValue`
- **ERROR**: Should use LongTermDebtFairValue, not specific DebtInstrument tag

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: "fair value of [notes/debt/long-term debt]"
- **ALWAYS** use: `LongTermDebtFairValue`

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 649.7 | "fair value of these Notes... were $649.7 million" | LongTermDebtFairValue |
| 32,109 | "fair value of the Company's long-term debt... $32,109" | LongTermDebtFairValue |
| 638 | "fair value of our long-term debt... $638 million" | LongTermDebtFairValue |

---

## Pattern 5: "No/Negative" Entities = General Reference

### WRONG Pattern (from training errors):
- Entity: "no"
- Context: "no borrowings outstanding under the Revolving Credit Facility"
- LLM Answer: `LineOfCreditFacilityRemainingBorrowingCapacity`
- **ERROR**: "no" is not a capacity amount, it's indicating facility existence

### RIGHT Pattern (correct tags):
- Entity: "no", "none", "zero"
- Context: "no borrowings outstanding", "no outstanding balance"
- **Use**: `LineOfCredit` (general facility reference)

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| no | "no borrowings outstanding under the Revolving Credit Facility" | LineOfCredit |

---

## Pattern 6: Interest Rate Stated on Note

### WRONG Pattern (from training errors):
- Entity: "6"
- Context: "Interest was payable... at 6% per annum"
- LLM Answer: `InterestExpense`
- **ERROR**: The percentage rate itself is StatedPercentage, not the expense amount

### RIGHT Pattern (correct tags):
- Entity: Percentage
- Context: "X% per annum", "X% interest rate", "[X%] Notes" (naming pattern)
- **Use**: `DebtInstrumentInterestRateStatedPercentage`

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 6 | "Interest was payable... at 6% per annum" | StatedPercentage |
| 3.25 | "The 3.25% Convertible Senior Notes" | StatedPercentage |
| 8.375 | "the 8.375% Senior Notes due 2022" | StatedPercentage |

---

## Decision Summary: What Tag to Use?

| Entity Type | Key Context Words | Correct Tag |
|-------------|------------------|-------------|
| % + plus/above/margin | "plus X%", "X% above LIBOR", "margin of X%" | DebtInstrumentBasisSpreadOnVariableRate1 |
| % + note name/rate | "X% Notes", "X% per annum", "interest rate of X%" | DebtInstrumentInterestRateStatedPercentage |
| $ + "up to"/capacity | "up to $X", "facility of $X", "commitments of $X" | LineOfCreditFacilityMaximumBorrowingCapacity |
| $ + "outstanding" | "outstanding borrowings of $X", "amount outstanding" | LineOfCreditFacilityCurrentBorrowingCapacity OR DebtInstrumentCarryingAmount |
| $ + "fair value" | "fair value of long-term debt", "fair value of Notes" | LongTermDebtFairValue |
| $ + "balance" | "balance of the term loan", "long-term debt was $X" | LongTermDebt |
| Entity = "no"/"none" | "no borrowings outstanding" | LineOfCredit |
| $ + "principal/face" | "aggregate principal amount of $X", "$X note" | DebtInstrumentFaceAmount |
| $ + "unamortized discount" | "unamortized discount of $X" | DebtInstrumentUnamortizedDiscount |
| $ + "letters of credit outstanding" | "letters of credit were outstanding" | LettersOfCreditOutstandingAmount |

---

## Pattern 7: LIBOR Rate (Absolute) vs Basis Spread

### WRONG Pattern (from training errors):
- Entity: "2.51"
- Context: "LIBOR at December 26, 2018 was approximately 2.51%"
- LLM Answer: "No appropriate tag available for LIBOR benchmark rate" or `DebtInstrumentBasisSpreadOnVariableRate1`
- **ERROR**: Confusing absolute LIBOR rates with basis spreads. The entity is the LIBOR rate itself, not a spread added to LIBOR.

### RIGHT Pattern (correct tags):
- Entity: Percentage (LIBOR rate)
- Context: "LIBOR was X%", "One month LIBOR at [date] was approximately X%"
- **Use extreme caution**: This is an absolute rate, not a spread. Check if a specific tag exists. In training data, this was tagged as `DebtInstrumentBasisSpreadOnVariableRate1` but the pattern suggests this may be a special case.

### Examples:
| Entity | Context Phrase | Correct Tag (from training) |
|--------|---------------|----------------------------|
| 2.51 | "One month LIBOR at December 26, 2018 was approximately 2.51%" | DebtInstrumentBasisSpreadOnVariableRate1 |

---

## Pattern 8: "Outstanding Under [Facility]" = Debt Carrying Amount

### WRONG Pattern (from training errors):
- Entity: "60"
- Context: "$60 million was outstanding under the Noble Midstream Services Revolving Credit Facility"
- LLM Answer: `LineOfCreditFacilityCurrentBorrowingCapacity`
- **ERROR**: "Outstanding under facility" indicates the debt instrument carrying amount, not the facility's current borrowing capacity.

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: "$X was outstanding under [facility name]", "$X outstanding under the [facility]"
- **Use**: `DebtInstrumentCarryingAmount` when referring to amounts outstanding under a credit facility. The "under" phrasing indicates the debt itself.

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 60 | "$60 million was outstanding under the Revolving Credit Facility" | DebtInstrumentCarryingAmount |
| 1.99 | "$1.99 billion under the Term Loan B Facility" | LongTermDebt |

---

## Pattern 9: Derivative Notional Referencing Debt = Face Amount

### WRONG Pattern (from training errors):
- Entity: "300.0"
- Context: "The total notional of the Company's interest rate swaps was $300.0 million"
- LLM Answer: `DerivativeNotionalAmount`
- **ERROR**: When the context discusses interest rate swaps in relation to debt instruments, and the amount represents the underlying debt principal, use `DebtInstrumentFaceAmount`.

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: Notional amount related to debt instruments, swap agreements tied to debt
- **Use**: `DebtInstrumentFaceAmount` when the notional represents the underlying debt principal

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 300.0 | "The total notional of the Company's interest rate swaps was $300.0 million" | DebtInstrumentFaceAmount |

---

## Pattern 10: Term Loan Balance = LongTermDebt

### WRONG Pattern (from training errors):
- Entity: "1.99"
- Context: "$1.99 billion under the Term Loan B Facility" (after repricing)
- LLM Answer: `DebtInstrumentCarryingAmount`
- **ERROR**: General references to term loan balances are `LongTermDebt`, not specific carrying amounts.

### RIGHT Pattern (correct tags):
- Entity: Dollar amount of term loan
- Context: "balance of the term loan", "amount under the Term Loan Facility"
- **Use**: `LongTermDebt` for general term loan balances

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 1.99 | "$1.99 billion under the Term Loan B Facility" | LongTermDebt |
| 273.4 | "balance of the 2016 Term Loan was $273.4 million" | LongTermDebt |

---

## Pattern 11: Credit Facility with No Outstanding Balance = LineOfCredit

### WRONG Pattern (from training errors):
- Entity: "17.0" or "0.4"
- Context: "issued a letter of credit for $17.0 million with no outstanding balance"
- LLM Answer: `LettersOfCreditOutstandingAmount`
- **ERROR**: When a facility/letter of credit has NO outstanding balance, use `LineOfCredit`.

### RIGHT Pattern (correct tags):
- Entity: Dollar amount OR "no" entity
- Context: "letter of credit for $X with no outstanding balance", "no outstanding balance under the facility"
- **Use**: `LineOfCredit` when there is explicitly no outstanding balance

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 17.0 | "issued a letter of credit for $17.0 million as of [date] with no outstanding balance" | LineOfCredit |
| no | "no outstanding balance on the Credit Agreement" | LineOfCredit |
| 0.4 | "€0.3 million of bank guarantees outstanding, €38.7 million available" | LineOfCredit |

---

## Pattern 12: Revolving Loans Denominated in Foreign Currency

### WRONG Pattern (from training errors):
- Entity: "100.7"
- Context: "$100.7 million of which were denominated in Canadian dollars" (outstanding revolving loans)
- LLM Answer: `LineOfCreditFacilityCurrentBorrowingCapacity`
- **ERROR**: When the entity is a breakdown of revolving loans in a foreign currency within a larger facility context, use `LineOfCredit`.

### RIGHT Pattern (correct tags):
- Entity: Dollar amount (foreign currency breakdown)
- Context: "$X of which were denominated in [foreign currency]" (as part of facility breakdown)
- **Use**: `LineOfCredit` when the entity is a currency-denominated portion of a larger facility

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 100.7 | "$100.7 million of which were denominated in Canadian dollars" | LineOfCredit |
| 79.4 | "$79.4 million of which were denominated in Australian dollars" | LineOfCredit |

---

## Pattern 13: Term Loan Facility Amounts = Face Amount (NOT Maximum Capacity)

### WRONG Pattern (from training errors):
- Entity: "225", "150"
- Context: "12-month €225 million term loan facility", "$150 million senior revolving credit facility and $150 million term loan facility"
- LLM Answer: `LineOfCreditFacilityMaximumBorrowingCapacity`
- **ERROR**: Model sees "$X [facility]" and always selects MaximumBorrowingCapacity without distinguishing facility type

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: "term loan facility of $X" (NOT revolving)
- **Use**: `DebtInstrumentFaceAmount` (term loans have principal/face amounts, revolving facilities have capacity limits)

### Key Distinction:
- Term loan facility amount = Face Amount (the loan principal)
- Revolving credit facility amount = MaximumBorrowingCapacity (the available limit)

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 225 (€) | "12-month €225 million term loan facility" | DebtInstrumentFaceAmount |
| 150 | "$150 million term loan facility" | DebtInstrumentFaceAmount |
| 150 | "$150 million senior revolving credit facility" | LineOfCreditFacilityMaximumBorrowingCapacity |

---

## Pattern 14: "Outstanding Principal Balance" = Carrying Amount (NOT Face Amount)

### WRONG Pattern (from training errors):
- Entity: "4.2"
- Context: "a loan with a $4.2 million outstanding principal balance"
- LLM Answer: `DebtInstrumentFaceAmount`
- **ERROR**: "Outstanding principal balance" means current REMAINING balance, not original face amount

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: "outstanding principal balance of $X"
- **Use**: `DebtInstrumentCarryingAmount` (the current remaining principal)

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 4.2 | "loan with a $4.2 million outstanding principal balance" | DebtInstrumentCarryingAmount |
| 475 (£) | "£475 million principal outstanding, translated at spot rate" | DebtInstrumentCarryingAmount |

---

## Pattern 15: "Allowing to Borrow in a Single Drawing Up to $X" = Current Borrowing Capacity

### WRONG Pattern (from training errors):
- Entity: "250"
- Context: "The Credit Agreement contains a 7-year term loan feature allowing the Operating Partnership to borrow in a single drawing up to $250 million"
- LLM Answer: `LineOfCreditFacilityMaximumBorrowingCapacity`
- **ERROR**: This describes the current borrowing MECHANISM, not the facility's maximum limit

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: "allowing to borrow in a single drawing up to $X"
- **Use**: `LineOfCreditFacilityCurrentBorrowingCapacity` (describes current borrowing mechanism)

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 250 | "allowing to borrow in a single drawing up to $250 million" | LineOfCreditFacilityCurrentBorrowingCapacity |

---

## Pattern 16: Advances Received = Face Amount (NOT Carrying Amount)

### WRONG Pattern (from training errors):
- Entity: "95,000"
- Context: "advances under the March 2016 $1,000,000 CPN of $95,000"
- LLM Answer: `DebtInstrumentCarryingAmount`
- **ERROR**: Advances RECEIVED are the face amount borrowed, not the current balance

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: "advances under the CPN of $X" or "received advances of $X"
- **Use**: `DebtInstrumentFaceAmount` (amounts borrowed/advanced)

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 95,000 | "advances under the March 2016 $1,000,000 CPN of $95,000" | DebtInstrumentFaceAmount |

---

## Pattern 17: Debt Financing in M&A = Face Amount (NOT Equity Proceeds)

### WRONG Pattern (from training errors):
- Entity: "36,000,000"
- Context: "closing of financing to the Parent of $36,000,000" (in M&A context with stockholder approval conditions)
- LLM Answer: `ProceedsFromIssuanceOfCommonStock`
- **ERROR**: Debt financing in M&A is not equity; it's debt instrument face amount

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: "closing of financing to the [entity] of $X" (M&A/corporate transaction)
- **Use**: `DebtInstrumentFaceAmount` (debt issuance in financing context)

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 36,000,000 | "closing of financing to the Parent of $36,000,000" | DebtInstrumentFaceAmount |

---

## Pattern 18: Government Loan = Face Amount (NOT LongTermDebt)

### WRONG Pattern (from training errors):
- Entity: "150,000"
- Context: "we received a loan of $150,000 from the IEDA"
- LLM Answer: `LongTermDebt`
- **ERROR**: Government loan with specific amount is a debt instrument face amount, not general long-term debt

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: "received a loan of $X from [government entity]"
- **Use**: `DebtInstrumentFaceAmount` (specific debt instrument issuance)

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 150,000 | "we received a loan of $150,000 from the IEDA" | DebtInstrumentFaceAmount |

---

## Pattern 19: Debt After Repricing = Carrying Amount (NOT Maximum Capacity)

### WRONG Pattern (from training errors):
- Entity: "1,695.8"
- Context: "repriced its existing $500.0 million senior secured revolving credit facility and $1,695.8 million senior secured Term Loan B facility"
- LLM Answer: `LineOfCreditFacilityMaximumBorrowingCapacity`
- **ERROR**: After repricing, this is the NEW carrying amount, not a facility capacity

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: Term loan amount AFTER repricing or modification
- **Use**: `DebtInstrumentCarryingAmount` (new carrying amount after repricing)

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 1,695.8 | "$1,695.8 million senior secured Term Loan B facility" (after repricing) | DebtInstrumentCarryingAmount |

---

## Pattern 20: Compound Subject Parsing - Amount Modifies First Item

### WRONG Pattern (from training errors):
- Entity: "90.0"
- Context: "$90.0 million outstanding borrowings, $1.2 million in letters of credit outstanding and $28.8 million of available borrowing capacity"
- LLM Answer: `DebtInstrumentCarryingAmount`
- **ERROR**: Entity modifies "outstanding borrowings" which in this context relates to letters of credit

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: "$X [Item A], $Y [Item B], and $Z [Item C]"
- **Rule**: Amount ALWAYS modifies the FIRST item in compound subjects
- Parse left to right to determine what the amount refers to

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 90.0 | "$90.0 million outstanding borrowings, $1.2 million in letters of credit..." | LettersOfCreditOutstandingAmount (when in credit facility context) |
| 1.2 | "$1.2 million in letters of credit outstanding" | LettersOfCreditOutstandingAmount |
| 28.8 | "$28.8 million of available borrowing capacity" | LineOfCreditFacilityRemainingBorrowingCapacity |

---

## Pattern 21: Balance Sheet Context - General Outstanding Amount = LongTermDebt

### WRONG Pattern (from training errors):
- Entity: "30.3"
- Context: "As of both May 31, 2016 and November 30, 2015, the outstanding amount related to the 5-year senior unsecured note was $30.3 million"
- LLM Answer: `DebtInstrumentCarryingAmount`
- **ERROR**: General balance sheet disclosure without "carrying amount" language = LongTermDebt

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: "As of [date], the outstanding amount related to the [note] was $X"
- **Use**: `LongTermDebt` (general balance sheet reference)

### Key Indicators:
- General balance sheet disclosure format
- No mention of "carrying amount" or "including accrued interest"
- References "outstanding amount" generally

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 30.3 | "outstanding amount related to the 5-year senior note" (balance sheet context) | LongTermDebt |

---

## Pattern 22: Letter of Credit Amounts = LettersOfCreditOutstandingAmount

### WRONG Pattern (from training errors):
- Entity: "450.0"
- Context: "letter of credit in the initial amount of $450.0 million"
- LLM Answer: `DebtInstrumentFaceAmount`
- **ERROR**: Confusing letters of credit amounts with debt instrument face amounts

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: "letter of credit in the initial amount of $X", "$X million of letters of credit"
- **ALWAYS** use: `LettersOfCreditOutstandingAmount` when context mentions letters of credit

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 450.0 | "letter of credit in the initial amount of $450.0 million" | LettersOfCreditOutstandingAmount |
| 17.0 | "issued a letter of credit for $17.0 million" | LettersOfCreditOutstandingAmount |

---

## Pattern 23: Note Purchase and Private Shelf Agreement = MaximumBorrowingCapacity

### WRONG Pattern (from training errors):
- Entity: "175.0"
- Context: "Amended and Restated Note Purchase and Private Shelf Agreement in the amount of $175.0 million"
- LLM Answer: `DebtInstrumentFaceAmount`
- **ERROR**: Note Purchase and Private Shelf Agreements are credit facilities, not debt instruments

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: "Note Purchase and Private Shelf Agreement in the amount of $X", "Shelf Agreement"
- **ALWAYS** use: `LineOfCreditFacilityMaximumBorrowingCapacity`

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 175.0 | "Amended and Restated Note Purchase and Private Shelf Agreement in the amount of $175.0 million" | LineOfCreditFacilityMaximumBorrowingCapacity |

---

## Pattern 24: "Total Availability" = CurrentBorrowingCapacity (NOT Maximum)

### WRONG Pattern (from training errors):
- Entity: "1,150,000"
- Context: "increased the credit facility by $200,000, bringing the total availability to $1,150,000"
- LLM Answer: `LineOfCreditFacilityMaximumBorrowingCapacity`
- **ERROR**: "Total availability" refers to current available amount, not maximum capacity

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: "total availability of $X", "bringing the total availability to $X"
- **Use**: `LineOfCreditFacilityCurrentBorrowingCapacity` (current available amount)

### Key Distinction:
- "Total availability" = current amount available to borrow
- "Maximum capacity" = the facility limit
- Different concepts - use CurrentBorrowingCapacity for availability

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 1,150,000 | "bringing the total availability to $1,150,000" | LineOfCreditFacilityCurrentBorrowingCapacity |

---

## Pattern 25: Facility with Borrowings Breakdown = CurrentBorrowingCapacity

### WRONG Pattern (from training errors):
- Entity: "400.0"
- Context: "$400.0 million secured revolving construction credit facility with $90.5 million of borrowings outstanding and $309.5 million of unused borrowing capacity"
- LLM Answer: `LineOfCreditFacilityMaximumBorrowingCapacity`
- **ERROR**: When context provides a breakdown of outstanding + unused, the entity refers to current state

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: "$X facility with $Y borrowings outstanding and $Z unused borrowing capacity"
- **Use**: `LineOfCreditFacilityCurrentBorrowingCapacity` (current borrowing state)

### How to Identify:
1. Look for breakdown: "borrowings outstanding" + "unused borrowing capacity"
2. The entity in this context is the CURRENT borrowing, not the maximum limit
3. Maximum is not explicitly stated, only the current state

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 400.0 | "$400.0 million facility with borrowings outstanding and unused capacity" | LineOfCreditFacilityCurrentBorrowingCapacity |

---

## Pattern 26: Issue Price Percentage = RedemptionPricePercentage

### WRONG Pattern (from training errors):
- Entity: "99.78"
- Context: "sold at an issue price of 99.78% of their face value"
- LLM Answer: `DebtInstrumentUnamortizedDiscount`
- **ERROR**: Issue price as percentage is redemption price, not unamortized discount

### RIGHT Pattern (correct tags):
- Entity: Percentage
- Context: "sold at an issue price of X% of face value", "issue price of X%"
- **ALWAYS** use: `DebtInstrumentRedemptionPricePercentage`

### Key Distinction:
- Issue price as PERCENTAGE (99.78%) → RedemptionPricePercentage
- Unamortized discount as DOLLAR AMOUNT → DebtInstrumentUnamortizedDiscount

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 99.78 | "sold at an issue price of 99.78% of their face value" | DebtInstrumentRedemptionPricePercentage |

---

## Pattern 27: "Remaining Outstanding Debt" = LongTermDebt (NOT CarryingAmount)

### WRONG Pattern (from training errors):
- Entity: "546,440"
- Context: "Company issued three notes totaling $546,440, which represented the remaining outstanding debt"
- LLM Answer: `DebtInstrumentCarryingAmount`
- **ERROR**: "Remaining outstanding debt" is general balance, not carrying amount

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: "remaining outstanding debt of $X", "represented the remaining outstanding debt"
- **Use**: `LongTermDebt` (general balance of debt remaining)

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 546,440 | "three notes totaling $546,440, which represented the remaining outstanding debt" | LongTermDebt |

---

## Pattern 28: Tranche A/B Facilities = DebtInstrumentFaceAmount

### WRONG Pattern (from training errors):
- Entity: "16.0"
- Context: "Tranche A loan revolving loan facility of up to $16.0 million"
- LLM Answer: `LineOfCreditFacilityMaximumBorrowingCapacity`
- **ERROR**: Tranche facilities are specific debt instruments, not revolving capacity

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: "Tranche A loan facility of up to $X", "Tranche B loan facility of $X"
- **Use**: `DebtInstrumentFaceAmount` (specific loan instrument amount)

### Key Distinction:
- Tranche facilities = specific debt instruments (Face Amount)
- Revolving credit facilities = capacity limits (MaximumBorrowingCapacity)

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 16.0 | "Tranche A loan revolving loan facility of up to $16.0 million" | DebtInstrumentFaceAmount |

---

## Pattern 29: "Indebtedness" in Facility Context = LineOfCredit

### WRONG Pattern (from training errors):
- Entity: "49.6"
- Context: "Company had $49.6 million of indebtedness and $3.8 million of letters of credit outstanding"
- LLM Answer: `DebtInstrumentCarryingAmount`
- **ERROR**: "Indebtedness" in facility context with letters of credit is general facility reference

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: "Company had $X million of indebtedness and $Y million of letters of credit outstanding"
- **Use**: `LineOfCredit` (general facility reference, not specific carrying amount)

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 49.6 | "Company had $49.6 million of indebtedness and $3.8 million of letters of credit outstanding" | LineOfCredit |

---

## Pattern 30: Facility Type - Term Loan vs Revolving Credit

### WRONG Pattern (from training errors):
- Entity: "150"
- Context: "$150 million senior revolving credit facility and $150 million term loan facility"
- LLM Answer: `LineOfCreditFacilityMaximumBorrowingCapacity` (for BOTH)
- **ERROR**: Model doesn't distinguish facility types - treats all "$X facility" as MaximumBorrowingCapacity

### RIGHT Pattern (correct tags):
- **CRITICAL DECISION**: Identify facility TYPE first, then apply appropriate tag
- Term loan facility → `DebtInstrumentFaceAmount` (specific debt instrument principal)
- Revolving credit facility → `LineOfCreditFacilityMaximumBorrowingCapacity` (borrowing limit)

### Key Distinction:
- **Term loan** = specific debt instrument with fixed principal → FaceAmount
- **Revolving credit** = flexible borrowing limit → MaximumBorrowingCapacity

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 150 | "$150 million term loan facility" | DebtInstrumentFaceAmount |
| 150 | "$150 million senior revolving credit facility" | LineOfCreditFacilityMaximumBorrowingCapacity |
| 264 | "term loan facility of $264 million" | DebtInstrumentFaceAmount |

### Reasoning Chain:
1. What type of facility is it?
   - If "term loan facility" → FaceAmount
   - If "revolving credit facility" → MaximumBorrowingCapacity
2. Don't just match on "facility" - the TYPE matters!

---

## Pattern 31: "Acquired/Entered Into a $X Facility" = MaximumBorrowingCapacity

### WRONG Pattern (from training errors):
- Entity: "45.0"
- Context: "we acquired a $45.0 million revolving credit facility"
- LLM Answer: `LineOfCredit`
- **ERROR**: "Acquired facility" is treated as general facility reference, not facility limit

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: "acquired/entered into/established a $X [type] facility"
- **ALWAYS** use: `LineOfCreditFacilityMaximumBorrowingCapacity`

### Key Distinction:
- **Action verb + $X facility** = facility establishment/limit → MaximumBorrowingCapacity
- **General facility reference without action** (e.g., "had $X of indebtedness") → LineOfCredit
- **"No outstanding"** → LineOfCredit

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 45.0 | "acquired a $45.0 million revolving credit facility" | LineOfCreditFacilityMaximumBorrowingCapacity |
| 2.25 | "entered into a $2.25 billion unsecured revolving credit facility" | LineOfCreditFacilityMaximumBorrowingCapacity |
| 45.0 | "had $45.0 million of indebtedness" (no action verb) | LineOfCredit |

---

## Pattern 32: Incomplete/Truncated Context = Default to FaceAmount for Financing Agreements

### WRONG Pattern (from training errors):
- Entity: "50,000"
- Context: "On November 4, 2015, the Company entered into an Agreement with One-Seven, its Managing Partner Douglas Stukel ("
- LLM Answer: "Insufficient context to determine appropriate XBRL tag"
- **ERROR**: Model gives up on truncated sentences instead of using available clues

### RIGHT Pattern (correct tags):
- Entity: Dollar amount
- Context: Dollar amount in financing/agreement context (truncated or complete)
- **Default assumption**: `DebtInstrumentFaceAmount` (debt instrument principal)
- Unless other indicators present: "outstanding" → CarryingAmount, "facility" → MaximumBorrowingCapacity, etc.

### Key Principle:
Dollar amounts in financing/agreement contexts usually indicate DEBT INSTRUMENT FACE AMOUNTS unless other context clearly indicates otherwise.

### Examples:
| Entity | Context Phrase | Correct Tag |
|--------|---------------|-------------|
| 50,000 | "entered into an Agreement with [Entity] for $50,000" (truncated) | DebtInstrumentFaceAmount |
| 36,000 | "closing of financing to the Parent of $36,000,000" (M&A) | DebtInstrumentFaceAmount |

### Reasoning Chain for Incomplete Context:
1. Is the entity a dollar amount?
   - YES → Continue
   - NO → Use other context clues

2. Is there "outstanding", "borrowed", "fair value", "carrying", "discount"?
   - YES → Use appropriate debt instrument tag
   - NO → Continue

3. Is there "facility", "credit facility", "revolving", "line of credit"?
   - YES → Use MaximumBorrowingCapacity
   - NO → Continue

4. Is this in a financing/agreement context (even if truncated)?
   - YES → Default to DebtInstrumentFaceAmount
   - NO → Re-examine context

### Anti-Pattern to Avoid:
- WRONG: "I don't have enough context" → Skip/Decline
- RIGHT: "This is a dollar amount in financing context → DebtInstrumentFaceAmount"
