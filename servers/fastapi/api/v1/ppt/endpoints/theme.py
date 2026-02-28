"""Theme and footer REST API — replaces Next.js /api/theme and /api/footer."""

import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Annotated, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.sql.theme import ThemeModel, FooterModel
from services.database import get_async_session

THEME_ROUTER = APIRouter(prefix="/theme", tags=["Theme"])


@THEME_ROUTER.get("/", summary="Get theme for user")
async def get_theme(
    userId: str = "default",
    sql_session: AsyncSession = Depends(get_async_session),
):
    result = await sql_session.scalars(
        select(ThemeModel).where(ThemeModel.user_id == userId)
    )
    theme = result.first()
    if not theme:
        return {"userId": userId, "themeData": {}}
    try:
        data = json.loads(theme.theme_data)
    except Exception:
        data = {}
    return {"userId": userId, "themeData": data}


@THEME_ROUTER.post("/", summary="Save theme for user")
async def save_theme(
    userId: Annotated[str, Body()] = "default",
    themeData: Annotated[dict, Body()] = {},
    sql_session: AsyncSession = Depends(get_async_session),
):
    result = await sql_session.scalars(
        select(ThemeModel).where(ThemeModel.user_id == userId)
    )
    theme = result.first()
    data_str = json.dumps(themeData, ensure_ascii=False)

    if theme:
        theme.theme_data = data_str
        theme.updated_at = datetime.utcnow()
    else:
        theme = ThemeModel(user_id=userId, theme_data=data_str)
    sql_session.add(theme)
    await sql_session.commit()
    return {"success": True}


FOOTER_ROUTER = APIRouter(prefix="/footer", tags=["Footer"])


@FOOTER_ROUTER.get("/", summary="Get footer properties for user")
async def get_footer(
    userId: str = "default",
    sql_session: AsyncSession = Depends(get_async_session),
):
    result = await sql_session.scalars(
        select(FooterModel).where(FooterModel.user_id == userId)
    )
    footer = result.first()
    if not footer:
        return {"userId": userId, "properties": {}}
    try:
        data = json.loads(footer.properties)
    except Exception:
        data = {}
    return {"userId": userId, "properties": data}


@FOOTER_ROUTER.post("/", summary="Save footer properties for user")
async def save_footer(
    userId: Annotated[str, Body()] = "default",
    properties: Annotated[dict, Body()] = {},
    sql_session: AsyncSession = Depends(get_async_session),
):
    result = await sql_session.scalars(
        select(FooterModel).where(FooterModel.user_id == userId)
    )
    footer = result.first()
    data_str = json.dumps(properties, ensure_ascii=False)

    if footer:
        footer.properties = data_str
        footer.updated_at = datetime.utcnow()
    else:
        footer = FooterModel(user_id=userId, properties=data_str)
    sql_session.add(footer)
    await sql_session.commit()
    return {"success": True}
