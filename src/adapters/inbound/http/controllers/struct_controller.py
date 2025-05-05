'''
 src/adapters/inbound/http/controllers/struct_controller.py
'''
from flask import Blueprint, request, jsonify
from src.core.usecases.struct import StructOrchestrator, StructFetcher, StructSender
from src.core.usecases.opresult import OperationStatus

bp_struct = Blueprint('struct', __name__, url_prefix='/api/v1/struct')

# Initialize orchestrator with real fetcher/sender
orchestrator = StructOrchestrator(StructFetcher(), StructSender())


@bp_struct.route('', methods=['POST'])
def handle_struct():
    body = request.get_json() or {}
    context = body.get('context')
    payload = body
    result = orchestrator.run(context, payload)
    status_code = 200 if result.status == OperationStatus.SUCCESS else 400
    return jsonify({
        'status': result.status.value,
        'message': result.message,
        'data': result.data
    }), status_code
