# src/adapters/inbound/http/schemas/taskboard_schema.py
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID


class TaskboardCreateSchema(BaseModel):
    owner_id: int
    project_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    is_private: bool = True
    access_link: Optional[UUID] = None
    password_hash: Optional[str] = None
    position: Any   # JSON-структура порядка колонок


class TaskboardReadSchema(BaseModel):
    id: int
    owner_id: int
    project_id: Optional[int]
    title: str
    description: Optional[str]
    is_private: bool
    access_link: UUID
    created_at: datetime
    position: Any
    column_ids: List[int] = []

    class Config:
        orm_mode = True
