# src/adapters/outbound/persistence/models/checklist.py
from sqlalchemy import Column as SAColumn, Text, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.orm import relationship

from .base import Base, AuditMixin


class Checklist(AuditMixin, Base):
    __tablename__ = 'checklists'

    task_id = SAColumn(BigInteger, ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    title = SAColumn(Text, nullable=False)
    position = SAColumn(JSONB, nullable=False, default=list)   # порядок чекбоксов
    start_at = SAColumn(TIMESTAMP, nullable=True)
    due_at = SAColumn(TIMESTAMP, nullable=True)

    task = relationship('Task', back_populates='checklists')
    items = relationship(
        'CheckItem',
        back_populates='checklist',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )
