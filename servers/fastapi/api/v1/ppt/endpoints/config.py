"""User configuration REST API — replaces Next.js /api/user-config.

GET  /config — read current user config
POST /config — update user config
GET  /config/has-key — check if LLM API key is configured
GET  /config/can-change — check if config changes are allowed
"""

import json
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from models.user_config import UserConfig
from utils.get_env import get_can_change_keys_env, get_user_config_path_env
from utils.user_config import get_user_config, update_env_with_user_config

CONFIG_ROUTER = APIRouter(prefix="/config", tags=["Configuration"])


@CONFIG_ROUTER.get("/", summary="Get current user configuration")
async def get_config():
    try:
        cfg = get_user_config()
        return cfg.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load config: {e}")


@CONFIG_ROUTER.post("/", summary="Update user configuration")
async def update_config(config: UserConfig):
    if get_can_change_keys_env() == "false":
        raise HTTPException(status_code=403, detail="Configuration changes are disabled (CAN_CHANGE_KEYS=false)")

    path = get_user_config_path_env()
    if not path:
        raise HTTPException(status_code=500, detail="USER_CONFIG_PATH not set")

    try:
        existing = get_user_config()
    except Exception:
        existing = UserConfig()

    merged = config.model_dump(exclude_none=True)
    existing_dict = existing.model_dump()
    existing_dict.update(merged)

    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(existing_dict, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save config: {e}")

    try:
        update_env_with_user_config()
    except Exception:
        pass

    return {"success": True, "message": f"Config saved to {path}"}


@CONFIG_ROUTER.get("/has-key", summary="Check if any LLM API key is configured")
async def has_required_key():
    try:
        cfg = get_user_config()
    except Exception:
        return {"hasKey": False}

    has_key = bool(
        cfg.OPENAI_API_KEY
        or cfg.GOOGLE_API_KEY
        or cfg.ANTHROPIC_API_KEY
        or cfg.OLLAMA_URL
        or cfg.CUSTOM_LLM_URL
        or (cfg.openai_compatible_configs and any(
            p.api_key for p in cfg.openai_compatible_configs.values() if p
        ))
    )
    return {"hasKey": has_key}


@CONFIG_ROUTER.get("/can-change", summary="Check if configuration changes are allowed")
async def can_change_keys():
    return {"canChange": get_can_change_keys_env() != "false"}


@CONFIG_ROUTER.get("/telemetry", summary="Get telemetry status")
async def telemetry_status():
    return {"telemetryEnabled": os.getenv("DISABLE_ANONYMOUS_TRACKING", "").lower() != "true"}
