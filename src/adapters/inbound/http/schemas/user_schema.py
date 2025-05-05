# src/adapters/inbound/http/schemas/user_schema.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserReadSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_blocked: bool
    created_at: datetime

    class Config:
        orm_mode = True
