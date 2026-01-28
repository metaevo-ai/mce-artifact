# XBRL Tag Classification: Semantic Disambiguation Guide

## Critical Distinctions for Error Prevention

This guide addresses the most common misclassification patterns identified from training data analysis.

---

## 1. Interest Rate vs Basis Spread

**THE DECISIVE RULE**: If a percentage is expressed as a **margin added to a benchmark rate** (LIBOR, base rate, etc.), it is **ALWAYS** `DebtInstrumentBasisSpreadOnVariableRate1`, NOT a stated interest rate.

### Basis Spread Indicators (use `DebtInstrumentBasisSpreadOnVariableRate1`):
- "plus a margin of X%"
- "LIBOR plus X%"
- "above the adjusted LIBOR rate"
- "X% to Y% above LIBOR"
- "base rate plus X%"
- "plus X% per annum"

### Stated Interest Rate Indicators (use `DebtInstrumentInterestRateStatedPercentage`):
- The rate written on/named after the note: "8.375% Senior Notes", "4.50% notes due 2034"
- "interest rate of X%" without reference to adding to a benchmark
- "bears interest at X%"
- "pay a fixed rate of X% per year"
- "X% per annum" without "plus" or "above" language

### WRONG → RIGHT Examples from Training Data:
1. "margin of 3.75% during the last two years" → `DebtInstrumentBasisSpreadOnVariableRate1` (NOT StatedPercentage)
2. "rates of interest charged are 1.000% to 1.750% above adjusted LIBOR" → `DebtInstrumentBasisSpreadOnVariableRate1` (NOT InterestRateEffectivePercentage)
3. "bears interest at either LIBOR plus 2%" → `DebtInstrumentBasisSpreadOnVariableRate1` (NOT LineOfCreditFacilityInterestRateAtPeriodEnd)
4. "Interest was payable... at 6% per annum" → `DebtInstrumentInterestRateStatedPercentage` (NOT InterestExpense)

---

## 2. Credit Facility Capacity: Maximum vs Current

### Maximum Borrowing Capacity Indicators (use `LineOfCreditFacilityMaximumBorrowingCapacity`):
- "up to $X billion/million"
- "revolving credit facility of up to $X"
- "increased to $X" (when facility limit is increased)
- "aggregate revolving credit facility of up to $X"
- "credit facility of $X billion" when describing facility SIZE/LIMIT
- "total term loan commitments of $X"
- "maximum aggregate principal amount was increased to $X"
- "capacity was increased to $X"

### When to use `DebtInstrumentFaceAmount`:
- "$X billion revolving credit agreement" (without "up to" or capacity language)
- This is the face amount/committed amount of the facility agreement itself
- The phrase "revolving credit agreement" indicates a debt instrument, not a facility capacity

### Current Borrowing Capacity Indicators (use `LineOfCreditFacilityCurrentBorrowingCapacity`):
- "outstanding borrowings of $X"
- "amount outstanding"
- "borrowings outstanding under the facility"
- "$X million outstanding borrowings"
- "drawn amount"
- "available to borrow without adding additional properties" (specific current availability)

### Current vs Maximum Context Clues:
- When sentence mentions "$X billion" facility LIMIT and no borrowing mentioned → Maximum
- When sentence mentions "$X million outstanding" → Current
- When comparing two facilities and asking about one specific amount → examine context carefully

### CRITICAL: "Allowing to borrow in a single drawing up to $X"
- This phrase indicates the current borrowing mechanism/limit, NOT the maximum facility capacity
- **ALWAYS** use `LineOfCreditFacilityCurrentBorrowingCapacity` when entity is described as "allowing to borrow in a single drawing up to $X"
- Example: "The Credit Agreement contains a 7-year term loan feature allowing the Operating Partnership to borrow in a single drawing up to $250 million" → CurrentBorrowingCapacity (NOT MaximumBorrowingCapacity)

