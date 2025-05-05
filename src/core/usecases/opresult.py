# src/core/usecases/opresult.py
from enum import Enum


class OperationStatus(Enum):
    SUCCESS = "success"
    DATABASE_ERROR = "db_error"
    VALIDATION_ERROR = "invalid_error"
    AUTHENTICATION_ERROR = "auth_error"
    NOT_REALIZED = "not_realized"


class OperationResult:
    def __init__(self, status: OperationStatus, msg: str = None, data=None):
        self.status = status
        self.message = message
        self.data = data
