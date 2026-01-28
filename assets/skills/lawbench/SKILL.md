# Skill: Structural Case Analysis with Fact-Act-Charge Mapping

## Skill Overview

This skill guides the agent to UPDATE and IMPROVE prior context through **structural case analysis** and **fact-act-charge mapping**. The core philosophy is: **analyze case structure first, apply legal reasoning second**. By teaching the model to systematically decompose case facts into discrete criminal acts before applying charge definitions, we eliminate pattern matching errors and achieve better generalization.

**Key Distinction from Previous Iterations:**

- **Iter 1-3**: Added more rules, examples, and patterns → caused overfitting through pattern memorization
- **Iter 4**: Attempted radical simplification but context remained bloated (88KB) and overfit (66%→52%)
- **Iter 5**: **Structural decomposition approach** - Teach HOW to decompose cases into acts, not WHAT charges apply to patterns

## Core Philosophy

### Why Previous Iterations Still Overfit

1. **Pattern-Based Learning Causes Memorization**: Even "simplified" rules like "if property taken secretly → 盗窃" cause overfitting because they match surface patterns rather than requiring deep analysis
2. **Context Size Correlates with Overfitting**: 88KB context in Iter 4 still correlates with 14% train-val gap
3. **Negative Learning Has Limits**: Teaching what NOT to do doesn't teach what TO do

### The Solution: Structural Decomposition

1. **Fact → Act Mapping**: Teach model to extract discrete criminal acts from narrative facts
2. **Act → Charge Matching**: Apply legal definitions to each act separately
3. **Multi-Charge by Structure**: Detect multiple charges by structure (numbered facts, temporal markers), not patterns
4. **Minimal Context**: Keep only structural guidance and charge definitions (target < 30KB)

## Available Utilities

This skill leverages utilities from `utils/`:

- **call_llm()** from `utils/llm.py`: For structured reflection on act extraction and charge matching
- **compute_embedding_similarity()** from `utils/embedding.py`: For finding similar structural patterns (use sparingly)
- **Pydantic schemas**: For structured LLM output parsing

Use LLM calls strategically for:
- Verifying act extraction completeness
- Validating charge matching decisions
- Generating structural rules from errors

## Methodology

### Phase 1: Diagnose Context Quality (Not Just Quantity)

Before updating, assess the current context's structural quality:

#### Step 1.1: Measure Structural Integrity

```
Read existing context files and assess:
1. Does context teach ACT EXTRACTION or just PATTERN MATCHING?
2. Is content organized by CASE STRUCTURE or by CHARGE TYPES?
3. Are there example-based patterns that cause memorization?
4. What's the train-val gap? (Target: < 8%)

Diagnostic Questions:
- If context teaches "when you see keyword X, predict charge Y" → PATTERN MATCHING
- If context teaches "extract acts from facts first, then match charges" → STRUCTURAL
- Is context > 50KB? → TOO BLOATED, needs radical pruning
- Is train accuracy > val accuracy + 10%? → OVERFITTING, reduce complexity
```

#### Step 1.2: Categorize Errors by Processing Stage

Load `data/train.json` and categorize each error by where in the processing pipeline it occurred:

```python
# Error categorization by processing stage
processing_stages = {
    "fact_comprehension_error": "Failed to understand what happened in the case",
    "act_extraction_error": "Failed to identify discrete criminal acts",
    "act_independence_error": "Failed to recognize acts as independent vs. dependent",
    "charge_selection_error": "Applied wrong charge to a correctly identified act",
    "charge_name_error": "Wrong or incomplete official charge name",
    "multi_charge_detection_error": "Failed to detect multiple independent charges",
    "format_error": "Output format issue"
}

# For each error, identify the stage where processing failed:
"""
Case: [案件事实]
Model Prediction: [错误预测]
Correct Answer: [正确答案]
Processing Stage Failure: [上述阶段之一]

Analysis:
- Fact Comprehension: Did model understand [key fact]?
- Act Extraction: Did model identify [criminal act]?
- Act Independence: Did model recognize [act A] and [act B] are independent?
- Charge Selection: Did model match [act] to [wrong charge] instead of [correct charge]?
"""
```

### Phase 2: Structural Decomposition Framework

Replace pattern-based charge matching with systematic case decomposition:

#### Step 2.1: Create Case Decomposition Guide

