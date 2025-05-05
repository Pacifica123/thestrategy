'''
 src/adapters/inbound/http/controllers/auth_controller.py
'''
import os
from flask import Blueprint, request, jsonify, current_app
import jwt
from datetime import datetime, timedelta
from src.adapters.outbound.persistence.repositories.user_rep import SQLAlchemyUserRepository

bp_auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_HOURS = 24


@bp_auth.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    # используем UserRepository вместо in-memory хранилища
    session = current_app.extensions['db'].session
    repo = SQLAlchemyUserRepository(session)

    user = repo.get_by_username(username)
    if not user or user.password_hash != password:
        return jsonify({'error': 'Invalid credentials'}), 401

    payload = {
        'sub': username,
        'iat': datetime.utcnow().timestamp(),
        'exp': (datetime.utcnow() + timedelta(hours=JWT_EXP_DELTA_HOURS)).timestamp()
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return jsonify({'access_token': token})
