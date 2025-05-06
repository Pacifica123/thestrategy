# src/main.py
import os
from flask import Flask
from flask_cors import CORS
from src.shared.extensions import init_extensions
from src.shared.exception.handlers import register_error_handlers
from src.adapters.outbound.persistence.crud_auto_registry import generate_crud_handlers
from src.shared.extensions import db


def create_app(auto_init: bool = False):
    app = Flask(__name__, instance_relative_config=False)

    # 1. Конфиг по FLASK_ENV
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object('src.config.ProdConfig')
    elif env == 'testing':
        app.config.from_object('src.config.TestConfig')
    else:
        app.config.from_object('src.config.DevConfig')

    CORS(app, supports_credentials=True)

    # 2. Инициализация расширений (db, migrate, jwt…)
    init_extensions(app)

    # 3. Глобальные error-handler’ы для AppError и прочих
    register_error_handlers(app)

    # 4. Blueprint’ы
    from src.adapters.inbound.http.controllers.auth_controller import bp_auth
    from src.adapters.inbound.http.controllers.struct_controller import bp_struct
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_struct)
    # … другие контроллеры …

    # 5. Генерация CRUD-контекстов и регистрация ручных fetch/send
    with app.app_context():
        # автоматически «подхватит» все модели через Base.registry.mappers
        generate_crud_handlers(db.session)
        # инициализируйте модули с декораторами register_fetch/register_send,
        # чтобы они сами вешали специфичные хэндлеры в глобальные словари
        import src.core.usecases.struct.handlers.user_handlers
        # …  другие modules с ручными хэндлерами …

    return app


if __name__ == '__main__':
    # При запуске python -m src.main
    application = create_app()
    application.run(host='0.0.0.0', port=5000)
