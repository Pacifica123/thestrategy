# src/core/usecases/auth/service.py
'''
 AuthService с методами register, login, social_login
'''
from datetime import datetime, timedelta
from src.core.usecases.auth.schemas import RegisterSchema, LoginSchema, SocialLoginSchema
from src.adapters.outbound.persistence.repositories.user_rep import SQLAlchemyUserRepository
from src.shared.utils.security import create_access_token, verify_social_token, hash_password, verify_password
from src.shared.exception.auth import InvalidCredentials, UserAlreadyExists, SocialAuthError
from src.shared.utils.logger import configure_logger
logger = configure_logger(__name__)


class AuthService:
    def __init__(self, session, jwt_secret: str, jwt_algo: str, jwt_exp_hours: int):
        self.session = session
        self.repo = SQLAlchemyUserRepository(session)
        self.jwt_secret = jwt_secret
        self.jwt_algo = jwt_algo
        self.jwt_exp = timedelta(hours=jwt_exp_hours)

    def register(self, data: dict) -> dict:
        schema = RegisterSchema(**data)
        logger.info("Попытка регистрации пользователя: %s", schema.username)
        if self.repo.get_by_username(schema.username) or self.repo.get_by_email(schema.email):
            raise UserAlreadyExists()
        user = self.repo.create(
            username=schema.username,
            email=schema.email,
            password_hash=hash_password(schema.password)
        )
        return {"id": user.id, "username": user.username, "email": user.email}

    def login(self, data: dict) -> str:
        schema = LoginSchema(**data)
        user = self.repo.get_by_username(schema.username)
        if not user or not verify_password(schema.password, user.password_hash):
            logger.error("Ошибка авторизации", exc_info=True)
            raise InvalidCredentials()
        return create_access_token(
            {
                'sub': user.username,
                'iat': datetime.utcnow().timestamp(),
                'exp': (datetime.utcnow() + self.jwt_exp)
            },
            secret=self.jwt_secret,
            algorithm=self.jwt_algo,
            expires_delta=self.jwt_exp
        )

    def social_login(self, data: dict) -> str:
        schema = SocialLoginSchema(**data)
        info = verify_social_token(schema.provider, schema.token)
        email = info.get("email")
        if not email:
            raise SocialAuthError("No email from provider")
        user = self.repo.get_by_email(email)
        if not user:
            user = self.repo.create(
                username=email.split("@")[0],
                email=email,
                password_hash=""
            )
        return create_access_token(
            {
                'sub': user.username,
                'iat': datetime.utcnow().timestamp(),
                'exp': (datetime.utcnow() + self.jwt_exp)
            },
            secret=self.jwt_secret,
            algorithm=self.jwt_algo,
            expires_delta=self.jwt_exp
        )
