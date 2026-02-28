"""Async HTTP helpers for calling the FastAPI backend from NiceGUI pages."""

import os
import aiohttp
import json
from typing import Any, Optional


def get_base_url() -> str:
    return (
        os.getenv("FASTAPI_URL")
        or os.getenv("NEXT_PUBLIC_FAST_API")
        or f"http://127.0.0.1:{os.getenv('FASTAPI_PORT', '8000')}"
    ).rstrip("/")


async def api_get(path: str, **kwargs) -> tuple[int, Any]:
    url = get_base_url() + path
    async with aiohttp.ClientSession() as s:
        async with s.get(url, **kwargs) as r:
            try:
                data = await r.json()
            except Exception:
                data = await r.text()
            return r.status, data


async def api_post(path: str, payload: Optional[dict] = None, **kwargs) -> tuple[int, Any]:
    url = get_base_url() + path
    async with aiohttp.ClientSession() as s:
        async with s.post(url, json=payload, **kwargs) as r:
            try:
                data = await r.json()
            except Exception:
                data = await r.text()
            return r.status, data


async def api_patch(path: str, payload: dict) -> tuple[int, Any]:
    url = get_base_url() + path
    async with aiohttp.ClientSession() as s:
        async with s.patch(url, json=payload) as r:
            try:
                data = await r.json()
            except Exception:
                data = await r.text()
            return r.status, data


async def api_delete(path: str) -> tuple[int, Any]:
    url = get_base_url() + path
    async with aiohttp.ClientSession() as s:
        async with s.delete(url) as r:
            try:
                data = await r.json()
            except Exception:
                data = await r.text()
            return r.status, data


async def api_post_form(path: str, data: aiohttp.FormData) -> tuple[int, Any]:
    url = get_base_url() + path
    async with aiohttp.ClientSession() as s:
        async with s.post(url, data=data) as r:
            try:
                resp = await r.json()
            except Exception:
                resp = await r.text()
            return r.status, resp


async def api_stream_sse(path: str):
    """Yield parsed SSE data dicts from an event stream."""
    url = get_base_url() + path
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            if r.status != 200:
                return
            buf = ""
            async for chunk, _ in r.content.iter_chunks():
                if not chunk:
                    continue
                buf += chunk.decode("utf-8", errors="ignore")
                while "\n\n" in buf:
                    block, buf = buf.split("\n\n", 1)
                    lines = [ln for ln in block.splitlines() if ln.strip()]
                    data_line = next((ln for ln in lines if ln.startswith("data:")), None)
                    if not data_line or len(data_line) <= 5:
                        continue
                    try:
                        yield json.loads(data_line[5:].strip())
                    except Exception:
                        continue
