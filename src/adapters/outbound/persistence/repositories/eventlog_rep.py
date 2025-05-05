# src/adapters/outbound/persistence/repositories/eventlog_rep.py
from typing import List
from sqlalchemy.orm import Session
from ...models.eventlog import EventLog
from .base_rep import SQLAlchemyBaseRepository


class SQLAlchemyEventLogRepository(SQLAlchemyBaseRepository[EventLog]):
    def __init__(self, session: Session):
        super().__init__(session, EventLog)

    def list_by_type(self, event_type) -> List[EventLog]:
        return (
            self.session
                .query(EventLog)
                .filter_by(event_type=event_type)
                .order_by(EventLog.event_timestamp.asc())
                .all()
        )
