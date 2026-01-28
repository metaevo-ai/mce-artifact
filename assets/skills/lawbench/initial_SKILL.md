## Skill Overview

This skill guides the agent to learn task-specific context for Chinese criminal charge prediction by systematically analyzing training examples, extracting legal knowledge patterns, and building a structured understanding of crime classifications and their defining elements.

## Methodology

### Phase 1: Load and Analyze Training Data

1. **Read training dataset**: Load `data/train.json` (contains: summary + detailed_results with id, question, llm_answer, target, is_correct)
2. **Identify charge vocabulary**: Extract all unique charges from `target` field to understand the scope of charges in this task
3. **Group examples by charge type**: Create a mapping of charges → list of cases with that charge

### Phase 2: Extract Crime Element Patterns

For each charge type identified, analyze the corresponding training examples to extract:

1. **Criminal action patterns**: What specific actions constitute this crime?
   - Examples: "秘密窃取" (secret taking) for 盗窃, "虚构事实" (fabricating facts) for 诈骗

2. **Victim/object patterns**: Who or what is harmed?
   - Examples: "他人财物" for property crimes, "国家机关公务" for 妨害公务

3. **Method patterns**: How is the crime committed?
   - Examples: "暴力威胁" for 抢劫, "醉酒驾驶" for 危险驾驶

4. **Threshold patterns**: What numerical or severity thresholds apply?
   - Amount thresholds, injury levels, repetition counts, etc.

5. **Intent patterns**: What mental state is required?
   - "以非法占有为目的" (intent of illegal possession), "明知故犯" (knowing violation)

### Phase 3: Build Distinction Knowledge

For similar/related charges, identify distinguishing features:

**Example distinctions to extract:**
- **盗窃 vs 诈骗**: 盗窃 is secret taking, 诈骗 is deception-induced voluntary transfer
- **职务侵占 vs 盗窃**: 职务侵占 involves misappropriation of property already in one's possession due to position
- **故意伤害 vs 寻衅滋事**: 故意伤害 targets specific individuals, 寻衅滋事 targets random victims
- **危险驾驶 vs 以危险方法危害公共安全**: 危险驾驶 is specifically drunk/drugged driving, the other is broader
- **行贿 vs 对非国家工作人员行贿**: Target of bribery (state official vs non-state personnel)

### Phase 4: Create Structured Context Files

Organize extracted knowledge into `context/` directory:

**File 1: charge_definitions.md**
```markdown
# 罪名定义与构成要件

## 财产类犯罪
### 盗窃
- 定义: 以非法占有为目的，秘密窃取公私财物
- 构成要件:
  1. 非法占有目的
  2. 秘密窃取行为
  3. 公私财物为对象
  4. 数额/情节达到立案标准
- 关键事实模式: "乘人不备"、"秘密窃取"、"盗走"

### 诈骗
- 定义: 以非法占有为目的，虚构事实或隐瞒真相，骗取数额较大财物
- 构成要件:
  1. 非法占有目的
  2. 虚构事实或隐瞒真相
  3. 被害人产生错误认识
  4. 被害人基于错误认识处分财产
  5. 数额较大
- 关键事实模式: "虚构"、"欺骗"、"信以为真"

### 职务侵占
- 定义: 公司、企业或其他单位的人员，利用职务上的便利，侵占本单位财物
- 构成要件:
  1. 主体: 公司/企业/单位人员
  2. 利用职务便利
  3. 侵占本单位财物
  4. 数额较大
- 关键事实模式: "利用职务便利"、"侵占"、"挪用"
```

