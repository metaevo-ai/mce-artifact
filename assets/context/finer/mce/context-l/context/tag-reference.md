# XBRL Tag Reference: Per-Tag Decision Rules

## Interest Rate Tags

### DebtInstrumentBasisSpreadOnVariableRate1
**Definition**: The percentage margin added to a benchmark interest rate (LIBOR, base rate, etc.)

**Key Phrases (ALWAYS indicates this tag)**:
- "plus a margin of X%"
- "LIBOR plus X%"
- "X% above [benchmark]"
- "X% to Y% above LIBOR"
- "base rate plus X%"

**What to EXCLUDE**:
- Total/stated interest rates (use `DebtInstrumentInterestRateStatedPercentage`)
- Effective rates after adjustments (NOT this tag)
- Redemption prices (use `DebtInstrumentRedemptionPricePercentage`)

**Example from Training**:
- ✅ CORRECT: "rates charged are 1.000% to 1.750% above adjusted LIBOR" → BasisSpread
- ✅ CORRECT: "bears interest at either LIBOR plus 2%" → BasisSpread
- ✅ CORRECT: "margin of 3.75% during the last two years" → BasisSpread

---

### DebtInstrumentInterestRateStatedPercentage
**Definition**: The stated/total interest rate written on a debt instrument

**Key Phrases**:
- "X% [Name] Notes" (naming pattern: "8.375% Senior Notes")
- "interest rate of X%"
- "X% per annum" (when NOT with "plus" or "above")
- "bears interest at X%"
- "fixed rate of X%"
- "pay a rate of X% per year"

**What to EXCLUDE**:
- Basis spreads/margins (use `DebtInstrumentBasisSpreadOnVariableRate1`)
- Interest expense amounts (NOT a tag for percentage values)

**Example from Training**:
- ✅ CORRECT: "Interest was payable... at 6% per annum" → StatedPercentage
- ✅ CORRECT: "The 8.375% Senior Notes due 2022" → StatedPercentage

---

## Credit Facility Capacity Tags

### LineOfCreditFacilityMaximumBorrowingCapacity
**Definition**: The maximum amount that can be borrowed under a credit facility

**Key Phrases**:
- "up to $X billion/million"
- "aggregate revolving credit facility of up to $X"
- "increased to $X" (when facility limit changes)
- "maximum aggregate principal amount of $X"
- "total term loan commitments of $X"
- "$X billion revolving credit facility" (when describing the facility size)
- "capacity was increased to $X"
- "we entered into a $X [billion/million] revolving credit facility"

**CRITICAL EXCLUSION - When NOT to use this tag**:
- "allowing to borrow in a single drawing up to $X" → Use `LineOfCreditFacilityCurrentBorrowingCapacity`
- Term loan facility amounts → Use `DebtInstrumentFaceAmount`
- Amounts described as "outstanding borrowings" → Use `LineOfCreditFacilityCurrentBorrowingCapacity`

**What to EXCLUDE**:
- Current outstanding borrowings (use `LineOfCreditFacilityCurrentBorrowingCapacity`)
- Available remaining capacity (use `LineOfCreditFacilityRemainingBorrowingCapacity`)
- General facility references without capacity language (use `LineOfCredit`)
- Revolving credit facilities when context is just the facility (use `LineOfCredit`)

**IMPORTANT**: When a credit facility is described as "$X billion revolving credit facility" without "up to" or explicit capacity limit language, this may be a general facility reference. Use `LineOfCredit` unless "up to", "capacity", or similar explicit limit language is present.

**Example from Training**:
- ✅ CORRECT: "entered into a $1.0 billion revolving credit agreement" → MaximumBorrowingCapacity
- ✅ CORRECT: "increased the amount of revolving commitments... to $1.99 billion" → MaximumBorrowingCapacity
- ✅ CORRECT: "permitted to issue up to $60 million of letters of credit" → MaximumBorrowingCapacity
- ❌ WRONG: "Amended and Restated Note Purchase and Private Shelf Agreement in the amount of $175.0 million" → DebtInstrumentFaceAmount (incorrect)
- ✅ CORRECT: "Amended and Restated Note Purchase and Private Shelf Agreement in the amount of $175.0 million" → MaximumBorrowingCapacity (corrected)

