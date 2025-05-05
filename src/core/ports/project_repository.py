# src/core/ports/project_repository.py
from typing import Protocol, List, Optional
from ..domain.entities import Project as ProjectEntity


class ProjectRepository(Protocol):
    def get_by_id(self, project_id: int) -> Optional[ProjectEntity]: ...
    def list_by_owner(self, owner_id: int) -> List[ProjectEntity]: ...

    def create(self,
               owner_id: int,
               title: str,
               is_private: bool = True,
               access_link: Optional[str] = None,
               password_hash: Optional[str] = None
              ) -> ProjectEntity: ...

    def update(self, project_id: int, **kwargs) -> ProjectEntity: ...
    def delete(self, project_id: int) -> None: ...
    def get_by_access_link(self, link: str) -> Optional[ProjectEntity]: ...
