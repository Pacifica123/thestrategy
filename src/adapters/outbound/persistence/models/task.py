# src/adapters/outbound/persistence/models/task.py
from sqlalchemy import Column as SAColumn, Text, ForeignKey, BigInteger, Index
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.orm import relationship

from .base import Base, AuditMixin


class Task(AuditMixin, Base):
    __tablename__ = 'tasks'
    __table_args__ = (
        Index('ix_tasks_due_at', 'due_at'),
        Index('ix_tasks_column_due', 'column_id', 'due_at'),
    )

    column_id = SAColumn(BigInteger, ForeignKey('columns.id', ondelete='CASCADE'), nullable=False)
    title = SAColumn(Text, nullable=False)
    position = SAColumn(JSONB, nullable=False, default=list)  # порядок чек-листов
    start_at = SAColumn(TIMESTAMP, nullable=True)
    due_at = SAColumn(TIMESTAMP, nullable=True)
    metadata_json = SAColumn(JSONB, nullable=True)

    column = relationship(
        'Column',
        back_populates='tasks',
        foreign_keys=[column_id]
    )
    checklists = relationship(
        'Checklist',
        back_populates='task',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )
