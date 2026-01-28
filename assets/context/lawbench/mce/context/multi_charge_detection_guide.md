# Multi-Charge Detection Guide

## Key Principle: Structural Markers Always Indicate Multiple Charges

### High-Confidence Multi-Charge Markers

| Marker | Example | Action |
|--------|---------|--------|
| Numbered facts | (一)、(二)、(三) | EACH number = separate charge to verify |
| "捏造事实使...受刑事拘留" | 捏造盗窃事实使他人受刑拘 | 诬告陷害 = separate charge |
| "另案处理" | 郭×1（另案处理） | Accomplice separate, but scan THIS defendant's other acts |
| "另查明" | 另查明... | Additional discovered acts = add charges |
| "判决宣告前" | 判决宣告前还有其他罪 | Pre-existing charges to include |

---

## Common Multi-Charge Patterns

### Pattern 1: Numbered Subsections (一)、(二)...

**Rule**: Each numbered item = separate charge to verify

**Example** (id:109):
```
（一）多次入室盗窃
...
（十三）捏造事实使王某、王某立受刑事拘留
```
**Correct Analysis**:
- Act 1: 盗窃 (multiple incidents)
- Act 2: 诬告陷害 (fabricating accusations)
**Charges**: 盗窃;诬告陷害

**Common Error**: Only identifying 盗窃, missing 诬告陷害

---

### Pattern 2: "捏造事实使他人受刑事拘留"

**Rule**: "捏造" + "受刑事拘留/追究" = 诬告陷害 (separate charge)

**Example** (id:109):
```
被告人捏造王某、王某立参与盗窃的事实，使二人受到刑事拘留
```
**Charge**: 诬告陷害

**Key Trigger Words**:
- 捏造 (fabricate, make up)
- 使...受刑事拘留 (cause to be criminally detained)
- 使...受到刑事追究 (cause to be prosecuted)

---

### Pattern 3: "另查明" (Additionally Discovered)

**Rule**: Additional facts discovered during investigation = additional charges

**Example** (id:112):
```
一、盗窃电缆线三次...
二、非法处置扣押的财产...
```
**Charges**: 盗窃;非法处置查封、扣押、冻结的财产

---

### Pattern 4: Unit Crime + Individual Crime

**Rule**: Unit (单位) charge + individual's additional crime = multiple charges

**Example** (id:106):
```
一、单位受贿事实...
二、危险驾驶事实...
```
**Charges**: 单位受贿;危险驾驶

---

## Temporal Markers (Medium Confidence)

| Marker | Example | Action |
|--------|---------|--------|
| Different years | 2012年...2014年... | Check if different acts |
| "后" / "随后" | 盗窃后... | Check if separate act |
| "另" | 另查明... | Additional act |
| "期间" | 2013年至2015年期间 | Check for multiple acts |

---

## Actor Markers (Check Multiple Roles)

| Marker | Example | Action |
|--------|---------|--------|
| Multiple defendants | 被告人A与被告人B | Check each role |
| "伙同" | 伙同他人 | Check scope of joint acts |
| "另案处理" | 张某（另案处理） | Accomplice's acts separate |

---

## Multi-Charge Decision Tree

```
START: Analyze case structure
├── Are there numbered subsections ((一)、(二)...)?
│   ├── YES → Extract EACH numbered item as separate charge
│   └── NO → Continue
├── Is there "捏造事实使...受刑事拘留"?
│   ├── YES → Add 诬告陷害 to charges
│   └── NO → Continue
├── Is there "另查明" or "另案处理"?
│   ├── YES → Add discovered acts as charges
│   └── NO → Continue
├── Are there different time periods?
│   ├── YES → Check if acts are independent (different nature)
│   └── NO → Continue
└── Are there different victim groups or act types?
    ├── YES → May indicate multiple charges
    └── NO → Consider single charge
```

---

## Charges That Commonly Co-occur

| Charge Combination | Common Scenario |
|-------------------|-----------------|
| 盗窃;诬告陷害 | Theft + fabricating accusations against others |
| 单位受贿;危险驾驶 | Unit bribery + individual DUI |
| 逃税;虚开增值税专用发票 | Tax evasion + invoice fraud |
| 故意伤害;故意毁坏财物 | Violence + property damage |
| 持有、使用假币;盗窃 | Counterfeit use + theft |
| 非法持有、私藏枪支、弹药;容留他人吸毒 | Weapons possession + providing venue for drug use |

---

## Processing Checklist for Multi-Charge Detection

□ Extracted all numbered subsections
□ Looked for "捏造事实使...受刑事拘留"
□ Checked for "另查明" patterns
□ Verified unit crime + individual crime combinations
□ Considered temporal independence of acts
□ Did NOT merge numbered facts (each number = separate charge)
□ Did NOT split sequential similar acts (same type = one charge)
