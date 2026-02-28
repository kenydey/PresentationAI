require("dotenv").config();
import { app, BrowserWindow } from "electron";
import path from "path";
import { findTwoUnusedPorts, killProcess } from "./utils";
import { startFastApiServer } from "./servers";
import { ChildProcessByStdio } from "child_process";
import { localhost } from "./constants";

var isDev = process.env.DEBUG === "True";
var baseDir = isDev ? process.cwd() : process.resourcesPath;
var resourcesDir = path.join(baseDir, "resources");
var fastapiDir = isDev ? path.join(baseDir, "servers/fastapi") : path.join(resourcesDir, "fastapi");

var win: BrowserWindow | undefined;
var fastApiProcess: ChildProcessByStdio<any, any, any> | undefined;

const createWindow = () => {
  win = new BrowserWindow({
    webPreferences: {
      webSecurity: false,
    },
    width: 1280,
    height: 720,
  });
};

async function startServers(fastApiPort: number) {
  try {
    fastApiProcess = await startFastApiServer(
      fastapiDir,
      fastApiPort,
      {
        DEBUG: isDev ? "True" : "False",
        LLM: process.env.LLM || "",
        LIBREOFFICE: process.env.LIBREOFFICE || "",
        OPENAI_API_KEY: process.env.OPENAI_API_KEY || "",
        GOOGLE_API_KEY: process.env.GOOGLE_API_KEY || "",
        APP_DATA_DIRECTORY: process.env.APP_DATA_DIRECTORY || "",
        TEMP_DIRECTORY: process.env.TEMP_DIRECTORY || "",
      },
      isDev
    );
  } catch (error) {
    console.error("Server startup error:", error);
  }
}

async function stopServers() {
  if (fastApiProcess?.pid) {
    await killProcess(fastApiProcess.pid);
  }
}

app.whenReady().then(async () => {
  createWindow();
  win?.loadFile(path.join(resourcesDir, "ui/homepage/index.html"));

  const [fastApiPort] = await findTwoUnusedPorts();
  console.log(`FastAPI port: ${fastApiPort}`);

  await startServers(fastApiPort);
  // Load NiceGUI UI directly from FastAPI
  win?.loadURL(`${localhost}:${fastApiPort}/ui/`);
});

app.on("window-all-closed", async () => {
  await stopServers();
  app.quit();
});
