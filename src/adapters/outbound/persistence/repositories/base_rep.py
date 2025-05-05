# src/adapters/outbound/persistence/repositories/base_rep.py
from sqlalchemy.orm import Session
from src.core.ports.base_repository import BaseRepository
from typing import TypeVar


T = TypeVar('T')


class SQLAlchemyBaseRepository(BaseRepository[T]):
    def __init__(self, session: Session, model_cls: type[T]):
        self.session = session
        self.model_cls = model_cls

    def get_all(self) -> list[T]:
        return self.session.query(self.model_cls).all()

    def get_by_id(self, id: int) -> T:
        return self.session.get(self.model_cls, id)

    def create(self, **kwargs) -> T:
        obj = self.model_cls(**kwargs)
        self.session.add(obj)
        self.session.commit()
        return obj

    def update(self, id: int, **kwargs) -> T:
        obj = self.get_by_id(id)
        for k, v in kwargs.items(): setattr(obj, k, v)
        self.session.commit()
        return obj

    def delete(self, id: int) -> None:
        obj = self.get_by_id(id)
        self.session.delete(obj)
        self.session.commit()
