'''
 tests/adapters/inbound/http/controllers/test_auth_controller.py
'''
import pytest
from flask import Flask
from src.adapters.inbound.http.controllers.auth_controller import bp_auth


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(bp_auth)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_login_success(client, app):
    client = app.test_client()
    resp = client.post('/api/v1/auth/login', json={'username': 'alice', 'password': 'hashedpassword'})
    assert resp.status_code == 200
    assert 'access_token' in resp.json
