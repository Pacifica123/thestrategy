# src/adapters/outbound/persistence/repositories/column_rep.py
from typing import List
from sqlalchemy.orm import Session
from ...models.column import Column as ColumnModel
from .base_rep import SQLAlchemyBaseRepository


class SQLAlchemyColumnRepository(SQLAlchemyBaseRepository[ColumnModel]):
    def __init__(self, session: Session):
        super().__init__(session, ColumnModel)

    def list_by_taskboard(self, taskboard_id: int) -> List[ColumnModel]:
        return (
            self.session
                .query(ColumnModel)
                .filter_by(taskboard_id=taskboard_id, deleted_at=None)
                .order_by(ColumnModel.id)  # если нужен стабильный порядок
                .all()
        )
