from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from api.lifespan import app_lifespan
from api.middlewares import UserConfigEnvUpdateMiddleware
from api.v1.ppt.router import API_V1_PPT_ROUTER
from api.v1.webhook.router import API_V1_WEBHOOK_ROUTER
from api.v1.mock.router import API_V1_MOCK_ROUTER
from nicegui_app import register_nicegui


app = FastAPI(lifespan=app_lifespan)

# Routers
app.include_router(API_V1_PPT_ROUTER)
app.include_router(API_V1_WEBHOOK_ROUTER)
app.include_router(API_V1_MOCK_ROUTER)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(UserConfigEnvUpdateMiddleware)


@app.get("/", include_in_schema=False)
def _redirect_root_to_ui():
    """根路径重定向到 /ui，避免访问 / 时出现 404。"""
    return RedirectResponse(url="/ui/", status_code=302)


# 将 NiceGUI 直接挂载到主 app 的 /ui 路径（避免子 app mount 导致 404）
register_nicegui(app)
