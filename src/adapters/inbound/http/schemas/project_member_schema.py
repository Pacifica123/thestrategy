# src/adapters/inbound/http/schemas/project_member_schema.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from core.domain.value_objects.permission_key import PermissionKey


class ProjectMemberCreateSchema(BaseModel):
    user_id: int
    project_id: int
    initial_permissions: Optional[List[PermissionKey]] = []


class ProjectMemberReadSchema(BaseModel):
    id: int
    user_id: int
    project_id: int
    invited_at: datetime
    permissions: List[PermissionKey]

    class Config:
        orm_mode = True
