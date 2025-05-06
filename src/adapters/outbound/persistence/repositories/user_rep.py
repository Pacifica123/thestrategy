# src/adapters/outbound/persistence/repositories/user_rep.py
from sqlalchemy.orm import Session
from src.core.ports.base_repository import BaseRepository
from src.adapters.outbound.persistence.models.user import User
from src.adapters.outbound.persistence.repositories.base_rep import SQLAlchemyBaseRepository
from src.core.usecases.struct.contexts import StructContext


class SQLAlchemyUserRepository(SQLAlchemyBaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(session, User)

    def get_by_username(self, username: str) -> User:
        return self.session.query(User).filter_by(username=username).one_or_none()

    def get_by_email(self, email: str) -> User:
        return self.session.query(User).filter_by(email=email).one_or_none()

    def block(self, user_id: int) -> None:
        user = self.get_by_id(user_id)
        if user:
            user.is_blocked = True
            self.session.commit()
