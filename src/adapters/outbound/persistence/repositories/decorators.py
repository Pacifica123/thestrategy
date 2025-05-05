# src/adapters/outbound/persistence/repositories/decorators.py
'''
 Декораторы к репозиториям
'''
from functools import wraps
from datetime import datetime
from typing import Any, Callable, TypeVar, Generic, Optional, Dict

from core.domain.value_objects.entity_type import EntityType
from ...models.history import History
from .base_rep import SQLAlchemyBaseRepository

T = TypeVar('T')


class HistoryLogger(Generic[T]):
    """
    Декоратор-обёртка для репозиториев, логирующий операции CRUD в таблицу history.
    Usage:
        base_repo = SQLAlchemyBaseRepository(session, Model)
        history_repo = SQLAlchemyBaseRepository(session, History)
        repo = HistoryLogger(base_repo, history_repo, EntityType.MODEL_ENTITY)
    """
    def __init__(
        self,
        repo: SQLAlchemyBaseRepository[T],
        history_repo: SQLAlchemyBaseRepository[History],
        entity_type: EntityType,
        user_context: Optional[Callable[[], Dict[str, Any]]] = None,
    ):
        self._repo = repo
        self._history_repo = history_repo
        self._entity_type = entity_type
        # user_context возвращает словарь với ключами user_id, username
        self._user_context = user_context or (lambda: {})

    def _log(self, action: str, record_id: int, before: Optional[Dict[str, Any]], after: Optional[Dict[str, Any]]):
        context = self._user_context()
        diff = {}
        if before and after:
            for k, new in after.items():
                old = before.get(k)
                if old != new:
                    diff[k] = {'old': old, 'new': new}

        payload = {
            'entity': self._entity_type.value,
            'action': action,
            'changed_by': context,
            'before': before,
            'after': after,
            'diff': diff,
        }
        self._history_repo.create(
            entity_type=self._entity_type,
            record_id=record_id,
            comment=f"{action} on {self._entity_type.name}",
            payload=payload,
        )

    def get_by_id(self, id: int) -> T:
        return self._repo.get_by_id(id)

    def get_all(self) -> list[T]:
        return self._repo.get_all()

    def create(self, **kwargs) -> T:
        obj = self._repo.create(**kwargs)
        after = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
        self._log('create', obj.id, before=None, after=after)
        return obj

    def update(self, id: int, **kwargs) -> T:
        before_obj = self._repo.get_by_id(id)
        before = {c.name: getattr(before_obj, c.name) for c in before_obj.__table__.columns}
        obj = self._repo.update(id, **kwargs)
        after = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
        self._log('update', id, before=before, after=after)
        return obj

    def delete(self, id: int) -> None:
        before_obj = self._repo.get_by_id(id)
        before = {c.name: getattr(before_obj, c.name) for c in before_obj.__table__.columns}
        self._repo.delete(id)
        # запись удаления: after=None
        self._log('delete', id, before=before, after=None)

    # проксирование остальных методов
    def __getattr__(self, name: str) -> Any:
        return getattr(self._repo, name)
