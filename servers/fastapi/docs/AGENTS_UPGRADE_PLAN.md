# 演示生成核心逻辑升级实施计划

## 一、目标

提升演示生成质量，接近原版 Presenton：支持美化、图表、结构化布局。通过三个专用 Agent 与统一的 Pydantic 状态模型实现。

---

## 二、核心模型设计

### 2.1 PresentationState（前端/后端共享）

**位置**: `models/presentation_state.py`（新建）

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class SlideState(BaseModel):
    """单页幻灯片状态"""
    title: str = Field(description="幻灯片标题")
    bullet_points: List[str] = Field(description="核心要点列表，每个 1–2 行", max_items=8)
    image_prompt: Optional[str] = Field(default=None, description="配图描述，用于 AI 生成或 Unsplash 搜索")
    layout_id: str = Field(description="Tailwind 布局 ID，对应 template_registry 中的 id")

class PresentationState(BaseModel):
    """演示文稿完整状态"""
    title: Optional[str] = Field(default=None, description="演示标题")
    slides: List[SlideState] = Field(description="幻灯片列表", min_items=1)
```

**约束**：
- `layout_id` 必须属于 `get_all_layout_ids()` 返回的有效 ID
- `bullet_points` 每个最多 ~100 字符，总页数由参数控制

---

## 三、三个 Agent 设计与实现

### 3.1 RESEARCH_AGENT（研究智能体）

**文件**: `agents/research_agent.py`（新建）

**职责**：从用户输入（文本、文件摘要、slides_markdown）提取结构化 JSON 大纲。

**System Prompt 要点**：
- 角色：资深演示架构师 + 数据分析师
- 输出：**纯 JSON**，符合 `PresentationState` 的 Pydantic 模式
- 禁止：Markdown 代码块、解释性文字
- 规则：
  - 每页：标题、3–6 个要点、配图描述（可选）
  - 第一页通常为标题页
  - 数据/对比类内容需提炼为要点
  - 支持联网检索（可选）
- 语言：按 `language` 参数输出

**接口**：
```python
async def research_agent_run(
    content: str,
    n_slides: int,
    language: str = "Chinese",
    additional_context: Optional[str] = None,
    tone: Optional[str] = None,
    verbosity: Optional[str] = None,
    instructions: Optional[str] = None,
    include_title_slide: bool = True,
    web_search: bool = False,
) -> PresentationState
```

**实现要点**：
- 使用 `services/llm_client.LLMClient.generate_structured()` 或 `stream_structured()`
- 使用 `get_model_for_task("outline")` 选择模型
- 强制解析为 `PresentationState`，解析失败时重试或返回明确错误
- 可为 `layout_id` 暂填占位（如 `"unknown"`），由 DESIGN_AGENT 覆盖

---

### 3.2 DESIGN_AGENT（设计智能体）

**文件**: `agents/design_agent.py`（新建）

**职责**：为 RESEARCH_AGENT 输出的大纲分配合适的 `layout_id`。

**System Prompt 要点**：
- 角色：专业演示设计师，熟悉视觉层次与数据可视化
- 输入：RESEARCH_AGENT 输出的 `PresentationState`（可不含或含占位 `layout_id`）
- 输出：同结构的 `PresentationState`，每页 `layout_id` 已填充
- 规则（参考 template_registry 中 layout 的 description）：
  - 标题/封面 → `general-intro-slide` / `basic-info-slide`
  - 要点较多（≥4）→ `bullet-with-icons-slide` / `numbered-bullets-slide` / `dual-column-list-slide`
  - 数据/指标 → `metrics-slide` / `chart-with-bullets-slide` / `dashboard-*`
  - 引用 → `quote-slide`
  - 流程图/步骤 → `visual-process-*`
  - 对比 → `side-by-side-*`
- 提供 `get_all_layout_ids()` 列表，限制只能从该集合选

**接口**：
```python
async def design_agent_run(
    state: PresentationState,
    layout_group: str = "general",  # general | modern | standard | swift
    instructions: Optional[str] = None,
) -> PresentationState
```

**实现要点**：
- 加载 `utils/template_registry.get_layout_by_group(layout_group)` 获取可用 layout 列表
- 在 system prompt 中注入 layout id + name + description
- 输出必须保持 `slides` 顺序和内容，仅修改 `layout_id`
- 使用 `response_model=PresentationState` 或等价 schema 强制 JSON 结构

---

### 3.3 VIBE_EDITOR（风格/指令编辑智能体）

**文件**: `agents/vibe_editor.py`（新建）

**职责**：根据自然语言指令修改 `PresentationState`。

**System Prompt 要点**：
- 角色：演示内容编辑专家
- 输入：当前 `PresentationState` JSON + 用户自然语言指令（如「让内容更简洁」「增加数据支撑」「换成更正式的语气」）
- 输出：修改后的 `PresentationState`
- 规则：
  - 仅修改与指令相关的字段
  - 保持 slides 数量与 layout_id 不变（除非指令明确要求改布局）
  - 不擅自添加/删除幻灯片
  - 输出纯 JSON，无 Markdown

**接口**：
```python
async def vibe_editor_run(
    state: PresentationState,
    instruction: str,
    language: str = "Chinese",
) -> PresentationState
```

**实现要点**：
- 将 `state.model_dump_json()` 作为 user message 一部分
- instruction 作为另一段 user message
- 使用 `generate_structured()` 强制输出 `PresentationState`

---

## 四、Agent 公共基础设施

### 4.1 目录结构

```
servers/fastapi/
├── agents/
│   __init__.py
│   research_agent.py
│   design_agent.py
│   vibe_editor.py
│   _base.py           # 可选：共享的调用、重试、日志
```

### 4.2 共享逻辑（`agents/_base.py`）

```python
# 伪代码
async def call_llm_structured(model, messages, response_schema) -> dict:
    client = LLMClient()
    result = await client.generate_structured(model, messages, response_schema)
    return result
