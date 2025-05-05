# src/adapters/outbound/persistence/models/eventlog.py
from sqlalchemy import Column as SAColumn, BigInteger, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from src.core.domain.value_objects.event_type import EventType

from .base import Base


class EventLog(Base):
    __tablename__ = 'eventlogs'

    id              = SAColumn(BigInteger, primary_key=True, autoincrement=True)
    event_type      = SAColumn(Enum(EventType, name='event_type_enum'), nullable=False)
    comment         = SAColumn(Text, nullable=False)
    event_timestamp = SAColumn(DateTime, nullable=False, server_default=func.now())
    payload         = SAColumn(JSONB, nullable=True)