---

### LineOfCreditFacilityCurrentBorrowingCapacity
**Definition**: The amount currently borrowed/outstanding under a facility

**Key Phrases**:
- "outstanding borrowings of $X"
- "amount outstanding"
- "borrowings outstanding"
- "$X million outstanding borrowings"
- "drawn amount"
- "allowing to borrow in a single drawing up to $X" (CRITICAL: this describes current borrowing mechanism)

**CRITICAL ADDITION - The "Allowing to Borrow" Pattern**:
- Phrase: "allowing to borrow in a single drawing up to $X"
- This indicates the current borrowing mechanism/limit of the facility
- Example: "The Credit Agreement contains a 7-year term loan feature allowing the Operating Partnership to borrow in a single drawing up to $250 million" → CurrentBorrowingCapacity

**What to EXCLUDE**:
- Maximum facility limits (use `LineOfCreditFacilityMaximumBorrowingCapacity`)
- General facility references (use `LineOfCredit`)

**Example from Training**:
- ✅ CORRECT: "$70.0 million outstanding borrowings" → CurrentBorrowingCapacity (context-dependent)
- ✅ CORRECT: "$618.0 million is available to borrow" → CurrentBorrowingCapacity
- ✅ CORRECT: "allowing to borrow in a single drawing up to $250 million" → CurrentBorrowingCapacity (was incorrectly tagged as MaximumBorrowingCapacity)
- ❌ WRONG: "total availability to $1,150,000" → MaximumBorrowingCapacity (incorrect)
- ✅ CORRECT: "total availability to $1,150,000" → CurrentBorrowingCapacity (corrected)
- ❌ WRONG: "$400.0 million secured revolving construction credit facility with borrowings outstanding" → MaximumBorrowingCapacity (incorrect)
- ✅ CORRECT: "$400.0 million secured revolving construction credit facility with borrowings outstanding" → CurrentBorrowingCapacity (corrected)

---

### LineOfCredit
**Definition**: General reference to a line of credit facility (no specific dollar amount entity)

**Key Phrases**:
- "revolving credit facility" (without capacity amount)
- "no borrowings outstanding under the [facility]"
- "no outstanding balance"

**What to EXCLUDE**:
- Specific dollar amounts (use capacity tags)
- Interest rates (use interest tags)

**Example from Training**:
- ✅ CORRECT: "no borrowings outstanding" → LineOfCredit
- ❌ WRONG: "Company had $49.6 million of indebtedness and $3.8 million of letters of credit outstanding" → DebtInstrumentCarryingAmount (incorrect)
- ✅ CORRECT: "Company had $49.6 million of indebtedness and $3.8 million of letters of credit outstanding" → LineOfCredit (corrected)

---

## Long-Term Debt Tags

### LongTermDebt
**Definition**: General long-term debt balance/carrying amount on balance sheet

**Key Phrases**:
- "long-term debt as of [date]"
- "balance of the term loan was $X"
- "long-term debt consisted of the following"
- "mortgage notes on land and other debt was $X"
- "$X billion under the Term Loan [name]" (general term loan balance)
- "outstanding amount related to the [note]" (balance sheet context)

**CRITICAL ADDITION - General Balance Sheet Context**:
- When context is general disclosure like "As of [date], the outstanding amount related to the [note] was $X"
- NO mention of "carrying amount" or "including accrued interest"
- General reference to outstanding amounts on balance sheet → LongTermDebt

**Example**: "As of both May 31, 2016 and November 30, 2015, the outstanding amount related to the 5-year senior unsecured note was $30.3 million" → LongTermDebt (NOT CarryingAmount)

**What to EXCLUDE**:
- Fair value amounts (use `LongTermDebtFairValue`)
- Face/principal amounts of specific notes (use `DebtInstrumentFaceAmount`)
- Specific debt instrument carrying amounts (use `DebtInstrumentCarryingAmount`)

**CRITICAL DISTINCTION**: When referring to "balance of the term loan" or amounts "under the Term Loan Facility", use `LongTermDebt` for general term loan balances. Do NOT use `DebtInstrumentCarryingAmount` unless specifically referring to the book value of the instrument with accrued interest.

