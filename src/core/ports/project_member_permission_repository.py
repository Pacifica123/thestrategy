# src/core/ports/project_member_permission_repository.py
from typing import Protocol, List
from core.domain.entities import ProjectMemberPermission as PMP
from core.domain.value_objects.permission_key import PermissionKey


class ProjectMemberPermissionRepository(Protocol):
    def list_by_member(self, member_id: int) -> List[PMP]: ...
    def add(self, member_id: int, key: PermissionKey) -> PMP: ...
    def remove(self, permission_id: int) -> None: ...
