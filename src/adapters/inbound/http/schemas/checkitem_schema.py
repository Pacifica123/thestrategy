# src/adapters/inbound/http/schemas/checkitem_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CheckItemCreateSchema(BaseModel):
    checklist_id: int
    title: str
    is_checked: Optional[bool] = False


class CheckItemReadSchema(BaseModel):
    id: int
    checklist_id: int
    title: str
    is_checked: bool
    created_at: datetime

    class Config:
        orm_mode = True
