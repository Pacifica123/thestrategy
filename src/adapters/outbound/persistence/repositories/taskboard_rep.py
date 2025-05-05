# src/adapters/outbound/persistence/repositories/taskboard_rep.py
from typing import List, Optional
from sqlalchemy.orm import Session
from ...models.taskboard import Taskboard
from .base_rep import SQLAlchemyBaseRepository


class SQLAlchemyTaskboardRepository(SQLAlchemyBaseRepository[Taskboard]):
    def __init__(self, session: Session):
        super().__init__(session, Taskboard)

    def list_by_owner(self, owner_id: int) -> List[Taskboard]:
        return (
            self.session
                .query(Taskboard)
                .filter_by(owner_id=owner_id, deleted_at=None)
                .all()
        )

    def list_by_project(self, project_id: int) -> List[Taskboard]:
        return (
            self.session
                .query(Taskboard)
                .filter_by(project_id=project_id, deleted_at=None)
                .all()
        )

    def get_by_access_link(self, link: str) -> Optional[Taskboard]:
        return (
            self.session
                .query(Taskboard)
                .filter_by(access_link=link, deleted_at=None)
                .one_or_none()
        )