### WRONG → RIGHT Examples:
1. "permitted to issue up to $60 million of letters of credit" → `LineOfCreditFacilityMaximumBorrowingCapacity` (NOT LettersOfCreditOutstandingAmount)
2. "entered into a $1.0 billion revolving credit agreement" → `DebtInstrumentFaceAmount` (NOT LineOfCreditFacilityMaximumBorrowingCapacity) - "credit agreement" without capacity language
3. "increased the amount of revolving commitments... aggregate of up to $1.99 billion" → `LineOfCreditFacilityMaximumBorrowingCapacity` (NOT DebtInstrumentFaceAmount)
4. "increased to $400,000,000" → `LineOfCreditFacilityMaximumBorrowingCapacity` (NOT LineOfCredit)
5. "increased the capacity... from $350 million to $530 million" → `LineOfCreditFacilityMaximumBorrowingCapacity` (NOT LineOfCredit)
6. "including a $500 million credit facility" (one of two totaling $1 billion) → `LineOfCreditFacilityCurrentBorrowingCapacity` if context implies what exists NOW, not limit (LLM said Maximum, needs context check)
7. "allowing to borrow in a single drawing up to $250 million" → `LineOfCreditFacilityCurrentBorrowingCapacity` (NOT MaximumBorrowingCapacity) - this describes current borrowing mechanism

---

## 3. LongTermDebt Hierarchy: General vs Specific Tags

### General Long-Term Debt Tag (use `LongTermDebt`):
- General references to "long-term debt" balance/amount
- Carrying amount of long-term debt on balance sheet
- "balance of the term loan was $X"
- When not explicitly stating "fair value" or "face amount"

### Long-Term Debt Fair Value (use `LongTermDebtFairValue`):
- **ALWAYS** use this when sentence contains "fair value" AND the amount is for long-term debt
- "fair value of long-term debt is estimated at $X"
- "quoted market prices" for long-term debt
- "estimated the fair value"

### Specific Debt Tags (use when applicable):
- `DebtInstrumentFaceAmount`: Principal/face amount of specific notes
- `DebtInstrumentCarryingAmount`: Book value with accrued interest
- `DebtInstrumentFairValue`: Fair value of specific INSTRUMENT (not general long-term debt)

### CRITICAL DISTINCTION: LongTermDebtFairValue vs DebtInstrumentFairValue
- `LongTermDebtFairValue`: Fair value of long-term debt AS A CATEGORY
- `DebtInstrumentFairValue`: Fair value of specific debt instruments

### WRONG → RIGHT Examples:
1. "fair value of these Notes... were $649.7 million" → `LongTermDebtFairValue` (NOT DebtInstrumentFairValue)
2. "balance of the 2016 Term Loan was $273.4 million" → `LongTermDebt` (NOT DebtInstrumentCarryingAmount)
3. "$70.0 million outstanding borrowings" → `DebtInstrumentCarryingAmount` (NOT LineOfCreditFacilityCurrentBorrowingCapacity) - context shows this is carrying amount of borrowings, not capacity
4. "$0.7 billion of repurchase agreements and revolving credit facilities that are considered long-term" → `LongTermDebtFairValue` (NOT CurrentBorrowingCapacity)

---

## 4. LineOfCredit vs Specific Amount Tags

### LineOfCredit (use for general facility references):
- When no specific dollar amount is being tagged
- Entity is "no" or similar indicating absence of borrowing
- General reference to facility without capacity or outstanding amount
- "no outstanding balance under the revolving credit facility"

### Specific Amount Tags (use when entity IS a dollar amount):
- `LineOfCreditFacilityMaximumBorrowingCapacity`: For maximum facility limits
- `LineOfCreditFacilityCurrentBorrowingCapacity`: For outstanding amounts
- `LineOfCreditFacilityRemainingBorrowingCapacity`: For available but unused capacity

### WRONG → RIGHT Example:
1. "no borrowings outstanding" → `LineOfCredit` (NOT LineOfCreditFacilityRemainingBorrowingCapacity)

---

## Quick Decision Tree

### If entity is a PERCENTAGE:
1. Is it a "margin of X%", "plus X%", "X% above LIBOR/base rate"?
   - YES → `DebtInstrumentBasisSpreadOnVariableRate1`
   - NO → `DebtInstrumentInterestRateStatedPercentage`

### If entity is a DOLLAR AMOUNT for CREDIT FACILITY:
1. Does sentence say "up to $X", "increased to $X", "commitments of $X", "facility of $X"?
   - YES → `LineOfCreditFacilityMaximumBorrowingCapacity`
