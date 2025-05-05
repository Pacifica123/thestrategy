# src/adapters/outbound/persistence/repositories/factory.py
from sqlalchemy.orm import Session

from .base_rep import SQLAlchemyBaseRepository
from .decorators import HistoryLogger
from ...models.history import History
from src.core.domain.value_objects.entity_type import EntityType
from typing import Callable


def make_repo_with_history(
    session: Session,
    model_cls: type,
    entity_type: EntityType,
    user_context: Callable[[], dict]
):
    base_repo = SQLAlchemyBaseRepository(session, model_cls)
    history_repo = SQLAlchemyBaseRepository(session, History)
    # обёртка, которая логирует create/update/delete
    return HistoryLogger(
        base_repo,
        history_repo,
        entity_type=entity_type,
        user_context=user_context
    )
