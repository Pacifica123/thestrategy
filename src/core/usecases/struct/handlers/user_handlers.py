# src/core/usecases/struct/handlers/user_handlers.py
from src.shared.reg_handlers import register_fetch, register_send
from src.core.usecases.struct.contexts import StructContext
from src.core.usecases.opresult import OperationResult, OperationStatus
from src.adapters.outbound.persistence.repositories.user_rep import SQLAlchemyUserRepository
from src.shared.extensions import db


@register_fetch(StructContext.GET_USER_BY_USERNAME)
def fetch_user_by_username(filters: dict) -> OperationResult:
    username = filters.get("username")
    if not username:
        return OperationResult(OperationStatus.VALIDATION_ERROR, message="Missing 'username'")
    repo = SQLAlchemyUserRepository(db.session)
    user = repo.get_by_username(username)
    return OperationResult(OperationStatus.SUCCESS, data=user)


@register_send(StructContext.BLOCK_USER)
def send_block_user(payload: dict) -> OperationResult:
    user_id = payload.get("user_id")
    if not user_id:
        return OperationResult(OperationStatus.VALIDATION_ERROR, message="Missing 'user_id'")
    repo = SQLAlchemyUserRepository(session)
    repo.block(user_id)
    return OperationResult(OperationStatus.SUCCESS, message="User blocked")
