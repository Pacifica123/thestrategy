# src/adapters/outbound/persistence/models/checkitem.py
from sqlalchemy import Column as SAColumn, Text, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from .base import Base, AuditMixin


class CheckItem(AuditMixin, Base):
    __tablename__ = 'checkitems'

    checklist_id = SAColumn(BigInteger, ForeignKey('checklists.id', ondelete='CASCADE'), nullable=False)
    title = SAColumn(Text, nullable=False)
    is_checked = SAColumn(Boolean, nullable=False, default=False)

    checklist = relationship('Checklist', back_populates='items')
