# src/adapters/outbound/persistence/models/taskboard.py
from sqlalchemy import Column as SAColumn, Text, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from uuid import uuid4

from .base import Base, AuditMixin, MixinAccessSettings


class Taskboard(AuditMixin, MixinAccessSettings, Base):
    __tablename__ = 'taskboards'

    owner_id = SAColumn(BigInteger, ForeignKey('users.id'), nullable=False)
    project_id = SAColumn(BigInteger, ForeignKey('projects.id', ondelete='SET NULL'), nullable=True)
    title = SAColumn(Text, nullable=False)
    description = SAColumn(Text, nullable=True)
    position = SAColumn(JSONB, nullable=False, default=list)  # порядок колонок

    owner = relationship(
        'User',
        back_populates='taskboards',
        foreign_keys=[owner_id]
    )

    project = relationship(
        'Project',
        back_populates='taskboards',
        foreign_keys=[project_id]
    )
    columns = relationship(
        'Column',
        back_populates='taskboard',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )

    def __init__(self, **kwargs):
        kwargs.setdefault('access_link', uuid4())
        kwargs.setdefault('position', [])
        super().__init__(**kwargs)
