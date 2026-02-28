"""Theme and footer models — migrated from Next.js SQLite API."""

from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class ThemeModel(SQLModel, table=True):
    __tablename__ = "themes"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    theme_data: str = Field(default="{}")  # JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class FooterModel(SQLModel, table=True):
    __tablename__ = "footers"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    properties: str = Field(default="{}")  # JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
