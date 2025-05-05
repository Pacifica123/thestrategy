'''
 src/core/usecases/struct/orchestrator.py
'''
from .fetcher import StructFetcher
from .sender import StructSender
from ..opresult import OperationResult, OperationStatus


class StructOrchestrator:
    def __init__(self, fetcher: StructFetcher, sender: StructSender):
        self.fetcher = fetcher
        self.sender = sender

    def run(self, context: str, payload: dict) -> OperationResult:
        # 1. Fetch data based on context
        fetch_result = self.fetcher.fetch(context, payload.get('filters', {}))
        if fetch_result.status != OperationStatus.SUCCESS:
            return fetch_result

        # 2. Send or process fetched data
        send_result = self.sender.send(context, fetch_result.data)
        if send_result.status != OperationStatus.SUCCESS:
            return send_result

        # 3. Combine results
        return OperationResult(
            OperationStatus.SUCCESS,
            data={
                'fetched': fetch_result.data,
                'sent_message': send_result.message
            })
