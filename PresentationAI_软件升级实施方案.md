# PresentationAI 软件升级实施方案

> 基于《自动PPT生成项目借鉴分析》制定的分阶段实施路线图  
> 制定日期：2026年2月

---

## 一、现状评估

### 1.1 现有优势
- **技术栈**：FastAPI + NiceGUI，与蓝图一致
- **图像处理**：已有 `image_utils.py` 中 `clip_image`（Lanczos 重采样 + object-fit: cover 裁剪逻辑），与借鉴分析建议高度吻合
- **生成流程**：`generate_presentation_outlines` → `generate_slide_content` → `PptxPresentationCreator`，已具备「提示词→LLM→JSON 大纲→pptx 渲染」的基础链路
- **多模型**：支持 OpenAI、Anthropic、Gemini、Ollama 等
- **MCP 支持**：存在 `mcp_server.py`，具备 Agent 扩展基础

### 1.2 待提升领域
| 维度 | 现状 | 目标 |
|------|------|------|
| 生成范式 | 单次生成（Single-pass） | 多智能体编排（Research→Design→Review） |
| 布局决策 | 模板固定选择 | 智能布局决策引擎，动态修复 |
| 文本溢出 | 依赖 PowerPoint 客户端 Autofit | 后端 Pillow 字体矩阵模拟 |
| 数据可视化 | 有限 | Graphviz 流程图 + Vega-Lite 声明式图表 |
| 风格迁移 | 手动选模板 | 视觉参考图 → 多模态分析 → 主题配置 |
| 编辑驱动 | 从零生成 | 基于 .pptx 占位符的编辑式生成 |
| 管道简洁度 | 耦合较多 | 参考 slides_generator 的直线性数据流 |

---

## 二、分阶段实施方案

### 阶段一：基础加固（优先级 P0，约 2–3 周）

**目标**：在不大幅改动架构的前提下，提升稳定性和可维护性。

#### 1.1 借鉴 slides_generator：管道化与模块隔离

- **行动**：梳理并重构 `generate_stream`、`generate_presentation_structure`、`generate_slide_content` 等逻辑。
- **原则**：将「LLM 文本生成」「图像请求」「pptx 构造」严格物理隔离为独立函数/模块。
- **产出**：`servers/fastapi/pipeline/` 目录，包含：
  - `text_generation.py`：纯 LLM 内容生成
  - `image_requests.py`：图像 API 调用与路径管理
  - `pptx_constructor.py`：封装 `PptxPresentationCreator` 调用
- **收益**：降低复杂度，为后续引入 Agent 提供清晰接入点。

#### 1.2 图像处理增强（Pillow 深度协同）

- **现状**：已有 `clip_image`（object-fit: cover）、`fit_image` 等。
- **补充**：
  - **色彩协调**：在 `image_utils.py` 中新增 `align_image_to_theme_colors(image, theme_hex_list)`，基于 LAB 色彩空间微调色相/饱和度，使 AI 图像与模板主色一致。
  - **占位符精准适配**：确保所有 `add_picture` 前都经 `clip_image` 或等价逻辑处理，杜绝直接拉伸。
  - **内存优化**：统一使用 `io.BytesIO` 传递图像，避免磁盘 I/O。

#### 1.3 文本溢出防护（Text Autofit 三重策略）

- **策略 1（提示词）**：在 `generate_slide_content` 的 system prompt 中明确每个布局的字符上限（如单行标题 ≤ 50 字，要点 ≤ 200 字）。
- **策略 2（pptx 属性）**：在 `PptxPresentationCreator` 中为所有文本框设置：
  ```python
  text_frame.word_wrap = True
  text_frame.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
  ```
- **策略 3（可选高级）**：新增 `utils/text_autofit.py`，用 Pillow 的 `ImageFont.getbbox()` 模拟文本尺寸，超限时循环递减字号直至适应。

---

### 阶段二：智能编排与多智能体（优先级 P1，约 4–6 周）

**目标**：引入 PPTAgent 风格的多智能体管线，替代单次生成。

#### 2.1 主控调度器（Orchestrator）

- **位置**：`servers/fastapi/orchestrator/` 或 `services/orchestrator/`
- **职责**：
  - 接收用户 Prompt / Markdown / 上传文档
  - 依次调度：Research Agent → Design Agent →（可选）Review Agent
  - 管理中间状态（JSON 大纲、布局 ID、资产路径）
