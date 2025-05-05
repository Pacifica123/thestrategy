# src/core/ports/task_repository.py
from typing import Protocol, List, Optional, Any
from ..domain.entities import Task as TaskEntity


class TaskRepository(Protocol):
    def get_by_id(self, task_id: int) -> Optional[TaskEntity]: ...
    def list_by_column(self, column_id: int) -> List[TaskEntity]: ...

    def create(self,
               column_id: int,
               title: str,
               position: Any,
               start_at: Optional[str] = None,
               due_at: Optional[str] = None,
               metadata_json: Optional[Any] = None
              ) -> TaskEntity: ...

    def update(self, task_id: int, **kwargs) -> TaskEntity: ...
    def delete(self, task_id: int) -> None: ...
    def list_due_before(self, when: str) -> List[TaskEntity]: ...
