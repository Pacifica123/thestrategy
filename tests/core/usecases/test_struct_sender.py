'''
 tests/core/usecases/test_struct_sender.py
'''
import pytest
from src.core.usecases.struct.sender import StructSender
from src.core.usecases.opresult import OperationStatus


def test_sender_unknown_case():
    sender = StructSender()
    result = sender.send('invalid', {})
    assert result.status == OperationStatus.NOT_REALIZED
