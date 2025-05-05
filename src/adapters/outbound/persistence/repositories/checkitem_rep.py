# src/adapters/outbound/persistence/repositories/checkitem_rep.py
from typing import List
from sqlalchemy.orm import Session

from ...models.checkitem import CheckItem
from .base_rep import SQLAlchemyBaseRepository


class SQLAlchemyCheckItemRepository(SQLAlchemyBaseRepository[CheckItem]):
    def __init__(self, session: Session):
        super().__init__(session, CheckItem)

    def list_by_checklist(self, checklist_id: int) -> List[CheckItem]:
        return (
            self.session
                .query(CheckItem)
                .filter_by(checklist_id=checklist_id, deleted_at=None)
                .all()
        )
