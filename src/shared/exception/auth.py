# /home/noir/projects/hobby/thestrategy/thestrategy/src/shared/exception/auth.py
'''
UserAlreadyExists, InvalidCredentials, SocialAuthError
'''
from .base import AppError


class UserAlreadyExists(AppError):
    code = 409
    message = "Username или email уже существуют"


class InvalidCredentials(AppError):
    code = 401
    message = "Invalid username or password"


class SocialAuthError(AppError):
    code = 400
    message = "Social authentication failed"
