# src/adapters/outbound/persistence/models/project.py
from sqlalchemy import Column, Text, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from uuid import uuid4

from .base import AuditMixin, MixinAccessSettings, Base


class Project(AuditMixin, MixinAccessSettings, Base):
    __tablename__ = 'projects'

    owner_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    title = Column(Text, nullable=False)

    owner = relationship(
        'User',
        back_populates='projects',
        foreign_keys=[owner_id]
    )
    taskboards = relationship(
        'Taskboard',
        back_populates='project',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )
    members = relationship("ProjectMember", back_populates="project")

    def __init__(self, **kwargs):
        # если не передали access_link, генерируем его
        kwargs.setdefault('access_link', uuid4())
        super().__init__(**kwargs)
