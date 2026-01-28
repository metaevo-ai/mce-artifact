# Structural Anti-Patterns (What NOT to Do)

## Anti-Pattern 1: Abbreviating Charge Names
**Error**: Using incomplete charge names
**Prevention**: Always use complete official names
**Reminder**: "Check official name reference; don't abbreviate"

### Examples of WRONG Charge Names:
- ❌ "虚开增值税专用发票" → ✅ "虚开增值税专用发票、用于骗取出口退税、抵扣税款发票"
- ❌ "伪造国家机关证件" → ✅ "伪造、变造、买卖国家机关公文、证件、印章"
- ❌ "倒卖车票" → ✅ "倒卖车票、船票"
- ❌ "走私珍贵动物制品" → ✅ "走私珍贵动物、珍贵动物制品"
- ❌ "非法持有枪支" → ✅ "非法持有、私藏枪支、弹药"

---

## Anti-Pattern 2: Confusing 非法吸收公众存款 with 诈骗
**Error**: Treating financial schemes targeting public as ordinary 诈骗
**Prevention**: Check if the scheme targets "不特定公众" (general public)
**Reminder**: "When you see promises of returns + multiple lenders + public solicitation → 非法吸收公众存款"

### Key Distinguishing Factors:
| Factor | 非法吸收公众存款 | 诈骗 |
|--------|-----------------|------|
| Target | 不特定公众 (general public) | 特定个人 (specific individuals) |
| Method | Promise returns, recruit investors | Deception, false pretense |
| Intent | May intend to return funds | Intent to permanently deprive |
| Key Words | "承诺支付月利息", multiple lenders (13人, 7人) | "虚构...事实", "骗取" |

### Example from Training Data (id:185):
**Facts**: "以'资金周转'名义, 承诺支付月利息1%-7.5%, 骗得丁某等13人共计436.5万元"
**Correct Charge**: 非法吸收公众存款
**Why Not 诈骗**: Targets 13 different people, promises returns, typical fundraising scheme

---

## Anti-Pattern 3: Wrongly Identifying 容留他人吸毒
**Error**: Confusing personal drug use with providing location for others
**Prevention**: "容留" means providing accommodation/venue, not just participating
**Reminder**: "If defendant just used drugs WITH others → NOT 容留他人吸毒. Only if defendant provided the location → 容留他人吸毒"

### Example from Training Data (id:180):
**Facts**: "被告人陈某拿出冰毒与胡某一起吸食"
**Correct Charge**: 毒品犯罪相关 (但非容留他人吸毒)
**Error**: Model predicted "容留他人吸毒" but this was just USING drugs together, not providing venue

### Key Question:
Was the defendant PROVIDING a location/venue for OTHERS to use drugs?
- YES → 容留他人吸毒
- NO (just using together) → Not this charge

---

## Anti-Pattern 4: Missing Multiple Charges in Numbered Facts
**Error**: Ignoring numbered subsections or "捏造" patterns
**Prevention**: Numbered subsections ALWAYS indicate multiple charges to check
**Reminder**: "When you see (一)、(二)... or '捏造事实使他人受刑事拘留' → Extract EACH charge"

### Example from Training Data (id:109):
**Facts**: Multiple盗窃 acts (1-12) + "捏造王某、王某立参与盗窃使其受刑事拘留" (13)
**Correct Charges**: 盗窃;诬告陷害
**Error**: Model missed 诬告陷害 because it didn't recognize the "捏造" pattern

### Critical Patterns to Detect:
- Numbered subsections = separate charges to verify
- "捏造...使...受刑事拘留" = 诬告陷害 (separate from other charges)
- "另查明" = additional charges to add

---

## Anti-Pattern 5: Wrong Charge for Computer/Cyber Crimes
**Error**: Using 诈骗 when the act is creating phishing tools/websites
**Prevention**: Creating tools for illegal access = 提供侵入、非法控制计算机信息系统程序、工具
**Reminder**: "When defendant creates phishing websites/tools for fraud → Check computer crime charges"

### Example from Training Data (id:5):
**Facts**: "制作假最高人民检察院网站...用于实施诈骗"
**Correct Charge**: 提供侵入、非法控制计算机信息系统程序、工具
**Error**: Model predicted 诈骗, but the core act was creating illegal tools

---

## Anti-Pattern 6: Confusing 失火 with 重大责任事故
**Error**: Labeling everyday fire accidents as production safety incidents
**Prevention**: 失火 is for fires in daily life contexts (祭祖, cooking, etc.)
**Reminder**: "When fire occurs during daily activities (祭祖, 干农活) → 失火, not 重大责任事故"

### Example from Training Data (id:58):
**Facts**: "在地里干农活时, 用打火机点燃杂草引发火灾"
**Correct Charge**: 失火
**Error**: Model predicted 重大责任事故 (incorrectly applied production safety rules)

### Key Distinction:
| Context | Charge |
|---------|--------|
| Fire during daily life (祭祖, 农活, 祭祀) | 失火 |
| Fire during production/operations (违章作业) | 重大责任事故 |

---

## Anti-Pattern 7: Missing Complete Charge Names for 虚开发票
**Error**: Using abbreviated name for invoice fraud
**Prevention**: The charge name is fixed and complete
**Reminder**: "Always use '虚开增值税专用发票、用于骗取出口退税、抵扣税款发票' in full"

### Example from Training Data (id:70, 144):
**Facts**: "虚开增值税专用发票22份, 税款350,620.25元"
**Correct Charge**: 虚开增值税专用发票、用于骗取出口退税、抵扣税款发票
**Error**: Model abbreviated the charge name

---

## Anti-Pattern 8: Not Checking for 诬告陷害 in Complex Cases
**Error**: Missing 诬告陷害 when defendant fabricates accusations
**Prevention**: Look for "捏造事实" + "使他人受刑事拘留/追究"
**Reminder**: "When facts include '捏造...使...受到刑事拘留' → Add 诬告陷害"

---

## Processing Checklist (Use for Every Case)

□ Checked all numbered subsections for multiple charges
□ Looked for "捏造事实使他人受刑事拘留" (诬告陷害)
□ Verified if "容留他人吸毒" requires providing venue (not just using together)
□ Used COMPLETE official charge names (not abbreviated)
□ Distinguished 非法吸收公众存款 vs 诈骗 (public vs specific targets)
□ Distinguished 失火 vs 重大责任事故 (daily context vs production)
□ For financial crimes: identified true nature of the scheme
