# src/adapters/outbound/persistence/models/project_member.py
from sqlalchemy import Column as SAColumn, BigInteger, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base, AuditMixin


class ProjectMember(AuditMixin, Base):
    __tablename__ = 'project_members'

    user_id = SAColumn(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    project_id = SAColumn(BigInteger, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    invited_at = SAColumn(DateTime, nullable=False, server_default=func.now())

    user = relationship(
        'User',
        back_populates='members',
        foreign_keys=[user_id]
    )
    project = relationship(
        'Project',
        back_populates='members',
        foreign_keys=[project_id]
    )
    permissions = relationship(
        'ProjectMemberPermission',
        back_populates='member',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )
