# src/adapters/outbound/persistence/repositories/project_rep.py
from typing import List, Optional
from sqlalchemy.orm import Session

from ...models.project import Project
from .base_rep import SQLAlchemyBaseRepository


class SQLAlchemyProjectRepository(SQLAlchemyBaseRepository[Project]):
    def __init__(self, session: Session):
        super().__init__(session, Project)

    def list_by_owner(self, owner_id: int) -> List[Project]:
        return (
            self.session
                .query(Project)
                .filter_by(owner_id=owner_id, deleted_at=None)
                .all()
        )

    def get_by_access_link(self, link: str) -> Optional[Project]:
        return (
            self.session
                .query(Project)
                .filter_by(access_link=link, deleted_at=None)
                .one_or_none()
        )
