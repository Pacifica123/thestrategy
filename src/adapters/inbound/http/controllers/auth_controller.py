'''
 src/adapters/inbound/http/controllers/auth_controller.py
'''
import os
from flask import Blueprint, request, jsonify, current_app
from src.shared.extensions import db

from src.core.usecases.auth.service import AuthService

bp_auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


def _make_service():
    return AuthService(
        session=db.session,
        jwt_secret=os.getenv('JWT_SECRET'),
        jwt_algo='HS256',
        jwt_exp_hours=24
    )


@bp_auth.route('/reg', methods=['POST'])
def register():
    svc = _make_service()
    user_data = svc.register(request.json or {})
    return jsonify(user_data), 201


@bp_auth.route('/login', methods=['POST'])
def login():
    svc = _make_service()
    token = svc.login(request.json or {})
    return jsonify({"access_token": token})


@bp_auth.route('/social', methods=['POST'])
def social_login():
    svc = _make_service()
    token = svc.social_login(request.json or {})
    return jsonify({"access_token": token})
