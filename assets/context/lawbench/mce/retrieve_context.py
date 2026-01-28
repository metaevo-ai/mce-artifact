from pathlib import Path

def retrieval_function(question: str) -> str:
    """
    Retrieve relevant context for the given case description.
    Uses structural case decomposition to identify charges accurately.
    """
    script_dir = Path(__file__).parent.resolve()
    context_dir = script_dir / "context"

    # Load all context files
    decomposition_guide = ""
    charge_definitions = ""
    anti_patterns = ""
    charge_names = ""
    multi_charge_guide = ""
    error_case_analysis = ""

    decomposition_file = context_dir / "case_decomposition_guide.md"
    definitions_file = context_dir / "charge_definitions_element_focused.md"
    anti_patterns_file = context_dir / "structural_anti_patterns.md"
    names_file = context_dir / "charge_name_reference.md"
    multi_charge_file = context_dir / "multi_charge_detection_guide.md"
    error_case_file = context_dir / "error_case_analysis.md"

    if decomposition_file.exists():
        decomposition_guide = decomposition_file.read_text()
    if definitions_file.exists():
        charge_definitions = definitions_file.read_text()
    if anti_patterns_file.exists():
        anti_patterns = anti_patterns_file.read_text()
    if names_file.exists():
        charge_names = names_file.read_text()
    if multi_charge_file.exists():
        multi_charge_guide = multi_charge_file.read_text()
    if error_case_file.exists():
        error_case_analysis = error_case_file.read_text()

    # Extract key terms from the question
    question_lower = question.lower()

    # Build relevant context based on detected patterns
    relevant_context = []

    # Section 1: Format rules (always include)
    format_section = """## CRITICAL OUTPUT FORMAT RULES

**Output Format**: [罪名]charge1;charge2<eoa>
- Do NOT add "罪" after charge names
- Use semicolon (;) to separate multiple charges
- Use COMPLETE official charge names (see reference below)

**CRITICAL CHARGE NAME RULE**:
When in doubt about a charge name, check charge_name_reference.md for the complete official name.
NEVER abbreviate charge names like:
- "虚开增值税专用发票" → MUST be "虚开增值税专用发票、用于骗取出口退税、抵扣税款发票"
- "倒卖车票" → MUST be "倒卖车票、船票"
- "伪造证件" → MUST be "伪造、变造、买卖国家机关公文、证件、印章"
- "走私珍贵动物制品" → MUST be "走私珍贵动物、珍贵动物制品"
"""
    relevant_context.append(format_section)

    # Section 2: Multi-charge detection triggers
    multi_charge_triggers = [
        ("（一）", "Numbered subsection found - EACH number may indicate separate charge"),
        ("（二）", "Numbered subsection found - EACH number may indicate separate charge"),
        ("捏造", "Fabrication detected - may indicate 诬告陷害"),
        ("受刑事拘留", "Fabrication causing criminal detention - may indicate 诬告陷害"),
        ("另案处理", "Separate case handling - check THIS defendant's other acts"),
        ("另查明", "Additional discovery - may indicate additional charges"),
        ("数罪并罚", "Mentions multiple charges - verify all charges are identified"),
        ("判决宣告前", "Pre-existing charges mentioned - may indicate multiple charges"),
        ("单位", "Unit crime mentioned - may combine with individual crimes"),
    ]

    for trigger, guidance in multi_charge_triggers:
        if trigger in question:
            relevant_context.append(f"\n### Multi-Charge Detection: {trigger}\n{guidance}")

    # Section 3: High-error charge patterns (from training data analysis)
    high_error_patterns = {
        "非法吸收公众存款": "CRITICAL: Check if targets '不特定公众' (general public) with return promises → 非法吸收公众存款 vs 诈骗 (诈骗 targets specific individuals)",
        "诈骗": "Check if truly 诈骗 or 非法吸收公众存款 (public fundraising scheme)",
        "容留他人吸毒": "MUST provide LOCATION for OTHERS to use drugs - not just using together",
        "制造毒品": "Even small-scale production = 制造毒品 (full name)",
        "持有、使用假币": "Using counterfeit currency to buy things = 持有、使用假币",
        "捏造事实": "Fabricating accusations causing detention = 诬告陷害 (separate charge!)",
        "失火": "Fire during daily activities (祭祖, 农活) = 失火 (not 重大责任事故)",
        "重大责任事故": "Only for production/operations violations - NOT for daily life fires",
        "提供侵入": "Creating phishing/illegal tools = 提供侵入、非法控制计算机信息系统程序、工具",
        "诬告陷害": "Fabricating crime facts to implicate others = 诬告陷害 (separate charge)",
        "窝藏、包庇": "Helping criminals escape = 窝藏、包庇; may combine with 包庇毒品犯罪分子",
        "虐待被监管人": "Prison staff abusing inmates = 虐待被监管人",
    }

    for keyword, guidance in high_error_patterns.items():
        if keyword in question:
            relevant_context.append(f"\n**{keyword} Guidance**: {guidance}")

    # Section 4: Complete charge name warnings
    charge_name_warnings = {
        "虚开": "Must use: 虚开增值税专用发票、用于骗取出口退税、抵扣税款发票",
        "增值税": "If invoice fraud → use full name above",
        "倒卖车票": "Must be: 倒卖车票、船票",
        "假药": "Must be: 生产、销售假药",
        "珍贵动物": "Must be: 走私珍贵动物、珍贵动物制品 or 非法猎捕、杀害珍贵、濒危野生动物",
        "枪支": "Must be: 非法持有、私藏枪支、弹药",
        "伪造国家机关": "Must be: 伪造、变造、买卖国家机关公文、证件、印章",
        "不符合安全标准": "Must be: 生产、销售不符合安全标准的食品",
        "假币": "If using counterfeit money → 持有、使用假币",
    }

    for keyword, warning in charge_name_warnings.items():
        if keyword in question:
            relevant_context.append(f"\n**Charge Name Check**: {warning}")

    # Section 5: Add core processing framework
    framework_section = """## CORE PROCESSING FRAMEWORK (Apply to every case)

### Step 1: Extract ALL Acts
- Look for numbered subsections ((一)、(二)...)
- Look for "捏造事实使...受刑事拘留" → 诬告陷害
- Look for "另查明" → additional acts
- Numbered items = potentially separate charges

### Step 2: Match Each Act to Charge by Elements
For EACH extracted act:
1. What elements are required?
2. Does this act satisfy all elements?
3. Use complete official charge name

### Step 3: Validate Charge Names
- Check charge_name_reference.md for complete names
- NEVER abbreviate fixed charge names

### Step 4: Verify Multi-Charge
- Did you identify ALL numbered acts?
- Did you check for 诬告陷害 (fabrication)?
- Did you check for separate unit + individual crimes?
"""
    relevant_context.append(framework_section)

    # Section 6: Add reference materials
    relevant_context.append("\n" + decomposition_guide)
    relevant_context.append("\n" + charge_definitions)
    relevant_context.append("\n" + anti_patterns)
    relevant_context.append("\n" + charge_names)
    relevant_context.append("\n" + multi_charge_guide)

    # Section 7: Add error case analysis if relevant keywords detected
    error_case_keywords = {
        "检疫": "动植物检疫徇私舞弊",
        "虚假单据": "动植物检疫徇私舞弊",
        "好处费": "行贿;单位行贿",
        "行贿": "行贿;单位行贿",
        "传销": "组织、领导传销活动;非法吸收公众存款",
        "发展下线": "组织、领导传销活动",
        "推荐奖": "组织、领导传销活动",
        "假冒注册商标": "假冒注册商标;生产、销售伪劣产品",
        "伪造存单": "金融凭证诈骗",
        "农某甲": "金融凭证诈骗",
        "客户经理": "协助组织卖淫",
        "招揽嫖客": "协助组织卖淫",
        "散发名片": "协助组织卖淫",
    }

    for keyword, related_charge in error_case_keywords.items():
        if keyword in question:
            relevant_context.append(f"\n**错误案例警示**: 检测到关键词\"{keyword}\"，请参考 error_case_analysis.md 中关于 \"{related_charge}\" 的案例分析")
            relevant_context.append("\n" + error_case_analysis)
            break

    # Combine all relevant context
    final_context = '\n\n'.join(filter(None, relevant_context))

    return final_context
