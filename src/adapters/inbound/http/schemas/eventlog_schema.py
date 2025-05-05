# src/adapters/inbound/http/schemas/eventlog_schema.py
from pydantic import BaseModel
from datetime import datetime
from typing import Any
from core.domain.value_objects.event_type import EventType


class EventLogCreateSchema(BaseModel):
    event_type: EventType
    comment: str
    payload: Any


class EventLogReadSchema(BaseModel):
    id: int
    event_type: EventType
    comment: str
    event_timestamp: datetime
    payload: Any

    class Config:
        orm_mode = True
