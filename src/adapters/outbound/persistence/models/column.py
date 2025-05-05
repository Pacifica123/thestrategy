# src/adapters/outbound/persistence/models/column.py
from sqlalchemy import Column as SAColumn, Text, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from .base import Base, AuditMixin


class Column(AuditMixin, Base):
    __tablename__ = 'columns'

    taskboard_id = SAColumn(BigInteger, ForeignKey('taskboards.id', ondelete='CASCADE'), nullable=False)
    title = SAColumn(Text, nullable=False)
    position = SAColumn(JSONB, nullable=False, default=list)  # порядок задач

    taskboard = relationship(
        'Taskboard',
        back_populates='columns',
        foreign_keys=[taskboard_id]
    )
    tasks = relationship(
        'Task',
        back_populates='column',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )
