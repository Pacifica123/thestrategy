'''
 src/core/usecases/struct/fetcher.py
'''
from ..opresult import OperationResult, OperationStatus
# from src.core.usecases.struct.contexts import StructContext
from src.shared.reg_handlers import FETCH_HANDLERS


class StructFetcher:
    def fetch(self, context: str, filters: dict) -> OperationResult:
        handler = FETCH_HANDLERS.get(context)
        if not handler:
            return OperationResult(
                OperationStatus.NOT_REALIZED,
                message=f"Неизвестный fetch-контекст: {context}")
        try:
            return handler(filters)
        except Exception as e:
            return OperationResult(OperationStatus.DATABASE_ERROR,
                                   message=str(e))