**Example from Training**:
- ✅ CORRECT: "balance of the 2016 Term Loan was $273.4 million" → LongTermDebt
- ✅ CORRECT: "carrying amount of the mortgage notes on land... was $278.4 million" → LongTermDebt
- ✅ CORRECT: "$1.99 billion under the Term Loan B Facility" → LongTermDebt
- ❌ WRONG: "$1.99 billion under the Term Loan B Facility" → DebtInstrumentCarryingAmount (incorrect)
- ✅ CORRECT: "outstanding amount related to the 5-year senior note" (balance sheet context) → LongTermDebt (was incorrectly tagged as CarryingAmount)
- ❌ WRONG: "three notes totaling $546,440, which represented the remaining outstanding debt" → DebtInstrumentCarryingAmount (incorrect)
- ✅ CORRECT: "three notes totaling $546,440, which represented the remaining outstanding debt" → LongTermDebt (corrected)

---

### LongTermDebtFairValue
**Definition**: Fair value of long-term debt (market-based estimate)

**Key Phrases**:
- "fair value of long-term debt"
- "quoted market prices" for long-term debt
- "estimated at $X" for long-term debt fair value
- "fair value was $X million" for debt instruments

**CRITICAL**: Use this tag for ANY fair value of debt instruments, NOT `DebtInstrumentFairValue`

**What to EXCLUDE**:
- Carrying/book values (use `LongTermDebt`)
- Face/principal amounts (use `DebtInstrumentFaceAmount`)

**Example from Training**:
- ✅ CORRECT: "fair value of the Company's long-term debt... $32,109" → LongTermDebtFairValue
- ✅ CORRECT: "fair value of these Notes... were $649.7 million" → LongTermDebtFairValue
- ✅ CORRECT: "fair value of our long-term debt... was $638 million" → LongTermDebtFairValue

---

## Debt Instrument Tags

### DebtInstrumentFaceAmount
**Definition**: Principal/face amount of a specific debt instrument

**Key Phrases**:
- "aggregate principal amount of $X"
- "face amount"
- "principal balance of $X note"
- "issued $X million of [notes]"
- "$X million note" (specific instrument issuance)
- "term loan facility of $X" (NOT revolving credit facility - term loan = face amount)
- "received a loan of $X from [entity]"
- "advances under the CPN of $X" (advances received, not balance)
- "closing of financing to the [entity] of $X" (M&A financing context)

**CRITICAL DISTINCTION - Term Loan vs Revolving Credit**:
- Term loan facility amount → `DebtInstrumentFaceAmount` (the loan principal)
- Revolving credit facility amount → `LineOfCreditFacilityMaximumBorrowingCapacity` (the available limit)

**Example**: "entered into a 12-month €225 million term loan facility" → DebtInstrumentFaceAmount (NOT MaximumBorrowingCapacity)

**What to EXCLUDE**:
- Facility capacities (use `LineOfCreditFacilityMaximumBorrowingCapacity`)
- Fair values (use `LongTermDebtFairValue`)
- Outstanding principal balance (use `DebtInstrumentCarryingAmount`)
- Amounts after repricing or modification (use `DebtInstrumentCarryingAmount`)

**Example from Training**:
- ✅ CORRECT: "issued... with an aggregate principal amount of $575 million" → FaceAmount
- ✅ CORRECT: "issued the buyer a $675,000 note" → FaceAmount
- ✅ CORRECT: "entered into a 12-month €225 million term loan facility" → FaceAmount (was incorrectly tagged as MaximumBorrowingCapacity)
- ✅ CORRECT: "we received a loan of $150,000 from the IEDA" → FaceAmount (was incorrectly tagged as LongTermDebt)
- ✅ CORRECT: "advances under the March 2016 $1,000,000 CPN of $95,000" → FaceAmount (was incorrectly tagged as CarryingAmount)
- ✅ CORRECT: "closing of financing to the Parent of $36,000,000" → FaceAmount (was incorrectly tagged as ProceedsFromIssuanceOfCommonStock)
- ❌ WRONG: "Tranche A loan revolving loan facility of up to $16.0 million" → LineOfCreditFacilityMaximumBorrowingCapacity (incorrect)
- ✅ CORRECT: "Tranche A loan revolving loan facility of up to $16.0 million" → FaceAmount (corrected)