```markdown
# Case Decomposition Framework

## Core Principle: READ → DECOMPOSE → MATCH → VALIDATE

### Step 1: Full Case Reading (Comprehension)
Before ANY analysis, read the ENTIRE case description to understand:
- WHO: Who are the parties involved (defendant, victim, accomplices)?
- WHAT: What actions/events are described?
- WHEN: What is the timeline or time markers?
- WHERE: Where did events occur?
- HOW: How were actions carried out?
- WHY: What was the intent or consequence?

### Step 2: Act Extraction (Decomposition)
Extract ALL discrete criminal acts from the facts. An "act" is a:
- Separately described behavior
- Behavior with distinct victim, method, or intent
- Behavior occurring at different time/location

**Act Extraction Rules:**
1. Numbered subsections ((一)、(二)...) → Separate acts
2. Temporal markers (different dates, "随后", "另") → Separate acts
3. Different victims/objects → Separate acts
4. Different methods (stealing vs. violence) → Separate acts
5. "另案处理", "另查明" → Additional acts mentioned

**Output**: List of acts in format:
```
Act 1: [brief description - who did what to whom]
Act 2: [brief description]
...
```

### Step 3: Act-to-Charge Matching (Legal Application)
For EACH extracted act, determine applicable charge:

**Matching Process:**
1. What is the criminal nature of this act? (property, violence, position, etc.)
2. What elements must be present for each possible charge?
3. Do the facts satisfy all required elements?
4. What is the most specific charge that fits?

**Charge Matching Checklist:**
□ Identify the act's criminal category
□ List all potentially applicable charges
□ Verify elements are satisfied
□ Select the most specific charge
□ Check for special identity requirements

### Step 4: Multi-Charge Validation
After matching all acts:
- Are there multiple acts with different charges?
- Are any charges potentially absorbed (continuing offense)?
- Is there an "另案处理" pattern we missed?
- Do the numbered facts indicate multiple charges?

### Step 5: Charge Name Validation
- Does each charge name match official reference?
- Are we using complete official names?
- No abbreviations or partial names
```

#### Step 2.2: Create Structural Markers Reference

```markdown
# Structural Markers for Multi-Charge Detection

## Always Check for Multiple Charges When You See:

### 1. Structural Markers (HIGH CONFIDENCE → Multiple Charges)

| Marker | Example | Interpretation |
|--------|---------|----------------|
| Numbered facts | (一)、(二)、(三) | Each numbered item = separate act |
| "另案处理" | 郭×1（另案处理） | Accomplice's acts → separate cases |
| "另查明" | 另查明... | Additional discovered acts |
| "判决宣告前" | 判决宣告前还有其他罪 | Pre-existing charges |
| "经审理查明" + numbers | 经审理查明：1...2...3... | Multiple distinct facts |

### 2. Temporal Markers (MEDIUM CONFIDENCE → Check Act Independence)

| Marker | Example | Action |
|--------|---------|--------|
| Different dates | 2013年...2014年... | Check if different acts |
| "后" / "随后" | 盗窃后... | Check if separate act |
| "同日" | 同日... | Check if concurrent acts |
| "期间" | 2013年至2015年期间 | Check for multiple acts |

### 3. Actor Markers (MEDIUM CONFIDENCE → Check Multiple Roles)

| Marker | Example | Action |
|--------|---------|--------|
| Multiple defendants | 被告人A与被告人B | Check each role |
| Accomplice notes | "小某（身份不详）" | Check accomplice actions |
| "伙同" | 伙同他人 | Check scope of joint acts |

## Multi-Charge Decision Tree

START: Analyze case structure
├── Are there numbered subsections ((一)、(二)...)?
│   ├── YES → Each number = separate charge
│   └── NO → Continue
├── Are there "另案处理" or "另查明" patterns?
│   ├── YES → Additional charges exist, find them
│   └── NO → Continue
├── Are there different time periods?
│   ├── YES → Check if acts are independent
│   └── NO → Continue
└── Are there different victim groups?
    ├── YES → Check if acts are independent
    └── NO → Consider single charge
```

### Phase 3: Fact-Act-Charge Mapping Examples

Create minimal but structural examples (NOT pattern-based):

