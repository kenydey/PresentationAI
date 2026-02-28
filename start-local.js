/**
 * Presenton 本地运行脚本 (uv / pip 安装模式)
 * 仅运行 FastAPI（内含 NiceGUI 前端），不再依赖 Next.js
 *
 * 使用方式:
 *   node start-local.js           # uv 模式 (默认)
 *   node start-local.js --pip     # pip 模式 (使用 .venv)
 *   node start-local.js --dev     # 开发模式 + 热重载
 */

import { join, dirname } from "path";
import { fileURLToPath } from "url";
import { spawn } from "child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const fastapiDir = join(__dirname, "servers/fastapi");

const args = process.argv.slice(2);
const hasDevArg = args.includes("--dev") || args.includes("-d");
const usePip = args.includes("--pip");
const isDev = hasDevArg;

const fastapiPort = parseInt(process.env.FASTAPI_PORT || "8000", 10);
const appmcpPort = parseInt(process.env.MCP_PORT || "8001", 10);

// 本地模式默认使用项目内的 app_data
const appDataDir = process.env.APP_DATA_DIRECTORY || join(__dirname, "app_data");
process.env.APP_DATA_DIRECTORY = appDataDir;
process.env.TEMP_DIRECTORY = process.env.TEMP_DIRECTORY || join(__dirname, "tmp");
process.env.CAN_CHANGE_KEYS = process.env.CAN_CHANGE_KEYS || "true";

const userConfigPath = join(appDataDir, "userConfig.json");
const userDataDir = dirname(userConfigPath);

// 创建数据目录
[userDataDir, process.env.TEMP_DIRECTORY].forEach((dir) => {
  if (dir && !existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
    console.log("创建目录:", dir);
  }
});

process.env.USER_CONFIG_PATH = userConfigPath;

const setupUserConfigFromEnv = () => {
  let existingConfig = {};
  if (existsSync(userConfigPath)) {
    try {
      existingConfig = JSON.parse(readFileSync(userConfigPath, "utf8"));
    } catch (_) {}
  }
  if (!["ollama", "openai", "google", "anthropic", "custom"].includes(existingConfig.LLM)) {
    existingConfig.LLM = undefined;
  }

  const userConfig = {
    LLM: process.env.LLM || existingConfig.LLM,
    OPENAI_API_KEY: process.env.OPENAI_API_KEY || existingConfig.OPENAI_API_KEY,
    OPENAI_MODEL: process.env.OPENAI_MODEL || existingConfig.OPENAI_MODEL,
    GOOGLE_API_KEY: process.env.GOOGLE_API_KEY || existingConfig.GOOGLE_API_KEY,
    GOOGLE_MODEL: process.env.GOOGLE_MODEL || existingConfig.GOOGLE_MODEL,
    OLLAMA_URL: process.env.OLLAMA_URL || existingConfig.OLLAMA_URL,
    OLLAMA_MODEL: process.env.OLLAMA_MODEL || existingConfig.OLLAMA_MODEL,
    ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY || existingConfig.ANTHROPIC_API_KEY,
    ANTHROPIC_MODEL: process.env.ANTHROPIC_MODEL || existingConfig.ANTHROPIC_MODEL,
    CUSTOM_LLM_URL: process.env.CUSTOM_LLM_URL || existingConfig.CUSTOM_LLM_URL,
    CUSTOM_LLM_API_KEY: process.env.CUSTOM_LLM_API_KEY || existingConfig.CUSTOM_LLM_API_KEY,
    CUSTOM_MODEL: process.env.CUSTOM_MODEL || existingConfig.CUSTOM_MODEL,
    PEXELS_API_KEY: process.env.PEXELS_API_KEY || existingConfig.PEXELS_API_KEY,
    PIXABAY_API_KEY: process.env.PIXABAY_API_KEY || existingConfig.PIXABAY_API_KEY,
    IMAGE_PROVIDER: process.env.IMAGE_PROVIDER || existingConfig.IMAGE_PROVIDER,
    TOOL_CALLS: process.env.TOOL_CALLS || existingConfig.TOOL_CALLS,
    DISABLE_THINKING: process.env.DISABLE_THINKING || existingConfig.DISABLE_THINKING,
    EXTENDED_REASONING: process.env.EXTENDED_REASONING || existingConfig.EXTENDED_REASONING,
    WEB_GROUNDING: process.env.WEB_GROUNDING || existingConfig.WEB_GROUNDING,
    COMFYUI_URL: process.env.COMFYUI_URL || existingConfig.COMFYUI_URL,
    COMFYUI_WORKFLOW: process.env.COMFYUI_WORKFLOW || existingConfig.COMFYUI_WORKFLOW,
    DALL_E_3_QUALITY: process.env.DALL_E_3_QUALITY || existingConfig.DALL_E_3_QUALITY,
    GPT_IMAGE_1_5_QUALITY: process.env.GPT_IMAGE_1_5_QUALITY || existingConfig.GPT_IMAGE_1_5_QUALITY,
  };
  writeFileSync(userConfigPath, JSON.stringify(userConfig, null, 2));
};

