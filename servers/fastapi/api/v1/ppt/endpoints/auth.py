"""Authentication REST API — register, login, profile, user management."""

from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Annotated, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.sql.user import UserModel
from services.database import get_async_session
from utils.auth import hash_password, verify_password, create_token, get_current_user, require_admin

AUTH_ROUTER = APIRouter(prefix="/auth", tags=["Authentication"])


@AUTH_ROUTER.post("/register", summary="Register a new user")
async def register(
    username: Annotated[str, Body()],
    password: Annotated[str, Body()],
    email: Annotated[Optional[str], Body()] = None,
    sql_session: AsyncSession = Depends(get_async_session),
):
    existing = await sql_session.scalars(select(UserModel).where(UserModel.username == username))
    if existing.first():
        raise HTTPException(status_code=400, detail="Username already exists")

    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    user = UserModel(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        role="user",
    )
    sql_session.add(user)
    await sql_session.commit()
    await sql_session.refresh(user)

    token = create_token(str(user.id), user.role)
    return {"token": token, "user": {"id": str(user.id), "username": user.username, "role": user.role}}


@AUTH_ROUTER.post("/login", summary="Login with username and password")
async def login(
    username: Annotated[str, Body()],
    password: Annotated[str, Body()],
    sql_session: AsyncSession = Depends(get_async_session),
):
    result = await sql_session.scalars(select(UserModel).where(UserModel.username == username))
    user = result.first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled")

    token = create_token(str(user.id), user.role)
    return {"token": token, "user": {"id": str(user.id), "username": user.username, "role": user.role}}


@AUTH_ROUTER.get("/me", summary="Get current user profile")
async def get_profile(user: Optional[UserModel] = Depends(get_current_user)):
    if user is None:
        return {"auth_enabled": False, "message": "Authentication is disabled (set AUTH_ENABLED=true to enable)"}
    return {"id": str(user.id), "username": user.username, "email": user.email, "role": user.role}


@AUTH_ROUTER.get("/users", summary="List all users (admin only)")
async def list_users(
    admin: Optional[UserModel] = Depends(require_admin),
    sql_session: AsyncSession = Depends(get_async_session),
):
    result = await sql_session.scalars(select(UserModel))
    users = result.all()
    return [{"id": str(u.id), "username": u.username, "email": u.email, "role": u.role, "is_active": u.is_active} for u in users]


@AUTH_ROUTER.post("/users/{user_id}/toggle-active", summary="Enable/disable user (admin only)")
async def toggle_user_active(
    user_id: str,
    admin: Optional[UserModel] = Depends(require_admin),
    sql_session: AsyncSession = Depends(get_async_session),
):
    import uuid as _uuid
    user = await sql_session.get(UserModel, _uuid.UUID(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = not user.is_active
    sql_session.add(user)
    await sql_session.commit()
    return {"id": str(user.id), "is_active": user.is_active}


@AUTH_ROUTER.post("/users/{user_id}/set-role", summary="Set user role (admin only)")
async def set_user_role(
    user_id: str,
    role: Annotated[str, Body(embed=True)],
    admin: Optional[UserModel] = Depends(require_admin),
    sql_session: AsyncSession = Depends(get_async_session),
):
    if role not in ("admin", "user"):
        raise HTTPException(status_code=400, detail="Role must be 'admin' or 'user'")
    import uuid as _uuid
    user = await sql_session.get(UserModel, _uuid.UUID(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = role
    sql_session.add(user)
    await sql_session.commit()
    return {"id": str(user.id), "role": user.role}
