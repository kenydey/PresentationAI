require("dotenv").config();
import { app, BrowserWindow } from "electron";
import path from "path";
import { findTwoUnusedPorts, killProcess } from "./utils";
import { startFastApiServer, startNextJsServer } from "./servers";
import { ChildProcessByStdio } from "child_process";
import { localhost } from "./constants";

var isDev = process.env.DEBUG === "True";
var baseDir = isDev ? process.cwd() : process.resourcesPath;
var resourcesDir = path.join(baseDir, "resources");
var fastapiDir = isDev ? path.join(baseDir, "servers/fastapi") : path.join(resourcesDir, "fastapi");
var nextjsDir = isDev ? path.join(baseDir, "servers/nextjs") : path.join(resourcesDir, "nextjs");

var win: BrowserWindow | undefined;
var fastApiProcess: ChildProcessByStdio<any, any, any> | undefined;
var nextjsProcess: ChildProcessByStdio<any, any, any> | undefined;

const createWindow = () => {
  win = new BrowserWindow({
    webPreferences: {
      webSecurity: false,
    },
    width: 1280,
    height: 720,
  });
};

async function startServers(fastApiPort: number, nextjsPort: number) {
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
    nextjsProcess = await startNextJsServer(
      nextjsDir,
      nextjsPort,
      {
        NEXT_PUBLIC_API: `${localhost}:${fastApiPort}`,
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
  if (nextjsProcess?.pid) {
    await killProcess(nextjsProcess.pid);
  }
}

app.whenReady().then(async () => {
  createWindow();
  win?.loadFile(path.join(resourcesDir, "ui/homepage/index.html"));
  win?.webContents.openDevTools();

  const [fastApiPort, nextjsPort] = await findTwoUnusedPorts();
  console.log(`FastAPI port: ${fastApiPort}, NextJS port: ${nextjsPort}`);

  await startServers(fastApiPort, nextjsPort);
  win?.loadURL(`${localhost}:${nextjsPort}/upload`);
});

app.on("window-all-closed", async () => {
  await stopServers();
  app.quit();
});