```markdown
# Structural Case Analysis Examples

## Example 1: Structural Decomposition of Numbered Facts
**Case ID**: [from training data]
**Facts**: "公诉机关指控：（一）2013年8月，被告人使用暴力殴打被害人致轻伤；（二）同年9月，被告人携带管制刀具在某公共场所出现"

### Correct Decomposition:
1. **Act 1**: Violence causing injury → Extract: "使用暴力殴打被害人致轻伤"
2. **Act 2**: Illegal weapons possession → Extract: "携带管制刀具在公共场所出现"

### Correct Matching:
- Act 1 → 故意伤害
- Act 2 → 非法携带枪支、弹药、管制刀具、危险物品危及公共安全

### Key Lesson:
**Numbered subsections ((一)、(二)) ALWAYS indicate separate charges.** Don't merge them.

---

## Example 2: "另案处理" Pattern
**Case ID**: [from training data]
**Facts**: "郭×1（另案处理）与被告人共同实施犯罪，被告人另在某日盗窃财物"

### Correct Decomposition:
1. **Act 1**: Accomplice's acts (not our defendant) → Exclude from this case
2. **Act 2**: Defendant's theft → Extract: "盗窃财物"

### Correct Matching:
- Focus on Act 2 only → 盗窃

### Key Lesson:
**"另案处理" means the accomplice's actions are in a separate case. Focus on THIS defendant's acts, but scan for additional acts by THIS defendant.**

---

## Example 3: Sequential vs. Independent Acts
**Facts**: "被告人多次用手摸或用生殖器碰触刘某某的阴部"

### Correct Decomposition:
- **Single Act**: Multiple touches of same nature = one continuing act → Extract: "多次猥亵行为"

### Correct Matching:
- Act 1 → 猥亵儿童

### Key Lesson:
**Sequential similar acts are ONE charge. Multiple charges require DIFFERENT act types.**

---

## Example 4: Temporal Marker with Different Acts
**Facts**: "2013年被告人逃税；2014年被告人虚开发票"

### Correct Decomposition:
1. **Act 1**: Tax evasion → Extract: "逃避纳税义务"
2. **Act 2**: Invoice fraud → Extract: "虚开增值税专用发票"

### Correct Matching:
- Act 1 → 逃税
- Act 2 → 虚开增值税专用发票、用于骗取出口退税、抵扣税款发票

### Key Lesson:
**Different time periods with different act types = Multiple charges.**
```

### Phase 4: Minimal Charge Definitions with Element Focus

Replace detailed definitions with element-focused, structural definitions:

```markdown
# Charge Definitions (Element-Focused)

## Property Crimes

### 盗窃
- **Elements**: (1) Secret taking, (2) Without victim's knowledge, (3) Intent to permanently deprive
- **Key Question**: Was the victim unaware of the taking?
- **Common Confusion**: NOT deception (诈骗), NOT position-based (职务侵占)

### 诈骗
- **Elements**: (1) Deception, (2) Victim voluntarily transfers property, (3) Intent to deprive
- **Key Question**: Did victim voluntarily transfer property due to being deceived?
- **Common Confusion**: NOT secret taking (盗窃)

### 职务侵占
- **Elements**: (1) Actor in position of trust, (2) Property in actor's custody, (3) Intent to permanently deprive
- **Key Question**: Was the actor already entrusted with the property?
- **Common Confusion**: NOT theft (盗窃 - no position), NOT temporary use (挪用资金)

## Violence Crimes

### 故意伤害
- **Elements**: (1) Intentional harm, (2) Specific victim, (3) Injury result
- **Key Question**: Was the victim specifically targeted with intent to harm?
- **Common Confusion**: NOT random target (寻衅滋事)

### 寻衅滋事
- **Elements**: (1) Random/trivial provocation, (2) Disturbing public order, (3) Random victim
- **Key Question**: Was the victim random and provocation trivial?
- **Common Confusion**: NOT specific target (故意伤害)

### 聚众斗殴
- **Elements**: (1) Gathering crowd, (2) Mutual fighting
- **Key Question**: Was it mutual combat between groups?
- **Common Confusion**: NOT attack on victim (故意伤害)

## Position Crimes

### 受贿
- **Elements**: (1) State official, (2) Using position, (3) Accepting property
- **Key Question**: Is the actor a state official using their position?
- **Common Confusion**: NOT non-state official (非国家工作人员受贿)

### 非国家工作人员受贿
- **Elements**: (1) Non-state personnel, (2) Using position, (3) Accepting property
- **Key Question**: Is the actor a non-state personnel using their position?
- **Common Confusion**: NOT state official (受贿)

## Document Crimes

### 伪造、变造、买卖国家机关公文、证件、印章
- **Elements**: (1) Falsifying/making/selling, (2) Government documents/seals
- **Key Question**: Was government documentation falsified or traded?
- **Full Name Required**: Don't abbreviate
```

