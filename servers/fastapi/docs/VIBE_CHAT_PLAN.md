# Vibe 对话式编辑功能 — 实施计划

## 一、目标

在 `/ui/viewer` 页面增加类似 AI PPT 工具「Vibe」模式的对话式编辑能力：

1. **前端**：右侧聊天气泡窗口（`ui.chat_message`）
2. **后端**：接收自然语言指令（如「把第三页改成案例分析并换成左右排版」）
3. **逻辑**：当前 JSON 状态 + 指令 → `vibe_editor_run` → 新 JSON
4. **实时**：新 JSON 推送前端 → `preview_sandbox` 无刷新重渲染

---

## 二、数据流与映射

### 2.1 当前与目标状态

| 环节 | 当前 | 目标 |
|------|------|------|
| 数据源 | API `slides[]`（SlideModel 格式） | 内存 `PresentationState`（可被 vibe 修改） |
| 预览输入 | `SlidePreviewData`（来自 slide_to_preview_data） | 同上，可从 `SlideState` 转换 |
| 编辑后 | 无 | vibe 返回新 `PresentationState` → 更新预览 |

### 2.2 需要新增的映射

**① API slides → PresentationState**

```
slides_to_presentation_state(slides: List[dict]) -> PresentationState
```

- 遍历每页 `slide`，从 `content` 提取 title、bullets、image_prompt
- `layout_id` 取自 `slide.layout`
- `image_url` 不进 SlideState，vibe 只改文案与 layout_id

**② SlideState → SlidePreviewData**

```
slide_state_to_preview_data(slide: SlideState | dict) -> dict
```

- 直接映射：title, bullet_points, image_prompt, layout_id
- `image_url` 在纯 vibe 场景下为 None（或从原 slides 按 index 保留）

**③ 指令中的页码**

- 用户可能说「第三页」「第 3 页」→ 需在 prompt 中显式说明当前编辑的是哪一页，或让 vibe 处理整体
- 建议：默认针对**当前选中页**，指令中可带「第 N 页」由 LLM 解析；若无则视为当前页

---

## 三、架构方案

### 方案 A：HTTP API（推荐 MVP）

| 步骤 | 说明 |
|------|------|
| 1 | 用户点击发送，触发 Python `async` handler |
| 2 | Handler 取 `instruction`、当前 `PresentationState` |
| 3 | 调用 `vibe_editor_run(state, instruction)` |
| 4 | 用返回的新 state 更新 `state["presentation_state"]` 和预览 |
| 5 | 向 `ui.chat_message` 追加用户消息和 AI 回复 |

- **优点**：实现简单，与 NiceGUI 事件模型一致，无需额外 WebSocket
- **缺点**：不支持流式输出、打字效果

### 方案 B：WebSocket（扩展）

| 步骤 | 说明 |
|------|------|
| 1 | 新增 `GET /api/v1/ppt/vibe/ws` WebSocket 路由 |
| 2 | 页面加载时用 `ui.run_javascript` 建立 WS 连接 |
| 3 | 用户发送 → JS 通过 WS 发送 `{instruction, state}` |
| 4 | 服务端收到后调用 `vibe_editor_run`，通过 WS 回传新 state |
| 5 | 客户端收到后需通知 Python 更新 UI |

- **难点**：WS 在浏览器，Python 负责渲染；收到新 state 后要驱动 NiceGUI 更新
- **可行做法**：JS 收到后调 `fetch('/api/v1/ppt/vibe/apply', {body: newState})`，后端写入 session；页面用 `ui.timer` 轮询或通过 `ui.run_javascript` 的返回值触发 Python 刷新
- **更优**：用**混合模式**：发送用 HTTP，WebSocket 仅用于服务端主动推送（如后续多人协作、流式打字）

### 推荐实施顺序

1. **阶段 1**：HTTP API + `ui.chat_message`（快速上线）
2. **阶段 2**：视需求增加 WebSocket（流式、多人等）

---

## 四、实施步骤（阶段 1）

| 步骤 | 任务 | 产出 |
|------|------|------|
| 1 | 新增 `slides_to_presentation_state`，API slides → PresentationState | `nicegui_app/utils/vibe_state.py` 或扩展 `utils/state_mapper.py` |
| 2 | 新增 `slide_state_to_preview_data`，SlideState → SlidePreviewData | 同上或 `slide_preview_data.py` |
| 3 | 新增 HTTP 接口 `POST /api/v1/ppt/vibe/edit`，入参：presentation_id / slides + instruction，内部调 `vibe_editor_run` | `api/v1/ppt/endpoints/vibe.py` |
| 4 | 修改 viewer：加载演示时构建并缓存 `PresentationState` | 在 `load_pres` 中调用 `slides_to_presentation_state` |
| 5 | 右侧新增聊天气泡区：`ui.chat_message` 容器 + 输入框 + 发送按钮 | 修改 `pages/viewer.py` |
| 6 | 发送 handler：调 vibe API → 用新 state 更新 `state["presentation_state"]` 和预览列表 → 刷新当前页预览 | 同上 |
| 7 | （可选）放宽 vibe_editor 的 layout_id 约束，或增加「允许改 layout」参数，以支持「换成左右排版」类指令 | `agents/vibe_editor.py` |

---

## 五、UI 布局示意

```
+------------------+------------------------+------------------+
| 幻灯片列表       | 预览 / 字段 / HTML...  | Vibe 对话        |
| (左栏 264px)     | (中央 flex-1)          | (右栏 320px)     |
|                  |                        |                  |
| [1. xxx]         |  +------------------+  | 聊天气泡         |
| [2. xxx]         |  | 16:9 预览         |  | - 用户：把第3页  |
| [3. xxx] ← 当前  |  |                  |  |   改成案例分析   |
| ...              |  +------------------+  | - AI：已修改     |
|                  |                        |                  |
| [AI 编辑此页]    | [预览][字段][HTML]... | 输入框           |
|                  |                        | [发送]           |
+------------------+------------------------+------------------+
```

---

## 六、API 设计（HTTP）

### `POST /api/v1/ppt/vibe/edit`

**Request:**
```json
{
  "slides": [ /* 当前 slides，SlideModel 序列化格式 */ ],
  "instruction": "把第三页改成案例分析并换成左右排版",
  "language": "Chinese"
}
```

**Response:**
```json
{
  "presentation_state": { /* PresentationState JSON */ },
  "message": "已按指令修改"
}
```

**逻辑**：
1. `slides` → `slides_to_presentation_state` → `PresentationState`
2. `vibe_editor_run(state, instruction, language)`
3. 返回新 `PresentationState`

---

## 七、Vibe 指令与 layout 变更

- 当前 `vibe_editor`：系统 prompt 要求「保持 layout_id 不变」
- 用户说「换成左右排版」时，需要改 layout_id
- **方案**：
  - **7a**：为 viewer 场景单独写一个 prompt，允许在指令明确要求时修改 layout_id
  - **7b**：增加参数 `allow_layout_change: bool`，为 True 时在 schema 中不限制 layout_id

---

## 八、错误与边界

- 未加载演示时：禁用发送，或提示「请先加载演示」
- LLM 异常：在 chat 中追加「❌ 修改失败：{error}」
- 空指令：前端校验，不发起请求

---

## 九、后续扩展（阶段 2）

1. **WebSocket 流式**：vibe 思考过程或部分结果分 chunk 推送
2. **持久化**：将修改写回数据库，而不是仅内存展示
3. **撤销/重做**：基于 `presentation_state` 历史栈
