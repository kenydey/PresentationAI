#!/usr/bin/env python3
"""
Call POST /api/v1/ppt/presentation/generate with the same payload the NiceGUI
presentation page sends. Run with the server up: uv run python scripts/request_generate.py
Use to verify backend wiring without opening the browser.
"""
import asyncio
import json
import os
import sys

try:
    import aiohttp
except ImportError:
    print("aiohttp required. Run from project root: uv run python scripts/request_generate.py")
    sys.exit(1)

BASE = os.getenv("FASTAPI_URL") or os.getenv("NEXT_PUBLIC_FAST_API") or "http://127.0.0.1:8000"
URL = BASE.rstrip("/") + "/api/v1/ppt/presentation/generate"

PAYLOAD = {
    "content": "介绍公司新产品的发布会：核心亮点、目标用户与市场机会。",
    "n_slides": 4,
    "language": "Chinese",
    "export_as": "pptx",
    "template": "general",
    "tone": "default",
    "verbosity": "standard",
    "include_table_of_contents": False,
    "include_title_slide": True,
    "web_search": False,
}


async def main():
    print(f"POST {URL}")
    print(f"Payload: n_slides={PAYLOAD['n_slides']}, template={PAYLOAD['template']}")
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json=PAYLOAD) as resp:
            text = await resp.text()
            print(f"HTTP {resp.status}")
            if resp.status != 200:
                try:
                    err = json.loads(text)
                    detail = err.get("detail", text)
                    print(f"Error: {detail}")
                except Exception:
                    print(text[:500])
                sys.exit(1)
            data = json.loads(text)
            print(f"OK presentation_id={data.get('presentation_id') or data.get('id')}")
            print(f"path={data.get('path')}, edit_path={data.get('edit_path')}")


if __name__ == "__main__":
    asyncio.run(main())
