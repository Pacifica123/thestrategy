# src/adapters/outbound/persistence/repositories/task_rep.py
from typing import List, Optional
from sqlalchemy.orm import Session

from ...models.task import Task
from .base_rep import SQLAlchemyBaseRepository


class SQLAlchemyTaskRepository(SQLAlchemyBaseRepository[Task]):
    def __init__(self, session: Session):
        super().__init__(session, Task)

    def list_by_column(self, column_id: int) -> List[Task]:
        return (
            self.session
                .query(Task)
                .filter_by(column_id=column_id, deleted_at=None)
                .all()
        )

    def list_due_before(self, when: str) -> List[Task]:
        return (
            self.session
                .query(Task)
                .filter(Task.due_at is not None, Task.due_at <= when, Task.deleted_at is None)
                .all()
        )
