"""User model for authentication."""

import uuid
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class UserModel(SQLModel, table=True):
    __tablename__ = "users"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: Optional[str] = Field(default=None)
    hashed_password: str
    role: str = Field(default="user")  # "admin" | "user"
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
