# src/adapters/inbound/http/schemas/permission_schema.py
from pydantic import BaseModel
from core.domain.value_objects.permission_key import PermissionKey


class PermissionCreateSchema(BaseModel):
    project_member_id: int
    permission_key: PermissionKey


class PermissionReadSchema(BaseModel):
    id: int
    project_member_id: int
    permission_key: PermissionKey

    class Config:
        orm_mode = True