2. Does sentence say "outstanding borrowings of $X", "amount outstanding", "$X outstanding"?
   - YES → `LineOfCreditFacilityCurrentBorrowingCapacity`
3. Is the amount described as "outstanding under [facility name]"?
   - YES → This is likely the carrying amount of the debt, NOT facility capacity. Check if sentence mentions "revolving credit facility" or similar. If yes and the context is about borrowings, consider `DebtInstrumentCarryingAmount`.

### If entity is a DOLLAR AMOUNT for DEBT:
1. Does sentence say "fair value of long-term debt"?
   - YES → `LongTermDebtFairValue`
2. Is it the "balance of the term loan" or general long-term debt amount?
   - YES → `LongTermDebt`
3. Is it specifically the principal/face amount?
   - YES → `DebtInstrumentFaceAmount`
4. Is it described as "outstanding under" a credit facility (e.g., "outstanding under the Revolving Credit Facility")?
   - YES → This is likely `DebtInstrumentCarryingAmount` or `LongTermDebt`, NOT facility capacity tag. The "under" phrasing indicates the debt instrument, not the facility.

### If entity is NOT a NUMBER (e.g., "no", "zero"):
1. Does sentence reference a credit facility with no borrowings?
   - YES → `LineOfCredit`

### LIBOR PERCENTAGE SPECIAL CASE:
1. Is the entity an absolute LIBOR rate like "2.51%" (not "LIBOR plus X%" or "X% above LIBOR")?
   - YES → This is NOT a basis spread. Use extreme caution - the correct tag may depend on context. When in doubt, check if this represents a spread or an absolute rate value.

---

## 6. Compound Subject Parsing: How to Identify What the Amount Modifies

### The Rule:
In compound subjects with multiple items, **the dollar amount modifies the FIRST item only**.

### Pattern: "$X [Item A], $Y [Item B], and $Z [Item C]"
- Always parse from left to right
- Example: "$90.0 million outstanding borrowings, $1.2 million in letters of credit outstanding and $28.8 million of available borrowing capacity"
  - $90.0M → outstanding borrowings
  - $1.2M → letters of credit outstanding
  - $28.8M → available borrowing capacity

### Application to Errors:
- **id 76**: "$90.0 million outstanding borrowings, $1.2 million in letters of credit outstanding"
  - Entity: 90.0
  - Modifies: "outstanding borrowings" (first item)
  - **WRONG** LLM Answer: `DebtInstrumentCarryingAmount`
  - **RIGHT** Tag: `LettersOfCreditOutstandingAmount` (context shows borrowings are part of credit facility context with letters of credit)

---

## 7. Face Amount vs Carrying Amount: Critical Distinctions

### When "Outstanding Principal Balance" = CarryingAmount (NOT FaceAmount):
- **Key indicator**: "outstanding principal balance" refers to the CURRENT remaining principal, not the original amount borrowed
- The word "outstanding" here means "remaining" or "currently owed"
- Example: "a $0.4 million payment guarantee on a loan with a $4.2 million outstanding principal balance"
  - $4.2M is the current remaining balance → `DebtInstrumentCarryingAmount`

### When "Principal" = FaceAmount:
- **Key indicators**:
  - "aggregate principal amount of $X" (issuance/borrowing)
  - "issued $X million of notes"
  - "received a loan of $X"
  - Advances received under a CPN (convertible promissory note)
  - Term loan facility amounts
- The word "principal" refers to the original/face amount borrowed

### When "Principal Outstanding" with Translation = CarryingAmount:
- **Key indicator**: Amount translated at spot rate indicates current value, not original face
- Example: "£475 million principal outstanding, translated to U.S. dollars at the spot rate"
  - Current value at reporting date → `DebtInstrumentCarryingAmount`

### Decision Tree for Principal Amounts:
1. Does the context say "outstanding principal balance"?
   - YES → `DebtInstrumentCarryingAmount`
2. Does it say "aggregate principal amount of $X" or "issued $X" (issuance context)?
   - YES → `DebtInstrumentFaceAmount`
3. Is the amount being translated to USD at a spot rate?
   - YES → `DebtInstrumentCarryingAmount` (current value)
