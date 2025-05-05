# src/core/ports/checkitem_repository.py
from typing import Protocol, List, Optional
from ..domain.entities import CheckItem as CI


class CheckItemRepository(Protocol):
    def get_by_id(self, checkitem_id: int) -> Optional[CI]: ...
    def list_by_checklist(self, checklist_id: int) -> List[CI]: ...

    def create(self,
               checklist_id: int,
               title: str,
               is_checked: bool = False
              ) -> CI: ...

    def update(self, checkitem_id: int, **kwargs) -> CI: ...
    def delete(self, checkitem_id: int) -> None: ...
