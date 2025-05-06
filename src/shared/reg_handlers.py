from typing import Callable
from src.core.usecases.opresult import OperationResult
from src.core.usecases.struct.contexts import StructContext


FETCH_HANDLERS: dict[str, Callable[..., OperationResult]] = {}
SEND_HANDLERS: dict[str, Callable[..., OperationResult]] = {}


def register_fetch(context: str):
    def decorator(fn: Callable[[dict], OperationResult]):
        FETCH_HANDLERS[context] = fn
        return fn
    return decorator


def register_send(context: str):
    def decorator(fn: Callable[[dict], OperationResult]):
        SEND_HANDLERS[context] = fn
        return fn
    return decorator