4. Is it advances received (not balance remaining)?
   - YES → `DebtInstrumentFaceAmount`

### WRONG → RIGHT Examples:
1. "$4.2 million outstanding principal balance" → `DebtInstrumentCarryingAmount` (NOT FaceAmount)
2. "advances under the March 2016 $1,000,000 CPN of $95,000" → `DebtInstrumentFaceAmount` (NOT CarryingAmount)
3. "£475 million principal outstanding, translated to U.S. dollars at spot rate" → `DebtInstrumentCarryingAmount` (NOT FaceAmount)

---

## 8. LongTermDebt vs DebtInstrumentCarryingAmount

### General Long-Term Debt (use `LongTermDebt`):
- **Balance sheet context**: "As of [date], the outstanding amount related to the [note] was $X"
- **No mention of "carrying amount" or "including accrued interest"**
- **General references to outstanding amounts**
- Example: "As of both May 31, 2016 and November 30, 2015, the outstanding amount related to the 5-year senior unsecured note was $30.3 million" → `LongTermDebt`

### Specific Carrying Amount (use `DebtInstrumentCarryingAmount`):
- **Explicit carrying language**: "carrying amount", "including principal and accrued interest"
- **Amounts outstanding under a specific facility** (when debt instrument is implied)
- Example: "Aggregate borrowings under the facility were $31.1 million" → `DebtInstrumentCarryingAmount`

### Decision Tree:
1. Is the context a general balance sheet disclosure (e.g., "As of [date]")?
   - YES → Likely `LongTermDebt`
2. Does the context mention "carrying amount" or "including accrued interest"?
   - YES → `DebtInstrumentCarryingAmount`
3. Is it specifically "outstanding under [facility name]"?
   - YES → `DebtInstrumentCarryingAmount`

### WRONG → RIGHT Examples:
1. "outstanding amount related to the 5-year senior note" (balance sheet context) → `LongTermDebt` (NOT CarryingAmount)
2. "balance including principal and accrued interest" → `DebtInstrumentCarryingAmount` (NOT LongTermDebt)

---

## 10. Letters of Credit Amounts

### LettersOfCreditOutstandingAmount Indicators (use this tag):
- Dollar amounts associated specifically with letters of credit
- "letter of credit in the initial amount of $X"
- "$X million of letters of credit were outstanding"
- Any dollar amount referenced in context of letters of credit issuance/amount

### What to EXCLUDE:
- Maximum capacity for letters of credit (use `LineOfCreditFacilityMaximumBorrowingCapacity`)
- General debt instrument face amounts (use `DebtInstrumentFaceAmount`)

### CRITICAL RULE:
If the context mentions "letter of credit" (singular or plural) AND the entity is a dollar amount, the tag should be `LettersOfCreditOutstandingAmount`, NOT `DebtInstrumentFaceAmount`.

### WRONG → RIGHT Examples:
1. "letter of credit in the initial amount of $450.0 million" → `LettersOfCreditOutstandingAmount` (NOT DebtInstrumentFaceAmount)
2. "$15 million of letters of credit were outstanding" → `LettersOfCreditOutstandingAmount` (NOT DebtInstrumentFaceAmount)

---

## 11. M&A Financing Context: Debt vs Equity

### When "Financing" = DebtInstrumentFaceAmount:
- **Context**: M&A or corporate transaction
- **Key indicators**: Specific dollar amount, closing conditions, debt issuance
- Example: "closing of financing to the Parent of $36,000,000" → `DebtInstrumentFaceAmount`

### When "Financing" = ProceedsFromIssuanceOfCommonStock:
- **Context**: Explicitly mentions stock/equity issuance
- **Key indicators**: "common stock", "equity", "shares"
- This tag is NOT for debt amounts

### Key Distinction:
- Debt financing in M&A = `DebtInstrumentFaceAmount`
- Equity financing = `ProceedsFromIssuanceOfCommonStock`

### WRONG → RIGHT Example:
1. "closing of financing to the Parent of $36,000,000" → `DebtInstrumentFaceAmount` (NOT ProceedsFromIssuanceOfCommonStock)

---

## 12. Private Shelf Agreements and Note Purchase Agreements