### Phase 5: Error-Driven Structural Refinement

Update context based on structural errors:

#### Step 5.1: Extract Structural Error Patterns

For each error in `data/train.json`, identify the structural failure:

```markdown
## Structural Error Entry: [Case ID]

### Error Analysis
- **Model Prediction**: [Wrong prediction]
- **Correct Answer**: [Correct charges]
- **Structural Failure**: [Which phase failed: Fact/Act/Match/Validate]

### Structural Breakdown of Error

**Facts**: [Key facts that should trigger correct decomposition]

**Correct Structure Analysis**:
1. Acts to extract:
   - Act 1: [What should have been extracted]
   - Act 2: [What should have been extracted]

2. Correct matching:
   - Act 1 → [Correct charge]
   - Act 2 → [Correct charge]

### Why Model Failed
[Explain the structural misunderstanding]

### Structural Prevention Rule
[Create a rule that prevents this structural error]
```

#### Step 5.2: Create Structural Anti-Patterns

```markdown
# Structural Anti-Patterns (What NOT to Do)

## Anti-Pattern 1: Merging Numbered Facts
**Error**: Treating (一)、(二) as one act
**Prevention**: Numbered subsections ALWAYS = separate charges
**Reminder**: "When you see (一)...(二)..., extract two separate acts"

## Anti-Pattern 2: Ignoring "另案处理"
**Error**: Missing additional charges after "另案处理" mentions
**Prevention**: "另案处理" mentions indicate other crimes exist
**Reminder**: "Accomplices may be '另案处理', but scan for THIS defendant's other acts"

## Anti-Pattern 3: Confusing Sequential Similar Acts
**Error**: Treating sequential similar acts as multiple charges
**Prevention**: Same act type repeatedly = ONE charge
**Reminder**: "Multiple similar acts = continuing offense, not multiple charges"

## Anti-Pattern 4: Wrong Charge Family
**Error**: Predicting wrong charge type for identified act
**Prevention**: Verify elements match before selecting charge
**Reminder**: "Don't match by keyword; verify all elements are satisfied"

## Anti-Pattern 5: Incomplete Charge Names
**Error**: Using abbreviated charge names
**Prevention**: Always use complete official names
**Reminder**: "Check official name reference; don't abbreviate"
```

### Phase 6: Simplified Retrieval Function

Update `retrieve_context.py` with structural retrieval logic:

```python
def retrieve_context(question: str) -> dict:
    """
    Retrieve structural guidance for legal charge prediction.
    Focus on case decomposition, not pattern matching.
    """
    # 1. Detect structural markers for multi-charge
    structural_markers = detect_structural_markers(question)

    # 2. Get act extraction guidance
    act_extraction_guide = get_act_extraction_guide()

    # 3. Get charge definitions with elements
    charge_definitions = get_charge_definitions()

    # 4. Get structural anti-patterns
    structural_anti_patterns = get_structural_anti_patterns()

    # 5. Get charge name reference
    charge_names = get_charge_name_reference()

    return {
        'structural_markers': structural_markers,
        'act_extraction_guide': act_extraction_guide,
        'charge_definitions': charge_definitions,
        'structural_anti_patterns': structural_anti_patterns,
        'charge_names': charge_names,
        'processing_checklist': [
            'Extracted ALL criminal acts?',
            'Checked numbered subsections ((一)、(二))?',
            'Checked "另案处理", "另查明" patterns?',
            'Matched each act to charge by elements?',
            'Used complete official charge names?'
        ]
    }
```

**Implementation Principles:**
- Keep retrieval focused on structural guidance
- Don't add pattern-based triggers
- Include processing checklist for each case
- Focus on verification, not matching

### Phase 7: Context File Structure (Structural Organization)

Organize context into minimal, structural files:

