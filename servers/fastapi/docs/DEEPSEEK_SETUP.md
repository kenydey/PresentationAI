# DeepSeek LLM 配置指南

## 1. 配置 DeepSeek

在 `servers/fastapi` 目录下执行：

```bash
APP_DATA_DIRECTORY=/tmp/app_data USER_CONFIG_PATH=/tmp/app_data/userConfig.json \
DEEPSEEK_API_KEY="你的API密钥" \
uv run python scripts/configure_deepseek.py
```

配置将写入 `userConfig.json`，包含：
- `base_url`: https://api.deepseek.com
- `default_model`: deepseek-chat
- `TOOL_CALLS`: true（DeepSeek 不支持 response_format，需使用 tool_calls 输出结构化 JSON）

## 2. 启动服务器

```bash
cd servers/fastapi
APP_DATA_DIRECTORY=/tmp/app_data TEMP_DIRECTORY=/tmp/presenton \
DATABASE_URL="sqlite+aiosqlite:////tmp/app_data/fastapi.db" \
USER_CONFIG_PATH=/tmp/app_data/userConfig.json \
DISABLE_ANONYMOUS_TRACKING=true CAN_CHANGE_KEYS=true \
DISABLE_IMAGE_GENERATION=true \
uv run python server.py --port 8000 --reload true
```

或使用 `node start-local.js`（若存在）。

## 3. 已修复项

- **LLM Provider 回退**：`get_llm_provider()` 在环境变量未设置时从 userConfig 读取
- **启动时加载配置**：lifespan 中调用 `update_env_with_user_config()`，确保配置生效
- **DeepSeek 兼容**：TOOL_CALLS=true 使用 tool_calls 代替 response_format
- **JSON 解析增强**：支持从 markdown 代码块和纯文本中提取 JSON
- **重试机制**：research_agent 在「无内容」时自动重试一次

## 4. 使用方式

- 打开 http://localhost:8000/ui/
- 进入「创建演示」页，输入关键词（如「人工智能简介」）后点击「同步生成」或「异步生成」
- 或进入「系统设置」验证 LLM 配置是否正确
