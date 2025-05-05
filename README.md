# TheStrategy Backend

**Flask-based** сервер для Kanban-приложения, архитектура по Clean Architecture / Hexagonal.

## 📁 Структура проекта
```bash
.
├── migrations/ # Alembic-миграции
├── scripts/
│ └── pre_initial.py # создание схемы + seed-данные dev
├── src/
│ ├── main.py # точка входа, create_app()
│ ├── config.py # Dev/Test/Prod конфигурации
│ ├── core/
│ │ ├── domain/ # сущности (@dataclass), VO, enums
│ │ ├── usecases/ # бизнес-правила, orchestrators
│ │ └── ports/ # интерфейсы репозиториев
│ ├── adapters/
│ │ ├── inbound/http/ # Flask-Blueprints, Pydantic-schemas
│ │ └── outbound/persistence/
│ │ ├── models/ # SQLAlchemy-модели + mixins
│ │ ├── repositories/ # базовый CRUD + декораторы
│ │ └── factory.py # фабрика обёрнутых репозиториев
│ └── shared/ # исключения, security (bcrypt, JWT), утилиты
├── tests/ # модульные и интеграционные тесты
├── req.txt # зависимости
├── pytest.ini
└── README.md # вы здесь
```

## Быстрый старт

1. **Создать виртуальное окружение и установить зависимости**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r req.txt
   ```

2. **Настроить переменные окружения**
    Создать .env (не в репо) с
    FLASK_ENV=development
    DATABASE_DEV_URL=postgresql://user:pass@localhost:5432/thestrategy
    JWT_SECRET=your_secret
    
3. **Инициализировать базу и наполнить dev-данными**
    ```bash
    python -m scripts.pre_initial
    ```
    
4. **Запустить:**
    ```bash
    python -m src.main
    ```
    
По умолчанию открывается http://0.0.0.0:5000.

