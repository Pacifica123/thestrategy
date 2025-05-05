# src/adapters/outbound/persistence/repositories/history_rep.py
from typing import List
from sqlalchemy.orm import Session
from ...models.history import History
from .base_rep import SQLAlchemyBaseRepository


class SQLAlchemyHistoryRepository(SQLAlchemyBaseRepository[History]):
    def __init__(self, session: Session):
        super().__init__(session, History)

    def list_by_entity(self, entity_type, record_id=None) -> List[History]:
        q = self.session.query(History).filter_by(entity_type=entity_type)
        if record_id is not None:
            q = q.filter_by(record_id=record_id)
        return q.order_by(History.event_timestamp.asc()).all()
