'''
 src/adapters/outbound/persistence/models/user.py
'''
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from .base import Base, AuditMixin
from .project import Project
from .project_member import ProjectMember


class User(AuditMixin, Base):
    __tablename__ = 'users'

    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    password_updated_at = Column(DateTime, nullable=True)
    is_blocked = Column(Boolean, nullable=False, default=False)

    # relationships
    projects = relationship(
        'Project',
        back_populates='owner',
        foreign_keys=[Project.owner_id]
    )
    taskboards = relationship(
        'Taskboard',
        back_populates='owner',
        foreign_keys='Taskboard.owner_id'
    )
    members = relationship(
        'ProjectMember',
        back_populates='user',
        foreign_keys=[ProjectMember.user_id],
        cascade='all, delete-orphan'
    )
