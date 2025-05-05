# src/core/ports/history_repository.py
from typing import Protocol, List, Optional, Any
from core.domain.entities import HistoryRecord as HR
from core.domain.value_objects.entity_type import EntityType


class HistoryRepository(Protocol):
    def get_by_id(self, id: int) -> Optional[HR]: ...

    def list_by_entity(self,
                       entity_type: EntityType,
                       record_id: Optional[int] = None
                      ) -> List[HR]: ...

    def create(self,
               entity_type: EntityType,
               record_id: int,
               comment: str,
               payload: Any
              ) -> HR: ...
