# tests/core/usecases/test_opresult.py
import pytest
from src.core.usecases.opresult import OperationResult, OperationStatus


def test_operation_result():
    res = OperationResult(OperationStatus.SUCCESS, message="ok", data={'x':1})
    assert res.status == OperationStatus.SUCCESS
    assert res.message == "ok"
    assert res.data == {'x':1}
