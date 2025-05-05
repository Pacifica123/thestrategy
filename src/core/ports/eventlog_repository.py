# src/core/ports/eventlog_repository.py
from typing import Protocol, List, Any, Optional
from core.domain.entities import EventLogRecord as ER
from core.domain.value_objects.event_type import EventType


class EventLogRepository(Protocol):
    def get_by_id(self, id: int) -> Optional[ER]: ...
    def list_by_type(self, event_type: EventType) -> List[ER]: ...

    def create(self,
               event_type: EventType,
               comment: str,
               payload: Any
              ) -> ER: ...
