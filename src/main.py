# from dotenv import load_dotenv
import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from src.config import DevConfig, TestConfig, ProdConfig

# Расширения
db = SQLAlchemy()
# load_dotenv()


def create_app(auto_init: bool = False):
    app = Flask(__name__, instance_relative_config=False)

    # Выбираем конфиг по FLASK_ENV
    FLASK_ENV = os.getenv('FLASK_ENV')
    if FLASK_ENV == 'production':
        app.config.from_object(ProdConfig)
    elif FLASK_ENV == 'testing':
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(DevConfig)

    # Инициализация расширений
    CORS(app)
    db.init_app(app)

    # --- Пре-инициализация базы (только если явно просили) ---
    if auto_init and FLASK_ENV != 'production':
        with app.app_context():
            from scripts.pre_initial import init_db, pre_initial_users
            init_db()               # создаёт все таблицы
            pre_initial_users()     # наполняет пользователей
    # ------------------------------------------------------------

    # Регистрируем blueprints
    from src.adapters.inbound.http.controllers.auth_controller import bp_auth
    from src.adapters.inbound.http.controllers.struct_controller import bp_struct
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_struct)

    return app


if __name__ == '__main__':
    # При запуске python -m src.main
    application = create_app()
    application.run(host='0.0.0.0', port=5000)
