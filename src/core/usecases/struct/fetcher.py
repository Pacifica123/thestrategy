'''
 src/core/usecases/struct/fetcher.py
'''
from ..opresult import OperationResult, OperationStatus
from .contexts import StructContext


class StructFetcher:
    def fetch(self, context: str, filters: dict) -> OperationResult:
        # TODO : проверка наличия context и валидности filters
        match context:
            case StructContext.TEST_WORK:
                return self._test_work(filters)
            case _:
                return OperationResult(
                    OperationStatus.NOT_REALIZED,
                    message=f"Unknown case: {context}")

    def _test_work(self, filters: dict) -> OperationResult:
        return OperationResult(OperationStatus.SUCCESS, data=[])
