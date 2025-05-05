from typing import Protocol, List, Any, Optional
from ..domain.entities import Checklist as CL


class ChecklistRepository(Protocol):
    def get_by_id(self, checklist_id: int) -> Optional[CL]: ...
    def list_by_task(self, task_id: int) -> List[CL]: ...

    def create(self,
               task_id: int,
               title: str,
               position: Any,
               start_at: Optional[str] = None,
               due_at: Optional[str] = None
              ) -> CL: ...

    def update(self, checklist_id: int, **kwargs) -> CL: ...
    def delete(self, checklist_id: int) -> None: ...
