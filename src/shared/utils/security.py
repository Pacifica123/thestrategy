# src/shared/utils/security.py
'''
    генерация и верификация JWT, хэширование  и верификация пароля,
    прочие методы касательно безопасности
'''
import bcrypt
import jwt
import requests
from datetime import datetime, timedelta


def hash_password(plain: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain.encode('utf-8'), salt).decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))


def create_access_token(data: dict, secret: str, algorithm: str, expires_delta: timedelta) -> str:
    now = datetime.utcnow()
    payload = {**data, "iat": now, "exp": now + expires_delta}
    return jwt.encode(payload, secret, algorithm=algorithm)


def verify_social_token(provider: str, token: str) -> dict:
    if provider == "google":
        resp = requests.get("https://oauth2.googleapis.com/tokeninfo",
                            params={"id_token": token})
        resp.raise_for_status()
        return resp.json()
    raise ValueError(f"Unknown provider {provider}")
