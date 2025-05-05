#!/usr/bin/env python
import os
import sys

# 1) Чтобы наш src был в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import create_app, db
from adapters.outbound.persistence.repositories.user_rep import SQLAlchemyUserRepository

# здесь берём Base из вашего пакета моделей
from adapters.outbound.persistence.models.base import Base


def run_all():
    app = create_app(auto_init=False)
    with app.app_context():
        # 1) Импортируем пакет моделей, чтобы Base.metadata наполнился всеми Table
        import adapters.outbound.persistence.models

        # 2) Создаём схему по вашему Base
        print("➤ Creating database tables …")
        Base.metadata.create_all(bind=db.engine)
        print("✔ Tables created.")

        # 3) Заливаем тестовых пользователей
        print("➤ Pre-filling test users …")
        session = db.session
        repo = SQLAlchemyUserRepository(session)
        users = [
            {'username': 'alice', 'email': 'alice@example.com', 'password_hash': 'hash1'},
            {'username': 'bob',   'email': 'bob@example.com',   'password_hash': 'hash2'},
            {'username': 'carol', 'email': 'carol@example.com', 'password_hash': 'hash3'},
        ]
        for u in users:
            if not repo.get_by_username(u['username']):
                repo.create(**u)
        session.commit()
        print("✔ Test users created.")

    print("🎉 Pre-initialization complete.")


if __name__ == '__main__':
    run_all()