### Note Purchase and Private Shelf Agreement (use `LineOfCreditFacilityMaximumBorrowingCapacity`):
- **Key indicators**: "Note Purchase and Private Shelf Agreement" or "Shelf Agreement"
- **Context**: These are credit facilities that establish a maximum borrowing capacity
- Example: "Amended and Restated Note Purchase and Private Shelf Agreement in the amount of $X" → MaximumBorrowingCapacity

### What to EXCLUDE:
- Specific debt instrument issuance amounts (use `DebtInstrumentFaceAmount`)
- General note amounts without facility language

### WRONG → RIGHT Example:
1. "Amended and Restated Note Purchase and Private Shelf Agreement in the amount of $175.0 million" → `LineOfCreditFacilityMaximumBorrowingCapacity` (NOT DebtInstrumentFaceAmount)

---

## 13. Credit Facility with Breakdown: Current vs Maximum Borrowing

### When Context Provides a Breakdown (use `LineOfCreditFacilityCurrentBorrowingCapacity`):
- **Key indicators**: "facility of $X" WITH "borrowings outstanding" or "unused capacity"
- **Pattern**: "$X [facility amount] with $Y borrowings outstanding and $Z unused borrowing capacity"
- The $X entity is the CURRENT borrowing, NOT the maximum limit
- Example: "$400.0 million secured revolving construction credit facility with $90.5 million of borrowings outstanding and $309.5 million of unused borrowing capacity"
  - Entity 400.0 is the CURRENT borrowing (the $90.5M that has been borrowed), not the maximum limit
  - This is a CurrentBorrowingCapacity situation

### How to Identify:
1. Does the sentence provide a BREAKDOWN of the facility (outstanding + unused)?
2. Is the entity amount matched with terms like "with borrowings outstanding"?
3. Does the breakdown add up to a TOTAL?

### WRONG → RIGHT Examples:
1. "$400.0 million secured revolving construction credit facility with $90.5 million of borrowings outstanding" → `LineOfCreditFacilityCurrentBorrowingCapacity` (NOT MaximumBorrowingCapacity)
   - The entity 400.0 in this context refers to what's currently borrowed
   - Maximum is not explicitly stated, only the current state

2. "increased the credit facility by $200,000, bringing the total availability to $1,150,000" → `LineOfCreditFacilityCurrentBorrowingCapacity` (NOT MaximumBorrowingCapacity)
   - "total availability" refers to current available amount, not maximum capacity

---

## 14. Tranche Facilities: When to Use DebtInstrumentFaceAmount

### Tranche A/B Loan Facilities (use `DebtInstrumentFaceAmount`):
- **Key indicators**: "Tranche A loan facility of up to $X"
- **Context**: These are specific loan instruments with committed amounts
- Tranche facilities represent specific debt instruments, not revolving capacity
- Example: "Tranche A loan revolving loan facility of up to $16.0 million" → DebtInstrumentFaceAmount

### Why NOT MaximumBorrowingCapacity:
- Tranche facilities are term loan components with fixed amounts
- Unlike revolving credit facilities, tranches don't have flexible borrowing limits
- The amount represents the committed face amount of the tranche

### WRONG → RIGHT Example:
1. "Tranche A loan revolving loan facility of up to $16.0 million" → `DebtInstrumentFaceAmount` (NOT LineOfCreditFacilityMaximumBorrowingCapacity)

---

## 15. Issue Price Percentage vs Redemption Price Percentage

### DebtInstrumentRedemptionPricePercentage Indicators:
- **Key indicators**: "sold at an issue price of X% of their face value"
- **Context**: This is the percentage price at which debt was initially sold/issued
- Example: "The Senior Notes were sold at an issue price of 99.78% of their face value" → RedemptionPricePercentage

### DebtInstrumentUnamortizedDiscount Indicators:
- **Key indicators**: "unamortized discount of $X"
- **Context**: The REMAINING unamortized portion of a discount
- Dollar amounts, NOT percentages

### CRITICAL DISTINCTION:
- Issue price expressed as a PERCENTAGE (99.78%) → `DebtInstrumentRedemptionPricePercentage`
- Unamortized discount expressed as a DOLLAR AMOUNT → `DebtInstrumentUnamortizedDiscount`
- Never use UnamortizedDiscount for percentage values

