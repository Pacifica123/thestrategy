from typing import Type, Callable, Any
from sqlalchemy.orm import Session
import pkgutil
import importlib
from sqlalchemy.orm import Mapper
from src.adapters.outbound.persistence.repositories.base_rep import SQLAlchemyBaseRepository
from src.core.usecases.struct.contexts import StructContext
from src.shared.reg_handlers import FETCH_HANDLERS, SEND_HANDLERS
from src.adapters.outbound.persistence.models import Base
from src.core.usecases.opresult import OperationResult, OperationStatus


def generate_crud_handlers(session: Session):
    """
    Автоматически регистрирует CRUD-контексты для всех моделей, унаследованных от Base.
    Контекст именуется:
      - get_all_<model>
      - get_by_id_<model>
      - create_<model>
      - update_<model>
      - delete_<model>
    Где <model> — имя класса модели в нижнем регистре.
    """
    # Ищем все модели
    for mapper in Base.registry.mappers:              # перебираем все Mapper’ы
        cls = mapper.class_                            # достаём класс модели
        if not hasattr(cls, '__tablename__'):          # фильтруем “чистые” классы
            continue
        model_name = cls.__name__.lower()
        repo = SQLAlchemyBaseRepository(session, cls)
        # GET ALL
        ctx_all = f"get_all_{model_name}"
        FETCH_HANDLERS[ctx_all] = lambda filters, repo=repo: OperationResult(
            OperationStatus.SUCCESS,
            data=repo.get_all()
        )

        # GET BY ID
        ctx_by_id = f"get_by_id_{model_name}"
        FETCH_HANDLERS[ctx_by_id] = lambda filters, repo=repo: _fetch_by_id(filters, repo)

        # CREATE
        send_ctx_create = f"create_{model_name}"
        SEND_HANDLERS[send_ctx_create] = lambda payload, repo=repo: _send_create(payload, repo)

        # UPDATE
        send_ctx_update = f"update_{model_name}"
        SEND_HANDLERS[send_ctx_update] = lambda payload, repo=repo: _send_update(payload, repo)

        # DELETE
        send_ctx_delete = f"delete_{model_name}"
        SEND_HANDLERS[send_ctx_delete] = lambda payload, repo=repo: _send_delete(payload, repo)


def _fetch_by_id(filters: dict, repo: SQLAlchemyBaseRepository) -> OperationResult:
    id_ = filters.get('id')
    if id_ is None:
        return OperationResult(OperationStatus.VALIDATION_ERROR, message='Missing id')
    obj = repo.get_by_id(id_)
    return OperationResult(OperationStatus.SUCCESS, data=obj)


def _send_create(payload: dict, repo: SQLAlchemyBaseRepository) -> OperationResult:
    try:
        obj = repo.create(**payload)
        return OperationResult(OperationStatus.SUCCESS, data=obj)
    except Exception as e:
        return OperationResult(OperationStatus.DATABASE_ERROR, message=str(e))


def _send_update(payload: dict, repo: SQLAlchemyBaseRepository) -> OperationResult:
    id_ = payload.get('id')
    if id_ is None:
        return OperationResult(OperationStatus.VALIDATION_ERROR, message='Missing id')
    kwargs = {k: v for k, v in payload.items() if k != 'id'}
    try:
        obj = repo.update(id_, **kwargs)
        return OperationResult(OperationStatus.SUCCESS, data=obj)
    except Exception as e:
        return OperationResult(OperationStatus.DATABASE_ERROR, message=str(e))


def _send_delete(payload: dict, repo: SQLAlchemyBaseRepository) -> OperationResult:
    id_ = payload.get('id')
    if id_ is None:
        return OperationResult(OperationStatus.VALIDATION_ERROR, message='Missing id')
    try:
        repo.delete(id_)
        return OperationResult(OperationStatus.SUCCESS, message='Deleted')
    except Exception as e:
        return OperationResult(OperationStatus.DATABASE_ERROR, message=str(e))