```

- 统一使用 `services/llm_client.LLMClient`
- 统一使用 `utils/llm_provider.get_model_for_task()` 或 `get_model()`
- 解析失败时：重试 1–2 次，或返回 `ValidationError` 给上层

### 4.3 Prompt 变量（推荐）

在 `constants/` 或 `agents/prompts.py` 中定义：

```python
RESEARCH_AGENT_SYSTEM_PROMPT = """..."""
DESIGN_AGENT_SYSTEM_PROMPT = """..."""  # 含 {layout_list} 占位
VIBE_EDITOR_SYSTEM_PROMPT = """..."""
```

便于后续调优与 A/B 测试。

---

## 五、后端集成

### 5.1 新 API 或扩展现有流程

**方案 A**：新增 `/api/v1/ppt/presentation/generate/v2` 端点

1. 接收：content, n_slides, language, template, instructions, files 等
2. 调用 RESEARCH_AGENT → 得到 `PresentationState`
3. 调用 DESIGN_AGENT → 更新 `layout_id`
4. 将 `PresentationState` 转为现有 `PresentationOutlineModel` + `PresentationStructureModel`，进入原有「填充 slide 内容 → 获取 assets → 导出」流水线

**方案 B**：在现有 `generate_presentation_handler` 中替换

- 将 `generate_ppt_outline` + `generate_presentation_structure` 替换为：
  - `research_agent_run` → `design_agent_run`
  - 再将 `PresentationState` 映射到现有结构

### 5.2 PresentationState → 现有模型映射

```python
# PresentationState.slides[i] -> SlideOutlineModel(content=...) 
# 将 title + bullet_points + image_prompt 拼接为 markdown 或结构化 content
# PresentationState.slides[i].layout_id -> layout 的 index（通过 get_slide_layout_index）
```

---

## 六、前端集成

### 6.1 创建演示页面展示 PresentationState

**位置**: `nicegui_app/pages/create.py` 或新建 `create_v2.py`

- 新增「结构化预览」区域
- 使用 `PresentationState` 的 Pydantic 模型在前端做校验（或通过 API 返回 JSON）
- 展示：每页标题、要点、配图描述、布局 ID
- 支持：编辑、调用 VIBE_EDITOR 的入口（输入自然语言指令）

### 6.2 前端状态绑定

- 创建演示时：content / slides_markdown → 调用 RESEARCH → DESIGN → 展示 `PresentationState`
- 用户编辑后：可再次调用 DESIGN_AGENT 重算 layout
- 用户输入指令：调用 VIBE_EDITOR → 更新 `PresentationState` → 刷新预览

---

## 七、实施步骤（建议顺序）

| 阶段 | 任务 | 产出 |
|------|------|------|
| 1 | 定义 `PresentationState`、`SlideState` | `models/presentation_state.py` |
| 2 | 编写 RESEARCH_AGENT + 严格 system prompt | `agents/research_agent.py` |
| 3 | 编写 DESIGN_AGENT + layout 列表注入 | `agents/design_agent.py` |
| 4 | 编写 VIBE_EDITOR | `agents/vibe_editor.py` |
| 5 | 实现 PresentationState → 现有 outline/structure 的映射 | `utils/state_mapper.py` |
| 6 | 集成到 generate 流程（新端点或替换） | `api/v1/ppt/endpoints/presentation.py` |
| 7 | 前端展示 PresentationState + 编辑 / VIBE_EDITOR 入口 | `nicegui_app/pages/create.py` |
| 8 | 测试与调优 | 单元测试 + 集成测试 |

---

## 八、技术要点

1. **JSON 强制解析**：使用 `model_validate()` 或 `model_validate_json()`，捕获 `ValidationError`，重试或返回友好错误
2. **模型选择**：RESEARCH 建议 Claude/GPT-4；DESIGN 建议 Gemini（视觉理解好）；VIBE_EDITOR 可用较小模型
3. **布局 ID 校验**：DESIGN_AGENT 输出用 `assert layout_id in get_all_layout_ids()` 或 Pydantic validator
4. **与现有流程兼容**：不破坏 `/outlines/stream`、`/prepare`、`/export` 等端点，新增或并行 v2 流程

---

## 九、依赖与兼容

- 复用：`services/llm_client`、`utils/llm_provider`、`utils/template_registry`、`models/presentation_layout`
- 无需新增大依赖，Pydantic 已有
- 与 `orchestrator` 可并存，后续可考虑用新 agents 替换 `ResearchAgent` / `DesignAgent`
