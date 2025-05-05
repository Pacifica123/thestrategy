'''
 src/core/usecases/struct/sender.py
'''
from ..opresult import OperationResult, OperationStatus
from .contexts import StructContext


class StructSender:
    def fetch(self, context: str, data: dict) -> OperationResult:
        # TODO : проверка наличия context и валидности filters
        match context:
            case StructContext.TEST_WORK:
                return self._test_work(data)
            case _:
                return OperationResult(
                    OperationStatus.NOT_REALIZED,
                    message=f"Unknown case: {context}")

    def _test_work(self, data: dict) -> OperationResult:
        return OperationResult(
            OperationStatus.SUCCESS,
            msg="StructSender работает")
