# src/adapters/inbound/http/schemas/column_schema.py
from pydantic import BaseModel
from typing import Any
from datetime import datetime


class ColumnCreateSchema(BaseModel):
    taskboard_id: int
    title: str
    position: Any   # JSON-структура порядка задач внутри колонки


class ColumnReadSchema(BaseModel):
    id: int
    taskboard_id: int
    title: str
    position: Any
    created_at: datetime

    class Config:
        orm_mode = True
