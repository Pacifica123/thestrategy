# src/adapters/outbound/persistence/repositories/checklist_rep.py
from typing import List
from sqlalchemy.orm import Session

from ...models.checklist import Checklist
from .base_rep import SQLAlchemyBaseRepository


class SQLAlchemyChecklistRepository(SQLAlchemyBaseRepository[Checklist]):
    def __init__(self, session: Session):
        super().__init__(session, Checklist)

    def list_by_task(self, task_id: int) -> List[Checklist]:
        return (
            self.session
                .query(Checklist)
                .filter_by(task_id=task_id, deleted_at=None)
                .all()
        )
