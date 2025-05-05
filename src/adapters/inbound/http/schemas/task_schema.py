# src/adapters/inbound/http/schemas/task_schema.py
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class TaskCreateSchema(BaseModel):
    column_id: int
    title: str
    position: Any            # JSON-порядок чек-листов внутри задачи
    start_at: Optional[datetime] = None
    due_at: Optional[datetime] = None
    metadata_json: Optional[Any] = None  # произвольная JSON-структура


class TaskReadSchema(BaseModel):
    id: int
    column_id: int
    title: str
    position: Any
    start_at: Optional[datetime]
    due_at: Optional[datetime]
    metadata_json: Optional[Any]
    created_at: datetime

    class Config:
        orm_mode = True