---

### DebtInstrumentCarryingAmount
**Definition**: Book value of debt instrument including principal and accrued interest

**Key Phrases**:
- "carrying amount of the [instrument]"
- "balance including principal and accrued interest"
- "net of unamortized debt discounts"
- "$X was outstanding under the [credit facility]" (amounts borrowed against a facility)
- "$X outstanding borrowings" (when referring to actual debt borrowed)
- "outstanding principal balance of $X" (CRITICAL: current remaining balance, not original)

**CRITICAL ADDITION - "Outstanding Principal Balance" Pattern**:
- Phrase: "outstanding principal balance"
- Meaning: The CURRENT remaining principal, not the original amount borrowed
- Example: "a loan with a $4.2 million outstanding principal balance" → CarryingAmount (NOT FaceAmount)

**CRITICAL ADDITION - Amounts After Repricing**:
- When debt has been repriced and the amount is the NEW carrying amount → CarryingAmount
- Example: "$1,695.8 million senior secured Term Loan B facility" (after repricing) → CarryingAmount (NOT MaximumBorrowingCapacity)

**CRITICAL ADDITION - Foreign Currency Translation**:
- When amount is translated to USD at spot rate → CarryingAmount (current value)
- Example: "£475 million principal outstanding, translated to U.S. dollars at the spot rate" → CarryingAmount (NOT FaceAmount)

**What to EXCLUDE**:
- General long-term debt (use `LongTermDebt`)
- Maximum capacities (use capacity tags)
- Current borrowing capacity of a facility (use `LineOfCreditFacilityCurrentBorrowingCapacity`)
- Original principal amounts at issuance (use `DebtInstrumentFaceAmount`)

**CRITICAL DISTINCTION**: "Outstanding under [facility]" indicates the debt instrument carrying amount, NOT the facility's current borrowing capacity. The phrasing "under the [facility]" indicates the debt is the instrument, not the facility capacity.

**Example from Training**:
- ✅ CORRECT: "Aggregate borrowings... were $31.1 million" → CarryingAmount
- ✅ CORRECT: "$70.0 million outstanding borrowings" → CarryingAmount (context-dependent)
- ✅ CORRECT: "$60 million was outstanding under the Revolving Credit Facility" → CarryingAmount
- ❌ WRONG: "$60 million was outstanding under the Revolving Credit Facility" → CurrentBorrowingCapacity (incorrect)
- ✅ CORRECT: "$4.2 million outstanding principal balance" → CarryingAmount (was incorrectly tagged as FaceAmount)
- ✅ CORRECT: "$1,695.8 million Term Loan B facility" (after repricing) → CarryingAmount (was incorrectly tagged as MaximumBorrowingCapacity)
- ✅ CORRECT: "£475 million principal outstanding, translated at spot rate" → CarryingAmount (was incorrectly tagged as FaceAmount)

---

### DebtInstrumentUnamortizedDiscount
**Definition**: Remaining unamortized discount on debt instruments

**Key Phrases**:
- "unamortized discount of $X"
- "discount remains unamortized"
- "discount on the Term Loan"
- "net of unamortized debt discounts of $X"

**Example from Training**:
- ✅ CORRECT: "net of unamortized debt discounts of $215.7 million" → UnamortizedDiscount
- ✅ CORRECT: "discount of $2.5 million... remains unamortized" → UnamortizedDiscount

---

### DebtInstrumentRedemptionPricePercentage
**Definition**: Percentage price for redeeming/repurchasing debt

**Key Phrases**:
- "repurchase at a price of X% of principal"
- "redemption price equal to X%"
- "purchase price of X% of principal amount"

**Example from Training**:
- ✅ CORRECT: "offer to repurchase... at a purchase price of 101.00% of principal amount" → RedemptionPricePercentage
- ❌ WRONG: "sold at an issue price of 99.78% of their face value" → DebtInstrumentUnamortizedDiscount (incorrect)
- ✅ CORRECT: "sold at an issue price of 99.78% of their face value" → RedemptionPricePercentage (corrected)

---

## Letters of Credit Tags

### LettersOfCreditOutstandingAmount
**Definition**: Dollar amount of letters of credit currently outstanding

