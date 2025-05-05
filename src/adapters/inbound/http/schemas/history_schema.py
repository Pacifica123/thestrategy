# src/adapters/inbound/http/schemas/history_schema.py
from pydantic import BaseModel
from datetime import datetime
from typing import Any
from core.domain.value_objects.entity_type import EntityType


class HistoryCreateSchema(BaseModel):
    entity_type: EntityType
    record_id: int
    comment: str
    payload: Any


class HistoryReadSchema(BaseModel):
    id: int
    entity_type: EntityType
    record_id: int
    comment: str
    event_timestamp: datetime
    payload: Any

    class Config:
        orm_mode = True
