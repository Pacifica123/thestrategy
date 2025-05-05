# src/core/ports/taskboard_repository.py
from typing import Protocol, List, Optional, Any
from ..domain.entities import Taskboard as TBEntity


class TaskboardRepository(Protocol):
    def get_by_id(self, taskboard_id: int) -> Optional[TBEntity]: ...
    def list_by_owner(self, owner_id: int) -> List[TBEntity]: ...
    def list_by_project(self, project_id: int) -> List[TBEntity]: ...

    def create(self,
               owner_id: int,
               title: str,
               project_id: Optional[int] = None,
               description: Optional[str] = None,
               is_private: bool = True,
               access_link: Optional[str] = None,
               password_hash: Optional[str] = None,
               position: Any = None
             ) -> TBEntity: ...

    def update(self, taskboard_id: int, **kwargs) -> TBEntity: ...
    def delete(self, taskboard_id: int) -> None: ...
    def get_by_access_link(self, link: str) -> Optional[TBEntity]: ...
