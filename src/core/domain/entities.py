# src/core/domain/entities.py
"""
Domain layer: core entities and value objects
"""
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import List, Optional, Any
from core.domain.value_objects.permission_key import PermissionKey
from core.domain.value_objects.entity_type import EntityType
from core.domain.value_objects.event_type import EventType


@dataclass
class User:
    id: int
    username: str
    email: str
    is_blocked: bool
    created_at: datetime


@dataclass
class Project:
    id: int
    owner_id: int
    title: str
    is_private: bool
    access_link: UUID
    created_at: datetime
    deleted_at: Optional[datetime] = None


@dataclass
class Taskboard:
    id: int
    owner_id: int
    project_id: Optional[int]
    title: str
    description: Optional[str]
    is_private: bool
    access_link: UUID
    position: Any
    created_at: datetime
    deleted_at: Optional[datetime] = None
    column_ids: List[int] = ()


@dataclass
class Column:
    id: int
    taskboard_id: int
    title: str
    position: Any
    created_at: datetime
    deleted_at: Optional[datetime] = None


@dataclass
class Task:
    id: int
    column_id: int
    title: str
    position: Any                # порядок чек-листов
    start_at: Optional[datetime]
    due_at: Optional[datetime]
    metadata_json: Optional[Any]
    created_at: datetime
    deleted_at: Optional[datetime] = None


@dataclass
class Checklist:
    id: int
    task_id: int
    title: str
    position: Any
    start_at: Optional[datetime]
    due_at: Optional[datetime]
    created_at: datetime
    deleted_at: Optional[datetime] = None
    item_ids: List[int] = ()


@dataclass
class CheckItem:
    id: int
    checklist_id: int
    title: str
    is_checked: bool
    created_at: datetime
    deleted_at: Optional[datetime] = None


@dataclass
class ProjectMember:
    id: int
    user_id: int
    project_id: int
    invited_at: datetime
    permissions: List[PermissionKey]


@dataclass
class ProjectMemberPermission:
    id: int
    project_member_id: int
    permission_key: PermissionKey


@dataclass
class HistoryRecord:
    id: int
    entity_type: EntityType
    record_id: int
    comment: str
    event_timestamp: datetime
    payload: Any


@dataclass
class EventLogRecord:
    id: int
    event_type: EventType
    comment: str
    event_timestamp: datetime
    payload: Any


# Value objects can include e.g., Email, PasswordHash, etc.
@dataclass(frozen=True)
class EmailAddress:
    value: str

    def __post_init__(self):
        assert '@' in self.value, 'Invalid email'
