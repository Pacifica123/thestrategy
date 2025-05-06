# src/shared/exception/base.py
'''
 базовые классы исключений (AppError и потомки)
'''


class AppError(Exception):
    """Базовое приложение-исключение с кодом и сообщением."""
    code = 500
    message = "Internal Server Error"

    def to_response(self):
        return {"error": self.message}, self.code
