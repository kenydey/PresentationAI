"""
提示词约束：文本溢出防护策略 1 - 在 LLM 层面明确字符上限。
供 Research/Design Agent 与 generate_slide_content 复用。
"""

# 各布局类型的建议字符上限（供提示词注入）
LAYOUT_CHAR_LIMITS = {
    "title": 50,           # 单行标题
    "subtitle": 80,         # 副标题
    "body": 200,           # 正文描述
    "bullet_item": 120,    # 每个要点
    "max_bullets": 6,      # 单页最多要点数
    "metric_value": 20,    # 指标数值
    "metric_label": 40,    # 指标标签
}

TEXT_OVERFLOW_SYSTEM_HINT = """
# 文本长度约束（防止排版溢出）
- 单行标题不超过 {title} 字
- 正文描述不超过 {body} 字
- 每个要点不超过 {bullet_item} 字，单页不超过 {max_bullets} 项
- 严格遵守上述上限，超限将导致文本框溢出
""".format(**LAYOUT_CHAR_LIMITS).strip()
