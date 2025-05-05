'''
общая база: Base = declarative_base(), audit-миксин
'''
from datetime import datetime
from sqlalchemy import Column, BigInteger, DateTime, ForeignKey, String, Boolean
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class AuditMixin:
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_by_id = Column(BigInteger, ForeignKey('users.id'), nullable=True)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    updated_by_id = Column(BigInteger, ForeignKey('users.id'), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by_id = Column(BigInteger, ForeignKey('users.id'), nullable=True)
    deleted_by_username = Column(String, nullable=True)


class MixinAccessSettings:
    access_link = Column(UUID(as_uuid=True), unique=True, nullable=False)
    password_hash = Column(String, nullable=True)
    is_private = Column(Boolean, nullable=False, default=True)
