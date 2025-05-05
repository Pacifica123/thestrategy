# src/adapters/inbound/http/schemas/checklist_schema.py
from pydantic import BaseModel
from typing import Optional, Any, List
from datetime import datetime


class ChecklistCreateSchema(BaseModel):
    task_id: int
    title: str
    position: Any                    # JSON-порядок чек-боксов внутри чек-листа
    start_at: Optional[datetime] = None
    due_at: Optional[datetime] = None


class ChecklistReadSchema(BaseModel):
    id: int
    task_id: int
    title: str
    position: Any
    start_at: Optional[datetime]
    due_at: Optional[datetime]
    created_at: datetime
    item_ids: List[int] = []

    class Config:
        orm_mode = True
