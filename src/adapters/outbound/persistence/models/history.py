# src/adapters/outbound/persistence/models/history.py
from sqlalchemy import Column as SAColumn, BigInteger, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from src.core.domain.value_objects.entity_type import EntityType

from .base import Base


class History(Base):
    __tablename__ = 'history'

    id              = SAColumn(BigInteger, primary_key=True, autoincrement=True)
    entity_type     = SAColumn(Enum(EntityType, name='entity_type_enum'), nullable=False)
    record_id       = SAColumn(BigInteger, nullable=False)
    comment         = SAColumn(Text, nullable=False)
    event_timestamp = SAColumn(DateTime, nullable=False, server_default=func.now())
    payload         = SAColumn(JSONB, nullable=True)