// 获取 Python 执行命令
const getPythonCmd = () => {
  if (usePip) {
    const venvPython =
      process.platform === "win32"
        ? join(fastapiDir, ".venv/Scripts/python.exe")
        : join(fastapiDir, ".venv/bin/python");
    if (existsSync(venvPython)) {
      return [venvPython];
    }
    console.warn("未找到 .venv，请先运行 scripts/install-with-pip.*");
    return [process.platform === "win32" ? "python" : "python3"];
  }
  // uv 模式
  return ["uv", "run", "python"];
};

const getServerArgs = (cmd) => {
  const base = ["server.py", "--port", fastapiPort.toString(), "--reload", isDev ? "true" : "false"];
  return cmd[0] === "uv" ? ["run", "python", ...base] : base;
};

const getMcpArgs = (cmd) => {
  const base = ["mcp_server.py", "--port", appmcpPort.toString()];
  return cmd[0] === "uv" ? ["run", "python", ...base] : base;
};

const startServers = async () => {
  const pythonCmd = getPythonCmd();

  console.log("\n==> Presenton 本地模式 (FastAPI + NiceGUI)");
  console.log("    UI:   http://localhost:" + fastapiPort + "/ui");
  console.log("    API:  http://localhost:" + fastapiPort + "/docs");
  console.log("    模式:", usePip ? "pip" : "uv");
  if (isDev) console.log("    开发: 热重载已启用");
  console.log("");

  const fastApiProcess = spawn(pythonCmd[0], getServerArgs(pythonCmd), {
    cwd: fastapiDir,
    stdio: "inherit",
    env: { ...process.env },
  });

  fastApiProcess.on("error", (err) => {
    console.error("FastAPI 启动失败:", err.message);
  });

  const appmcpProcess = spawn(pythonCmd[0], getMcpArgs(pythonCmd), {
    cwd: fastapiDir,
    stdio: "ignore",
    env: { ...process.env },
  });

  appmcpProcess.on("error", (err) => {
    console.error("MCP 启动失败:", err.message);
  });

  // Ollama (可选)
  let ollamaProcess = null;
  let ollamaConfig = process.env.LLM;
  if (!ollamaConfig && existsSync(userConfigPath)) {
    try {
      ollamaConfig = JSON.parse(readFileSync(userConfigPath, "utf8")).LLM;
    } catch (_) {}
  }
  if (ollamaConfig === "ollama") {
    try {
      ollamaProcess = spawn("ollama", ["serve"], {
        cwd: process.platform === "win32" ? __dirname : "/",
        stdio: "inherit",
        env: process.env,
      });
      ollamaProcess.on("error", (err) => {
        console.warn("Ollama 启动失败(可选):", err.message);
      });
    } catch (err) {
      console.warn("Ollama 启动失败(可选):", err.message);
    }
  }

  const exitPromises = [
    new Promise((r) => fastApiProcess.on("exit", r)),
  ];
  if (ollamaProcess) {
    exitPromises.push(new Promise((r) => ollamaProcess.on("exit", r)));
  }
  const code = await Promise.race(exitPromises);
  console.log("\n进程退出，code:", code);
  process.exit(code ?? 1);
};

setupUserConfigFromEnv();
startServers();
