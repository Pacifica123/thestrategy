# src/adapters/outbound/persistence/models/project_member_permission.py
from sqlalchemy import Column as SAColumn, BigInteger, ForeignKey, Enum
from sqlalchemy.orm import relationship

from src.core.domain.value_objects.permission_key import PermissionKey
from .base import Base, AuditMixin


class ProjectMemberPermission(AuditMixin, Base):
    __tablename__ = 'project_member_permissions'

    member_id = SAColumn(
        BigInteger,
        ForeignKey('project_members.id', ondelete='CASCADE'),
        nullable=False,
        name='project_member_id',
    )
    permission_key = SAColumn(
        Enum(PermissionKey, name='permission_key_enum'),
        nullable=False,
    )

    member = relationship(
        'ProjectMember',
        back_populates='permissions',
        foreign_keys=[member_id]
    )
