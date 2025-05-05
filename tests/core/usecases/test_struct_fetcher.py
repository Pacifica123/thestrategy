'''
 tests/core/usecases/test_struct_fetcher.py
'''
import pytest
from src.core.usecases.struct.fetcher import StructFetcher
from src.core.usecases.opresult import OperationStatus


def test_fetcher_unknown_case():
    fetcher = StructFetcher()
    result = fetcher.fetch('invalid', {})
    assert result.status == OperationStatus.NOT_REALIZED
