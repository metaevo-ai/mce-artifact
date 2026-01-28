# Case Decomposition Framework for Chinese Criminal Law

## Core Principle: READ → DECOMPOSE → MATCH → VALIDATE

---

## Step 1: Full Case Reading (Comprehension)

Before ANY analysis, read the ENTIRE case description to understand:
- **WHO**: Who are the parties involved (defendant, victim, accomplices)?
- **WHAT**: What actions/events are described?
- **WHEN**: What is the timeline or time markers?
- **WHERE**: Where did events occur?
- **HOW**: How were actions carried out?
- **WHY**: What was the intent or consequence?

**Critical**: Look for structural markers that indicate MULTIPLE charges:
- Numbered subsections: (一)、(二)、(三)...
- "另案处理" (separate case handling)
- "另查明" (additionally discovered)
- Time markers with different periods
- Multiple victims or different methods

---

## Step 2: Act Extraction (Decomposition)

Extract ALL discrete criminal acts from the facts. An "act" is a:
- Separately described behavior with its own legal implications
- Behavior with distinct victim, method, or intent
- Behavior occurring at different time/location

### Act Extraction Rules:

1. **Numbered subsections ((一)、(二)...) ALWAYS indicate separate acts** → Each number = potentially separate charge
2. **Temporal markers (different dates, "随后", "另") indicate separate acts**
3. **Different victims/objects indicate separate acts**
4. **"另案处理", "另查明" indicate additional acts to investigate**
5. **"捏造" (fabricate) + "使他人受刑事拘留" = 诬告陷害 (separate charge)**

### Output Format:
```
Act 1: [who did what to whom - brief description]
Act 2: [brief description]
...
```

---

## Step 3: Act-to-Charge Matching (Legal Application)

For EACH extracted act, determine applicable charge:

### Matching Process:
1. **What is the criminal nature of this act?** (property, violence, position, etc.)
2. **What elements must be present for each possible charge?**
3. **Do the facts satisfy all required elements?**
4. **What is the most specific charge that fits?**

### Key Charge Distinctions (HIGH FREQUENCY ERRORS):

#### Property Crimes:
- **盗窃**: Secret taking WITHOUT victim's knowledge
- **诈骗**: Victim "willingly" transfers property due to deception
- **职务侵占**: Property already in actor's custody (position-based)
- **非法吸收公众存款**: Solicit deposits from UNSPECIFIC PUBLIC with promises of returns
- **诈骗**: Deceive SPECIFIC INDIVIDUALS to obtain property

#### Drug Crimes:
- **容留他人吸毒**: Must PROVIDE LOCATION for OTHERS to use drugs
- **持有、使用假币**: Use counterfeit currency to obtain goods/services
- **制造毒品**: Produce illegal narcotics (even small quantities)

#### Position Crimes:
- **受贿**: State official using position to accept property
- **行贿**: Give property to state official for improper benefits
- **单位行贿**: Bribery conducted in the name of/for the benefit of a unit

#### Document Crimes:
- **伪造、变造、买卖国家机关公文、证件、印章**: Must use FULL name including all elements
- **虚开增值税专用发票、用于骗取出口退税、抵扣税款发票**: Full name required

---

## Step 4: Multi-Charge Validation

After matching all acts:

### CHECKLIST:
□ Are there numbered subsections indicating multiple charges?
□ Are there "另案处理" or "另查明" patterns?
□ Are there different time periods with different act types?
□ Does "捏造事实使他人受刑事拘留" appear? (诬告陷害)
□ Does the prosecution explicitly state multiple charges?

### Multi-Charge Decision Rules:
1. Numbered subsections → EACH is a separate charge (verify against facts)
2. "捏造事实使他人受刑事拘留" → 诬告陷害 is separate from other charges
3. "另查明" → Additional discovered acts = additional charges
4. Different criminal natures (violence + property + document) = multiple charges

---

## Step 5: Charge Name Validation

### CRITICAL RULE: Use Complete Official Names

**NEVER abbreviate charge names!**

Common full names that MUST be used in full:
- 虚开增值税专用发票、用于骗取出口退税、抵扣税款发票
- 伪造、变造、买卖国家机关公文、证件、印章
- 非法持有、私藏枪支、弹药
- 非法猎捕、杀害珍贵、濒危野生动物
- 生产、销售不符合安全标准的食品
- 生产、销售假药
- 走私珍贵动物、珍贵动物制品
- 倒卖车票、船票

---

## Processing Checklist for Each Case

Before finalizing your answer, verify:

1. [ ] Extracted ALL criminal acts from numbered subsections
2. [ ] Checked for "捏造" patterns (诬告陷害)
3. [ ] Checked for "容留他人吸毒" (must provide location for OTHERS)
4. [ ] Checked for "另案处理", "另查明" patterns
5. [ ] Matched each act to charge by ELEMENTS satisfied
6. [ ] Used COMPLETE official charge names (no abbreviations)
7. [ ] For financial crimes: distinguished 非法吸收公众存款 vs 诈骗
8. [ ] For document crimes: used full official names