**Key Phrases**:
- "letters of credit were outstanding"
- "$X million of letters of credit were outstanding"
- "outstanding letters of credit and bank guarantees"

**What to EXCLUDE**:
- Maximum capacity for letters of credit (use `LineOfCreditFacilityMaximumBorrowingCapacity`)

**Example from Training**:
- ✅ CORRECT: "$15 million of letters of credit were outstanding" → LettersOfCreditOutstandingAmount
- ✅ CORRECT: "$41.8 million... outstanding letters of credit" → LettersOfCreditOutstandingAmount
- ❌ WRONG: "letter of credit in the initial amount of $450.0 million" → DebtInstrumentFaceAmount (incorrect)
- ✅ CORRECT: "letter of credit in the initial amount of $450.0 million" → LettersOfCreditOutstandingAmount (corrected)

---

## Decision Rules: When to Use Each Tag

### Decision 1: Term Loan Facility vs Revolving Credit Facility

**The Rule**: The facility TYPE determines the tag, not just the word "facility".

**IF "$X term loan facility"**:
→ Use `DebtInstrumentFaceAmount`
→ Reasoning: Term loans are specific debt instruments with a fixed principal

**IF "$X revolving credit facility"**:
→ Use `LineOfCreditFacilityMaximumBorrowingCapacity`
→ Reasoning: Revolving facilities have a flexible borrowing limit

**Examples**:
- ✅ CORRECT: "$150 million term loan facility" → DebtInstrumentFaceAmount
- ✅ CORRECT: "$150 million senior revolving credit facility" → LineOfCreditFacilityMaximumBorrowingCapacity
- ❌ WRONG: "$150 million term loan facility" → LineOfCreditFacilityMaximumBorrowingCapacity (incorrect)
- ✅ CORRECT: "$150 million term loan facility" → DebtInstrumentFaceAmount (corrected)
- ❌ WRONG: "$264 million term loan facility" → LineOfCreditFacilityMaximumBorrowingCapacity (incorrect)
- ✅ CORRECT: "$264 million term loan facility" → DebtInstrumentFaceAmount (corrected)

### Decision 2: "Acquired/Entered Into $X Facility" vs General Facility Reference

**The Rule**: Action verbs + "$X facility" = MaximumBorrowingCapacity; General references = LineOfCredit

**IF "acquired/entered into/established a $X facility"**:
→ Use `LineOfCreditFacilityMaximumBorrowingCapacity`
→ Reasoning: The action establishes the facility limit

**IF "had $X of indebtedness" (no action verb)**:
→ Use `LineOfCredit`
→ Reasoning: General facility reference without specific limit

**Examples**:
- ✅ CORRECT: "acquired a $45.0 million revolving credit facility" → LineOfCreditFacilityMaximumBorrowingCapacity
- ❌ WRONG: "acquired a $45.0 million revolving credit facility" → LineOfCredit (incorrect)
- ✅ CORRECT: "acquired a $45.0 million revolving credit facility" → LineOfCreditFacilityMaximumBorrowingCapacity (corrected)
- ✅ CORRECT: "entered into a $2.25 billion unsecured revolving credit facility" → LineOfCreditFacilityMaximumBorrowingCapacity

### Decision 3: Incomplete/Truncated Context in Financing Agreements

**The Rule**: Dollar amounts in financing contexts default to FaceAmount unless other indicators present

**IF dollar amount in financing/agreement context (even if truncated)**:
→ Use `DebtInstrumentFaceAmount` as default assumption
→ Reasoning: Financing agreements typically involve debt instrument principals

**When NOT to use FaceAmount**:
- "outstanding"/"borrowed" → CarryingAmount
- "fair value" → LongTermDebtFairValue
- "facility"/"credit facility" → MaximumBorrowingCapacity
- "discount"/"unamortized" → UnamortizedDiscount

**Examples**:
- ✅ CORRECT: "entered into an Agreement with [Entity] for $50,000" (truncated) → DebtInstrumentFaceAmount
- ❌ WRONG: "entered into an Agreement with [Entity] for $50,000" → "Insufficient context" (incorrect)
- ✅ CORRECT: "entered into an Agreement with [Entity] for $50,000" → DebtInstrumentFaceAmount (corrected)

---