### WRONG → RIGHT Example:
1. "sold at an issue price of 99.78% of their face value" → `DebtInstrumentRedemptionPricePercentage` (NOT DebtInstrumentUnamortizedDiscount)

---

## 16. "Remaining Outstanding Debt" = LongTermDebt (NOT CarryingAmount)

### LongTermDebt Indicators for Remaining Debt:
- **Key indicators**: "remaining outstanding debt of $X"
- **Context**: Balance sheet disclosure of debt remaining after partial payoff/sale
- Example: "Company issued three notes totaling $546,440, which represented the remaining outstanding debt" → LongTermDebt

### When NOT to Use CarryingAmount:
- "Remaining outstanding debt" refers to the general balance of what debt is left
- NOT the book value including accrued interest
- NOT the carrying amount of a specific instrument

### WRONG → RIGHT Example:
1. "three notes totaling $546,440, which represented the remaining outstanding debt" → `LongTermDebt` (NOT DebtInstrumentCarryingAmount)

---

## 17. General Facility Reference vs Specific Amount

### LineOfCredit (use for general facility references):
- **Context**: Dollar amounts that represent the facility itself, not specific borrowings or capacity
- **Key indicators**: "Company had $X million of indebtedness" (when followed by separate letters of credit)
- **Pattern**: When amount is part of facility breakdown but refers to the general facility reference
- Example: "Company had $49.6 million of indebtedness and $3.8 million of letters of credit outstanding" → LineOfCredit

### When to Use LineOfCredit:
1. Amount represents "indebtedness" under a credit facility generally
2. Amount is mentioned alongside letters of credit outstanding
3. No specific "carrying amount" or "principal balance" language

### When to Use DebtInstrumentCarryingAmount:
1. Explicit "carrying amount" language
2. "Balance including principal and accrued interest"
3. Specific outstanding amount under a named facility

### WRONG → RIGHT Example:
1. "Company had $49.6 million of indebtedness and $3.8 million of letters of credit outstanding" → `LineOfCredit` (NOT DebtInstrumentCarryingAmount)

---

## 18. Facility Type Decision Chain: Revolving vs Term Loan

### THE CRITICAL DECISION POINT

When encountering "$X [type] facility", you MUST determine the facility TYPE first before selecting the tag.

### STEP-BY-STEP REASONING CHAIN

**STEP 1: Identify the facility type from the name**
- Look for these key words in the facility name:
  - **REVOLVING**: "revolving credit facility", "revolving facility", "Revolver", "revolving line of credit"
  - **TERM LOAN**: "term loan facility", "term loan", "Term Loan", "term facility"

**STEP 2: Apply the facility-type rule**

IF the facility type is **REVOLVING CREDIT**:
→ Use `LineOfCreditFacilityMaximumBorrowingCapacity`
→ Reasoning: Revolving facilities have a MAXIMUM BORROWING LIMIT, not a fixed principal

IF the facility type is **TERM LOAN**:
→ Use `DebtInstrumentFaceAmount`
→ Reasoning: Term loans are specific debt instruments with a FIXED PRINCIPAL amount

### DECISION TABLE

| Facility Name Pattern | Example | Tag |
|----------------------|---------|-----|
| "$X revolving credit facility" | "$150 million senior revolving credit facility" | LineOfCreditFacilityMaximumBorrowingCapacity |
| "$X term loan facility" | "$150 million term loan facility" | DebtInstrumentFaceAmount |
| "$X revolving line of credit" | "$20 million revolving line of credit" | LineOfCreditFacilityMaximumBorrowingCapacity |
| "term loan facility of $X" | "term loan facility of $264 million" | DebtInstrumentFaceAmount |
| "revolving credit facility of up to $X" | "revolving credit facility of up to $2.25 billion" | LineOfCreditFacilityMaximumBorrowingCapacity |

### ANTI-PATTERN (Common Error)

**WRONG REASONING**: "I see '$X facility' and the word 'facility' → MaximumBorrowingCapacity"

**THIS IS INCORRECT BECAUSE**:
- The facility TYPE matters more than the word "facility"
- Term loans are debt instruments (Face Amount)
- Revolving credits are capacity limits (MaximumBorrowingCapacity)