- **接口设计**：
  ```python
  async def run_pipeline(
      user_input: str,
      context: PresentationContext,
  ) -> PresentationResult:
      outline = await research_agent.run(user_input, context)
      designed = await design_agent.run(outline, context)
      if enable_review:
          designed = await review_agent.run(designed, context)
      return designed
  ```

#### 2.2 研究智能体（Research Agent）

- **模型建议**：Claude 3.5 / GLM-4 等
- **输入**：用户 Prompt、可选 PDF/Word（经 Docling/MinerU 解析）
- **输出**：符合 Pydantic  schema 的 JSON 大纲（如 `PresentationOutlineModel`）
- **提示词约束**：
  - 强制纯 JSON 输出，禁止 ```json 包裹或说明文字
  - 角色设定（Persona）：如「资深数据分析师」「技术架构师」
- **可复用**：可基于现有 `generate_presentation_outlines` 做增强，增加 Web 搜索、文档解析等能力。

#### 2.3 设计智能体（Design Agent）

- **模型建议**：Gemini 1.5 Pro（擅长自由形态视觉设计）
- **输入**：研究智能体输出的 JSON 大纲
- **输出**：带 layout_id 的增强 JSON，以及图表/图像生成指令
- **职责**：
  - 从布局注册表选择 Tailwind/Layout ID
  - 规则约束：如「超过 4 个要点 → dual_column_list」「含数据对比 → 触发图表 API」
  - 调用 MCP 工具（图像预处理、图表渲染等）

#### 2.4 评审智能体（Review Agent，可选）

- **模型**：本地 Llama 3 或轻量模型
- **职责**：内容一致性、布局合理性、逻辑流检查
- **触发**：检测到布局溢出或逻辑断层时，返回「退回重绘」指令
- **参考**：PPTAgent 的 PPTEval 框架

#### 2.5 提示词工程体系

- **结构**：`servers/fastapi/prompts/`，按 Agent 分文件
- **变量**：`{hint}`, `{persona}`, `{layout_constraints}`, `{output_schema}`
- **约束**：每个 prompt 必须包含结构化输出说明（Pydantic schema 或 JSON 示例）

---

### 阶段三：动态布局与实时修复（优先级 P2，约 3–4 周）

**目标**：借鉴 LandPPT，实现智能布局选择与热修复。

#### 3.1 布局决策引擎

- **位置**：`servers/fastapi/layout_engine/`
- **逻辑**：
  - 根据 JSON 内容拓扑（如要点数量、是否有图表）评分
  - 映射到 `get_layout_by_name` 的现有布局体系
  - 规则示例：3 项论点 → 三列；4+ 项 → grid-cols-2 grid-rows-2
- **集成**：在 Design Agent 输出后调用，或在 NiceGUI 大纲编辑器的「添加/删除项」时实时触发。

#### 3.2 视觉参考与风格迁移

- **功能**：用户上传参考图（海报、竞品幻灯片截图）
- **流程**：Base64 → 多模态 API（GPT-4o / Gemini 1.5 Pro）→ 提取主色调 Hex、排版密度、字体层级
- **输出**：Tailwind 主题配置字典，注入 NiceGUI 运行时
- **固化**：在 pptx 导出时将 Hex 转为 `RGBColor`，写入幻灯片主题

#### 3.3 Markdown Frontmatter 支持

- **格式**：`--- theme: light; layout: split_image_right ---`
- **解析**：在 Markdown 输入解析阶段拦截，驱动布局切换与母版索引选择
- **参考**：Marp、Slidev 的 YAML Frontmatter 模式

---

### 阶段四：数据可视化与 MCP 扩展（优先级 P3，约 3–4 周）

**目标**：引入 Chat2PPTX 风格的数据图表能力。

#### 4.1 Graphviz 流程图

- **场景**：算法流程、组织架构、因果关系
- **流程**：研究智能体检测 → 输出标准 DOT 语法 → `pygraphviz` 解析 → CairoSVG 渲染 PNG → Pillow 裁剪 → 插入幻灯片
- **安全**：仅解析 DOT，不执行任意代码

#### 4.2 声明式图表（Vega-Lite / JSON）

- **原则**：禁止 LLM 生成可执行代码，改为输出 JSON 规范
- **实现**：LLM 输出 Vega-Lite 或自定义 JSON（type, data, axes）→ FastAPI 用 Matplotlib/Plotly 非交互后端渲染 → BytesIO → Pillow 去白边 → 插入 pptx
- **参考**：chat2plot 的思路

#### 4.3 MCP 工具封装

- **目标**：将现有 API（图像预处理、模板检索、导出）封装为 MCP 工具
- **收益**：Design Agent 可自主决定何时调用图像处理、何时请求图表渲染

---

### 阶段五：编辑驱动生成（优先级 P4，约 2–3 周）

**目标**：支持基于现有 .pptx 模板的「编辑式」生成。

#### 5.1 占位符提取

- **输入**：用户上传的 .pptx 模板
- **逻辑**：解析占位符 XML（python-pptx 的 `slide.shapes.placeholders`）→ 转为 JSON 模式
- **输出**：`{ slide_type, placeholder_ids, content_hints }`

#### 5.2 编辑指令生成

- **LLM 任务**：针对提取的模式，输出「填充/修改」指令序列，而非从零生成整页
- **优势**：保留模板原有设计，仅替换内容，减少排版崩溃

---

## 三、技术架构总览（目标状态）

```
┌─────────────────────────────────────────────────────────────────┐
│  统一网关层 (FastAPI + NiceGUI WebSocket)                         │
│  - Prompt / Markdown / 文档上传 / 视觉参考上传                     │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  多智能体编排层 (Orchestrator)                                     │
│  Research → Design → Review (可选)                                │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  视觉与图表渲染中枢                                                │
│  - Matplotlib / Graphviz 管道                                     │
│  - Pillow 图像预处理（裁剪、色彩对齐、去白边）                       │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  中间表示与实时反馈 (NiceGUI 状态树)                                │
│  - HTML/Tailwind 预览 / 布局热修复                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  编译与导出 (python-pptx / 坐标映射)                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 四、依赖与资源建议

