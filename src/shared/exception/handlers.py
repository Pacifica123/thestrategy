# src/shared/exception/handlers.py
'''
 централизованные Flask-errorhandlers
'''
from flask import jsonify
from src.shared.exception.base import AppError


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(err: AppError):
        payload, status = err.to_response()
        return jsonify(payload), status

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not Found"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal Server Error"}), 500
