# src/core/usecases/auth/schemas.py
'''
 Pydantic: RegisterSchema, LoginSchema, SocialLoginSchema
'''

from pydantic import BaseModel, EmailStr, constr


class RegisterSchema(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=8)


class LoginSchema(BaseModel):
    username: str
    password: str


class SocialLoginSchema(BaseModel):
    provider: str               # e.g. 'google', 'facebook'
    token: str                  # OAuth access token from client