#### File 1: case_decomposition_guide.md (Max 8KB)
```markdown
# Case Decomposition Framework

## Process: READ → DECOMPOSE → MATCH → VALIDATE

### Step 1: Full Reading
Extract: who, what, when, where, how, why

### Step 2: Act Extraction
Rules:
- Numbered subsections = separate acts
- Different time periods = check independence
- Different victims = check independence
- Different methods = separate acts
- "另案处理" = additional acts

### Step 3: Charge Matching
For each act:
1. Identify criminal nature
2. List possible charges
3. Verify elements
4. Select most specific

### Step 4: Multi-Charge Validation
- Independent acts = multiple charges
- Same act type = one charge
- Check absorption rules
```

#### File 2: structural_markers_reference.md (Max 5KB)
```markdown
# Structural Markers for Multi-Charge Detection

## High-Confidence Multi-Charge Markers

| Marker | Meaning | Action |
|--------|---------|--------|
| (一)、(二)... | Numbered facts | Each = separate charge |
| 另案处理 | Separate case | Find THIS defendant's acts |
| 另查明 | Additional found | Include in charges |
| 判决宣告前 | Pre-existing | Add to charges |

## Temporal Markers
| Marker | Action |
|--------|--------|
| Different years | Check independence |
| "后"/"随后" | Check if separate act |
```

#### File 3: charge_definitions_element_focused.md (Max 10KB)
```markdown
# Charge Definitions (Element-Focused)

## Property Crimes
### 盗窃
- Elements: Secret taking + unaware victim + intent to deprive
- Key: Victim unaware

### 诈骗
- Elements: Deception + voluntary transfer + intent to deprive
- Key: Victim "willing"

[Continue for other charges]
```

#### File 4: structural_anti_patterns.md (Max 5KB)
```markdown
# Structural Anti-Patterns

## What NOT to Do
1. Don't merge numbered facts
2. Don't ignore "另案处理" patterns
3. Don't split sequential similar acts
4. Don't match charges by keyword
5. Don't abbreviate charge names

## Processing Checklist
□ Extracted all acts?
□ Checked structural markers?
□ Verified charge elements?
□ Used complete names?
```

#### File 5: charge_name_reference.md (Max 2KB)
```markdown
# Official Charge Name Reference

## Complete Names Required
[High-frequency charges with full names]

## Validation Rule
Always use complete official name from reference
```

**Total Target Size: < 30KB** (vs. Iter 4's 88KB)

### Phase 8: Update Strategy (Structural Refinement)

#### Update Priority (highest first):
1. **RESTRUCTURE** context around case decomposition process
2. **PRUNE** all pattern-based rules and keywords
3. **KEEP** only element-focused charge definitions
4. **ADD** structural markers for multi-charge detection
5. **INCLUDE** minimal examples demonstrating structure
6. **ENSURE** processing checklist is included

#### Don't Add:
- Keyword-based triggers
- Scenario descriptions
- Complex combination rules
- Large example libraries

#### Do Add:
- Act extraction rules
- Structural markers
- Element verification checklists
- Anti-pattern reminders

## Key Principles

1. **Structure Over Patterns**: Decompose cases first, match charges second
2. **Act-Based Reasoning**: Identify discrete criminal acts, not charge patterns
3. **Minimal Context**: Smaller context with structural guidance beats large pattern libraries
4. **Element Verification**: Match by elements satisfied, not keywords matched
5. **Process Checklist**: Include verification checklist for each case
6. **Structural Markers**: Use numbered facts, "另案处理" as multi-charge indicators
7. **Precision Names**: Always use complete official charge names

## Output

This skill produces structurally-organized context files:

- `context/case_decomposition_guide.md`: Act extraction and matching framework
- `context/structural_markers_reference.md`: Multi-charge detection markers
- `context/charge_definitions_element_focused.md`: Element-based charge definitions
- `context/structural_anti_patterns.md`: What NOT to do (processing errors)
- `context/charge_name_reference.md`: Official charge name validation
- `context/retrieve_context.py`: Structural retrieval function

**Target: < 30KB total context** (vs. Iter 4's 88KB)

The structurally-organized context should enable the base model to:

1. Decompose cases into discrete criminal acts
2. Detect multiple charges through structural markers
3. Match charges by element verification, not pattern matching
4. Apply consistent processing to all cases
5. Output charges in correct format: [罪名]charge1;charge2<eoa>