**File 2: charge_distinctions.md**
```markdown
# 罪名区分要点

## 盗窃类
| 罪名 | 核心特征 | 区分要点 |
|------|---------|---------|
| 盗窃 | 秘密窃取 | 被害人不知情 |
| 诈骗 | 欺骗获取 | 被害人"自愿"交出 |
| 抢夺 | 公然夺取 | 趁人不备但公开进行 |
| 抢劫 | 暴力威胁 | 使用暴力或威胁 |

## 暴力犯罪
| 罪名 | 攻击对象 | 伤害程度 | 动机特征 |
|------|---------|---------|---------|
| 故意伤害 | 特定对象 | 轻伤以上 | 报复/冲突 |
| 寻衅滋事 | 不特定对象 | 轻微伤为主 | 无事生非 |
| 聚众斗殴 | 聚众互殴 | 视情况 | 争霸/报复 |

## 职务犯罪
| 罪名 | 主体 | 客体 | 手段 |
|------|------|------|------|
| 职务侵占 | 企业人员 | 本单位财物 | 侵占/挪用 |
| 挪用资金 | 企业人员 | 本单位资金 | 挪用 |
| 受贿 | 国家工作人员 | 职务廉洁性 | 收受财物 |
| 贪污 | 国家工作人员 | 公共财物 | 侵吞/骗取 |
```

**File 3: multi_charge_patterns.md**
```markdown
# 数罪并罚案例模式

## 常见多罪名组合

### 1. 暴力+其他犯罪
- 故意伤害 + 妨害公务: 伤害执法人员
- 寻衅滋事 + 非法携带枪支: 滋事时携带武器

### 2. 财产+其他犯罪
- 盗窃 + 持有、使用假币: 使用假币作案
- 诈骗 + 伪造证件: 伪造材料诈骗

### 3. 职务犯罪组合
- 受贿 + 滥用职权: 利用职权收受贿赂并滥用
- 行贿 + 对非国家工作人员行贿: 多向行贿

## 判断多个罪名的标准
1. 行为独立性: 两个以上独立的行为
2. 罪名独立性: 每个行为符合独立的犯罪构成
3. 排除牵连: 不构成牵连犯或吸收犯
4. 数罪并罚: 依法合并处罚
```

### Phase 5: Refine with Error Analysis

1. Review `detailed_results` for incorrect predictions
2. Identify patterns in errors:
   - **Similar charge confusion**: Confused similar charges (e.g., 盗窃 vs 诈骗)
   - **Missing charges**: Failed to identify multiple applicable charges
   - **Wrong charge selection**: Selected wrong charge for the facts
3. Update context with additional distinctions based on errors

### Phase 6: Create Retrieval Function

Write `retrieve_context.py` with function:
```python
def retrieve_context(question: str) -> dict:
    """
    Retrieve relevant context for a given case description.
    Returns:
        dict with keys:
        - 'relevant_charges': list of potentially applicable charges
        - 'definitions': charge definitions with elements
        - 'distinctions': how to distinguish from similar charges
        - 'patterns': key fact patterns to look for
    """
```

**Implementation approach:**
- Use keyword matching on fact patterns to identify potential charges
- Retrieve relevant definitions and distinctions
- Include multi-charge detection logic

## Key Principles

1. **Build incrementally**: Start with most common charges, expand based on training data
2. **Pattern-based learning**: Extract recurring fact patterns that indicate specific charges
3. **Distinction-focused**: Emphasize learning how to differentiate similar charges
4. **Legal accuracy**: Ensure patterns align with Chinese criminal law (《中华人民共和国刑法》)
5. **Practical application**: Focus on facts that distinguish charges in real cases

## Output

This skill produces:
- `context/charge_definitions.md`: Charge definitions and elements
- `context/charge_distinctions.md`: How to distinguish similar charges
- `context/multi_charge_patterns.md`: Multi-charge case patterns
- `context/retrieval_guide.md`: How to apply context to new cases
- `retrieve_context.py`: Context retrieval function

The context should enable the base model to:
1. Identify potential charges from case facts
2. Distinguish between similar charges
3. Detect when multiple charges apply
4. Output charges in the required format: [罪名]charge1;charge2<eoa>