**CORRECT REASONING**: "I see '$X [type] facility' → What type? If 'revolving', use Maximum; if 'term loan', use FaceAmount"

### WRONG → RIGHT Examples

1. **"$150 million senior revolving credit facility"**
   - WRONG: DebtInstrumentFaceAmount
   - RIGHT: LineOfCreditFacilityMaximumBorrowingCapacity
   - Why: It's a revolving facility (capacity limit), not a term loan (principal)

2. **"$150 million term loan facility"**
   - WRONG: LineOfCreditFacilityMaximumBorrowingCapacity
   - RIGHT: DebtInstrumentFaceAmount
   - Why: It's a term loan (specific debt instrument principal)

3. **"$264 million term loan facility"**
   - WRONG: LineOfCreditFacilityMaximumBorrowingCapacity
   - RIGHT: DebtInstrumentFaceAmount
   - Why: Term loan = debt instrument principal

### COMPOUND FACILITY SENTENCES

When a sentence mentions multiple facilities:
- "a $X [Type A] facility and a $Y [Type B] facility"
- Parse EACH facility independently
- Apply the rules to each one based on its TYPE

Example: "a $150 million revolving credit facility and a $150 million term loan facility"
- First $150 (revolving) → LineOfCreditFacilityMaximumBorrowingCapacity
- Second $150 (term loan) → DebtInstrumentFaceAmount

---

## 19. "Acquired/Entered Into a $X Facility" = Maximum Borrowing Capacity

### THE PATTERN

When the context describes acquiring or entering into a facility with a dollar amount, this refers to the FACILITY LIMIT, not a general facility reference.

### KEY INDICATORS

**Action verbs that indicate facility establishment**:
- "acquired a $X facility"
- "entered into a $X facility"
- "established a $X facility"
- "implemented a $X facility"

### STEP-BY-STEP REASONING CHAIN

**STEP 1: Identify the action**
- Is there an action verb like "acquired", "entered into", "established", "implemented"?
- YES → Proceed to step 2
- NO → Use other context clues

**STEP 2: Check for dollar amount + facility**
- Does the sentence contain "$X [type] facility"?
- YES → This describes the facility SIZE/LIMIT

**STEP 3: Apply the rule**
→ Use `LineOfCreditFacilityMaximumBorrowingCapacity`
→ Reasoning: The action of acquiring/entering into a facility with an amount defines the MAXIMUM BORROWING CAPACITY

### WHEN NOT TO USE LineOfCredit

**LineOfCredit** is for:
- General facility references without specific amounts
- "no borrowings outstanding under the facility"
- Non-numeric entities

**LineOfCreditFacilityMaximumBorrowingCapacity** is for:
- "$X [type] facility" when acquiring/establishing
- "up to $X facility"
- "facility of $X" with action verbs

### WRONG → RIGHT Examples

1. **"we acquired a $45.0 million revolving credit facility"**
   - WRONG: LineOfCredit
   - RIGHT: LineOfCreditFacilityMaximumBorrowingCapacity
   - Why: "Acquired $X facility" describes the facility limit, not a general reference

2. **"we entered into a $2.25 billion unsecured revolving credit facility"**
   - WRONG: LineOfCredit
   - RIGHT: LineOfCreditFacilityMaximumBorrowingCapacity
   - Why: "Entered into $X facility" establishes the maximum borrowing capacity

3. **"the company had $45.0 million of indebtedness" (without action verb)**
   - Use: LineOfCredit (this is a general facility reference)

---

## 20. Incomplete/Truncated Context: Look for Entity Indicators

### THE CHALLENGE

Sometimes sentences are truncated or incomplete. The model must still extract the correct tag based on available context.

### KEY PRINCIPLE

**Dollar amounts in financing/agreement contexts usually indicate DEBT INSTRUMENT FACE AMOUNTS** unless other context clearly indicates otherwise.

### STEP-BY-STEP REASONING CHAIN

**STEP 1: Identify the entity type**
- Is the entity a DOLLAR AMOUNT?
- YES → Likely one of: FaceAmount, CarryingAmount, MaximumBorrowingCapacity

