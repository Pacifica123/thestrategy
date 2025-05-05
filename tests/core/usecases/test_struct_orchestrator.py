'''
 tests/core/usecases/test_struct_orchestrator.py
'''
import pytest
from src.core.usecases.struct.orchestrator import StructOrchestrator
from src.core.usecases.struct.fetcher import StructFetcher
from src.core.usecases.struct.sender import StructSender
from src.core.usecases.opresult import OperationStatus


class DummyFetcher(StructFetcher):
    def fetch(self, context, filters):
        return super()._test_work(filters) if context == 'test' else super().fetch(context, filters)


class DummySender(StructSender):
    def send(self, context, data):
        return super()._test_work(data) if context == 'test' else super().send(context, data)


@pytest.fixture
def orchestrator():
    return StructOrchestrator(DummyFetcher(), DummySender())


def test_orchestrator_success(orchestrator):
    result = orchestrator.run('test', {'filters': {}})
    assert result.status == OperationStatus.SUCCESS
    assert 'fetched' in result.data
    assert 'sent_message' in result.data


def test_orchestrator_fetch_failure(orchestrator):
    # Unknown context: fetch returns NOT_REALIZED
    result = orchestrator.run('invalid', {})
    assert result.status == OperationStatus.NOT_REALIZED
