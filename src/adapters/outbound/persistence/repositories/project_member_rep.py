# src/adapters/outbound/persistence/repositories/project_member_rep.py
from typing import List, Optional
from sqlalchemy.orm import Session
from ...models.project_member import ProjectMember
from .base_rep import SQLAlchemyBaseRepository


class SQLAlchemyProjectMemberRepository(SQLAlchemyBaseRepository[ProjectMember]):
    def __init__(self, session: Session):
        super().__init__(session, ProjectMember)

    def list_by_project(self, project_id: int) -> List[ProjectMember]:
        return self.session.query(ProjectMember)\
                   .filter_by(project_id=project_id, deleted_at=None)\
                   .all()

    def list_by_user(self, user_id: int) -> List[ProjectMember]:
        return self.session.query(ProjectMember)\
                   .filter_by(user_id=user_id, deleted_at=None)\
                   .all()