**STEP 2: Look for contextual indicators**

INDICATORS FOR FaceAmount:
- "Agreement" (financing agreements)
- "entered into an Agreement with [entity]"
- Financing transactions
- Dollar amounts without "outstanding", "borrowed", "fair value" language

INDICATORS FOR CarryingAmount:
- "outstanding", "borrowed", "carrying"
- "net of unamortized discount"
- "including accrued interest"

INDICATORS FOR MaximumBorrowingCapacity:
- "facility", "credit facility", "revolving"
- "up to $X", "capacity of $X"

**STEP 3: Apply elimination logic**

1. Is there "outstanding", "borrowed", "fair value", "carrying", "discount"?
   - YES → Use appropriate debt instrument tag (CarryingAmount, UnamortizedDiscount, etc.)
   - NO → Continue to step 2

2. Is there "facility", "credit facility", "revolving", "line of credit"?
   - YES → Use MaximumBorrowingCapacity
   - NO → Continue to step 3

3. Is this in a financing/agreement context?
   - YES → Use DebtInstrumentFaceAmount (most likely)
   - NO → Re-examine context for other indicators

### COMMON PATTERNS IN TRUNCATED CONTEXT

**Pattern 1: "entered into an Agreement with [Entity]"**
- Context: Financing/transaction agreement
- Entity: Dollar amount
- Default assumption: FaceAmount (debt instrument principal)
- Example: "entered into an Agreement with [Partner] for $50,000" → DebtInstrumentFaceAmount

**Pattern 2: "Acquired [Company] for $X"**
- Context: M&A transaction
- Entity: Dollar amount
- Default assumption: FaceAmount (financing amount)

### ANTI-PATTERN (Common Error)

**WRONG**: "I don't have enough context, so I'll say 'Insufficient context'"

**THIS IS INCORRECT BECAUSE**:
- Even incomplete context contains clues
- Dollar amounts in financial agreements usually indicate debt amounts
- The default for dollar amounts in financing contexts is FaceAmount

**CORRECT**: "This is a dollar amount in a financing context. The default tag for such amounts is DebtInstrumentFaceAmount unless other indicators suggest otherwise."

---

## 21. Anti-Patterns Summary: What Causes Classification Errors

### Anti-Pattern 1: Ignoring Facility Type
**PROBLEM**: Seeing "$X facility" and selecting MaximumBorrowingCapacity without checking if it's revolving or term loan.

**WRONG**: "$150 million term loan facility" → MaximumBorrowingCapacity
**RIGHT**: "$150 million term loan facility" → DebtInstrumentFaceAmount

**FIX**: Always identify facility TYPE first. Term loan = FaceAmount, Revolving = MaximumBorrowingCapacity.

### Anti-Pattern 2: "Acquired Facility" Confusion
**PROBLEM**: Treating "acquired $X facility" as general facility reference (LineOfCredit).

**WRONG**: "acquired a $45.0 million revolving credit facility" → LineOfCredit
**RIGHT**: "acquired a $45.0 million revolving credit facility" → LineOfCreditFacilityMaximumBorrowingCapacity

**FIX**: Action verbs (acquired, entered into) + $X + facility = MaximumBorrowingCapacity. LineOfCredit is only for non-numeric or "no outstanding" cases.

### Anti-Pattern 3: Giving Up on Truncated Context
**PROBLEM**: Declaring "insufficient context" when sentences are incomplete.

**WRONG**: "$50,000 Agreement with..." → "Insufficient context"
**RIGHT**: "$50,000 Agreement with..." → DebtInstrumentFaceAmount (financing context)

**FIX**: Dollar amounts in financing/agreement contexts default to FaceAmount unless other indicators are present.

### Anti-Pattern 4: Always Selecting MaximumBorrowingCapacity for "Facility"
**PROBLEM**: Word matching instead of semantic understanding.

**WRONG**: All "$X facility" → MaximumBorrowingCapacity
**RIGHT**: Check facility TYPE first, then apply appropriate tag

**FIX**:
- Revolving credit facility → MaximumBorrowingCapacity
- Term loan facility → DebtInstrumentFaceAmount
- The word "facility" alone is not sufficient - TYPE matters!
