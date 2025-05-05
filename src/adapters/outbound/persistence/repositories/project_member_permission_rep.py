# src/adapters/outbound/persistence/repositories/project_member_permission_rep.py
from typing import List
from sqlalchemy.orm import Session
from ...models.project_member_permission import ProjectMemberPermission
from .base_rep import SQLAlchemyBaseRepository


class SQLAlchemyProjectMemberPermissionRepository(
        SQLAlchemyBaseRepository[ProjectMemberPermission]):

    def __init__(self, session: Session):
        super().__init__(session, ProjectMemberPermission)

    def list_by_member(self, member_id: int) -> List[ProjectMemberPermission]:
        return self.session.query(ProjectMemberPermission)\
                   .filter_by(project_member_id=member_id, deleted_at=None)\
                   .all()
