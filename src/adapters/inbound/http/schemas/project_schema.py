# src/adapters/inbound/http/schemas/project_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class ProjectCreateSchema(BaseModel):
    owner_id: int
    title: str
    is_private: bool = True
    access_link: Optional[UUID] = None      # можно передать готовую ссылку
    password_hash: Optional[str] = None     # для доступа по паролю


class ProjectReadSchema(BaseModel):
    id: int
    owner_id: int
    title: str
    is_private: bool
    access_link: UUID
    created_at: datetime

    class Config:
        orm_mode = True