### 4.1 新增 Python 依赖（已实施）

```toml
# pyproject.toml 已添加
numpy>=1.24.0           # align_image_to_theme_colors
[graphviz]               # 可选：pip install .[graphviz]
pygraphviz>=1.11         # 流程图（需系统安装 Graphviz）
```

**Graphviz 系统安装**（Windows）：
1. 下载 https://graphviz.org/download/
2. 安装后将 bin 目录加入 PATH

### 4.2 参考开源项目

| 能力 | 参考项目 | 用途 |
|------|----------|------|
| 管道简化 | [ai-forever/slides_generator](https://github.com/ai-forever/slides_generator) | 直线性数据流 |
| 多智能体 | [icip-cas/PPTAgent](https://github.com/icip-cas/PPTAgent) | 编排与提示词 |
| 动态布局 | [sligter/LandPPT](https://github.com/sligter/LandPPT) | 布局修复、视觉参考 |
| 数据图表 | [ihopeit/chat2pptx](https://github.com/ihopeit/chat2pptx) | Graphviz、Markdown 转 PPT |
| 声明式图表 | [nyanp/chat2plot](https://github.com/nyanp/chat2plot) | JSON→ 可视化 |
| DOM→pptx | [atharva9167j/dom-to-pptx](https://github.com/atharva9167j/dom-to-pptx) | HTML 坐标映射参考 |

---

## 五、风险与应对

| 风险 | 应对 |
|------|------|
| 多智能体增加延迟与成本 | 阶段二可先实现 Research+Design 双智能体，Review 设为可选；支持「单次生成」降级模式 |
| Graphviz 安装复杂 | 提供 Docker 镜像预装，或文档明确 Windows/Linux 安装步骤 |
| MCP 生态不稳定 | 先封装 3–5 个核心工具，其余沿用现有 REST API |
| 视觉参考多模态成本高 | 可限制调用频率，或提供「手动选色」作为替代 |

---

## 六、建议执行顺序（甘特图概览）

```
周次    1  2  3  4  5  6  7  8  9  10 11 12
────────────────────────────────────────────
阶段一  ████████
阶段二        ████████████████
阶段三                  ████████████
阶段四                        ████████████
阶段五                              ████████
```

- **阶段一** 与 **阶段二** 可部分并行：管道重构与 Orchestrator 设计可同步推进。
- **阶段三** 依赖阶段二的 Design Agent 输出结构。
- **阶段四** 可在阶段二完成 Research Agent 后即启动 Graphviz 管线。
- **阶段五** 可作为独立功能，与阶段二、三并行开发。

---

## 七、总结

本方案将《自动PPT生成项目借鉴分析》中的 PPTAgent、LandPPT、slides_generator、Chat2PPTX 等项目的优势，转化为可落地的五阶段实施路径。优先完成**基础加固**和**多智能体编排**，再逐步引入**动态布局**、**数据可视化**和**编辑驱动生成**，可在控制风险的前提下，系统性地提升 PresentationAI 的企业级能力与用户体验。
