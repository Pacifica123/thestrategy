import ast
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
import sys
import traceback

# --- Настройки ---
PROJECT_ROOT = Path(__file__).parent.parent  # корень проекта, где лежит src
SCHEMAS_ROOT = PROJECT_ROOT / 'src' / 'adapters' / 'inbound' / 'http' / 'schemas'

# Пример целевого пути, можно параметризовать /home/noir/projects/hobby/thestrategy/thestrategy_react/src/entities
TARGET_BASE_PATH = 'home/noir/projects/hobby/thestrategy/thestrategy_react/src/entities' # сюда будем писать TS модели

# --- Маппинг типов Python -> TypeScript ---
PY_TO_TS_TYPE_MAP = {
    'int': 'number',
    'float': 'number',
    'str': 'string',
    'bool': 'boolean',
    'Any': 'any',
    'dict': 'any',
    'list': 'any[]',
    'datetime': 'Date',
    'Optional': '',  # обрабатывается отдельно
    'Union': '',  # обрабатывается отдельно
}


# --- Помощь для логов ---


def log_info(msg: str):
    print(f"[INFO] {msg}")


def log_error(msg: str):
    print(f"[ERROR] {msg}")


def log_debug(msg: str):
    print(f"[DEBUG] {msg}")

# --- Утилиты для разбора аннотаций AST ---


def get_full_name(node: ast.AST) -> Optional[str]:
    """
    Рекурсивно получить полное имя типа из AST (например, Optional[int], List[str], mymodule.MyEnum)
    """
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        value = get_full_name(node.value)
        if value:
            return value + '.' + node.attr
        else:
            return node.attr
    elif isinstance(node, ast.Subscript):
        base = get_full_name(node.value)
        if base is None:
            return None
        # Для Optional[int] или List[str]
        if isinstance(node.slice, ast.Index):
            sub = get_full_name(node.slice.value)
        else:
            sub = get_full_name(node.slice)
        if sub:
            return f"{base}[{sub}]"
        else:
            return base
    elif isinstance(node, ast.Constant):
        return str(node.value)
    elif isinstance(node, ast.Tuple):
        # Для Union[int, str]
        elts = [get_full_name(e) for e in node.elts]
        return ','.join(filter(None, elts))
    else:
        return None


def parse_type_annotation(node: ast.AST) -> str:
    """
    Преобразовать аннотацию из AST в строку, например Optional[int], List[str]
    """
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return get_full_name(node)
    elif isinstance(node, ast.Subscript):
        base = parse_type_annotation(node.value)
        if isinstance(node.slice, ast.Index):
            sub = parse_type_annotation(node.slice.value)
        else:
            sub = parse_type_annotation(node.slice)
        return f"{base}[{sub}]"
    elif isinstance(node, ast.Tuple):
        return ','.join(parse_type_annotation(e) for e in node.elts)
    else:
        return 'Any'  # fallback


# --- Конвертация Python типов в TS ---


def python_type_to_ts(py_type: str) -> Tuple[str, bool]:
    """
    Конвертируем Python тип в TS.
    Возвращаем (ts_type, is_nullable)
    """
    # Обработка Optional[T] -> T | null
    if py_type.startswith('Optional[') and py_type.endswith(']'):
        inner = py_type[len('Optional['):-1]
        ts_inner, _ = python_type_to_ts(inner)
        return f"{ts_inner} | null", True

    # Обработка Union[T1, T2, ...]
    if py_type.startswith('Union[') and py_type.endswith(']'):
        inner = py_type[len('Union['):-1]
        parts = [p.strip() for p in inner.split(',')]
        ts_parts = []
        nullable = False
        for p in parts:
            ts_p, is_null = python_type_to_ts(p)
            ts_parts.append(ts_p)
            if is_null:
                nullable = True
        ts_type = ' | '.join(ts_parts)
        if nullable:
            ts_type += ' | null'
        return ts_type, nullable

    # Простейшие типы
    if py_type in PY_TO_TS_TYPE_MAP:
        ts_type = PY_TO_TS_TYPE_MAP[py_type]
        if ts_type == '':
            # например Optional или Union без параметров
            return 'any', True
        return ts_type, False

    # datetime.datetime или datetime
    if py_type.endswith('datetime'):
        return 'Date', False

    # Если тип содержит [], например List[int]
    if py_type.startswith('List[') and py_type.endswith(']'):
        inner = py_type[len('List['):-1]
        ts_inner, _ = python_type_to_ts(inner)
        return f"{ts_inner}[]", False

    # Если тип содержит Dict[...] - переводим в any
    if py_type.startswith('Dict['):
        return 'any', False

    # Если тип - enum или кастомный класс - возвращаем как есть (будет импорт)
    return py_type, False


# --- Парсинг файла схемы ---


class SchemaField:
    def __init__(self, name: str, py_type: str, default: Optional[Any], is_optional: bool):
        self.name = name
        self.py_type = py_type
        self.is_optional = is_optional
        self.default = default


class ParsedSchema:
    def __init__(self, name: str, fields: List[SchemaField], imports: Dict[str, str], orm_mode: bool):
        self.name = name
        self.fields = fields
        self.imports = imports  # {symbol: module_path}
        self.orm_mode = orm_mode


def parse_schema_file(file_path: Path) -> List[ParsedSchema]:
    """
    Парсим файл с pydantic схемами.
    Возвращаем список ParsedSchema.
    """
    log_info(f"Парсим файл схемы: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()

    tree = ast.parse(source, filename=str(file_path))

    # Собираем импорты, чтобы потом понимать откуда брать enum и другие классы
    imports_map = {}  # symbol -> module (пример: MyEnum -> src.enums.my_enum)
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                imports_map[alias.asname or alias.name] = module

    schemas = []

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            # Проверяем наследование от BaseModel
            base_names = [get_full_name(base) for base in node.bases]
            if 'BaseModel' not in base_names:
                continue

            class_name = node.name
            fields = []
            orm_mode = False

            # Ищем атрибуты класса - поля
            for stmt in node.body:
                # Проверка на Config класс
                if isinstance(stmt, ast.ClassDef) and stmt.name == 'Config':
                    for config_stmt in stmt.body:
                        if isinstance(config_stmt, ast.Assign):
                            for target in config_stmt.targets:
                                if isinstance(target, ast.Name) and target.id == 'orm_mode':
                                    if isinstance(config_stmt.value, ast.Constant) and config_stmt.value.value is True:
                                        orm_mode = True
                                        log_debug(f"Найдена orm_mode=True в {class_name}")

                # Поля - это AnnAssign (аннотированные присваивания)
                if isinstance(stmt, ast.AnnAssign):
                    field_name = stmt.target.id if isinstance(stmt.target, ast.Name) else None
                    if field_name is None:
                        continue
                    # Тип
                    py_type = parse_type_annotation(stmt.annotation)
                    # Значение по умолчанию
                    default = None
                    if stmt.value is not None:
                        if isinstance(stmt.value, ast.Constant):
                            default = stmt.value.value
                        elif isinstance(stmt.value, ast.NameConstant):
                            default = stmt.value.value
                        else:
                            default = None  # сложные значения не обрабатываем сейчас

                    # Определяем, является ли поле Optional
                    is_optional = py_type.startswith('Optional[') or default is not None

                    fields.append(SchemaField(field_name, py_type, default, is_optional))

            schemas.append(ParsedSchema(class_name, fields, imports_map, orm_mode))

    return schemas


# --- Генерация TS-кода ---


def snake_to_camel(snake_str: str) -> str:
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def generate_ts_class(schema: ParsedSchema) -> str:
    """
    Генерируем TS-класс из ParsedSchema.
    """
    class_name = schema.name
    fields = schema.fields

    lines = []
    lines.append(f"export class {class_name} {{")
    # Конструктор
    lines.append("    constructor(")
    for f in fields:
        ts_type, is_nullable = python_type_to_ts(f.py_type)
        # TS имя поля - camelCase
        ts_name = snake_to_camel(f.name)
        nullable_suffix = ' | null' if is_nullable else ''
        lines.append(f"        public {ts_name}: {ts_type}{nullable_suffix},")
    lines.append("    ) {}")
    lines.append("")

    # fromJson метод
    lines.append(f"    static fromJson(json: any): {class_name} {{")
    lines.append(f"        return new {class_name}(")
    for f in fields:
        ts_name = snake_to_camel(f.name)
        # Для дат - конвертируем в Date
        ts_type, _ = python_type_to_ts(f.py_type)
        is_date = ts_type == 'Date'
        is_nullable = f.py_type.startswith('Optional[') or f.default is not None

        json_field = f.name  # в json snake_case

        if is_date:
            if is_nullable:
                lines.append(f"            json.{json_field} ? new Date(json.{json_field}) : null,")
            else:
                lines.append(f"            new Date(json.{json_field}),")
        else:
            # Для nullable добавляем ?? null
            if is_nullable:
                lines.append(f"            json.{json_field} ?? null,")
            else:
                lines.append(f"            json.{json_field},")
    lines.append("        );")
    lines.append("    }")
    lines.append("}")

    return '\n'.join(lines)


# --- Основная логика ---


def process_all_schemas(target_base_path: Path):
    """
    Обрабатываем все схемы в SCHEMAS_ROOT и кладём TS модели в target_base_path.
    """
    log_info(f"Начинаем обработку схем из {SCHEMAS_ROOT}")

    # Ищем все .py файлы в schemas
    for schema_file in SCHEMAS_ROOT.glob('*.py'):
        try:
            schemas = parse_schema_file(schema_file)
            for schema in schemas:
                # Формируем путь для TS файла
                # Пример: TaskCreateSchema -> Task.ts (убираем суффиксы Create/Read)
                base_name = schema.name
                for suffix in ['CreateSchema', 'ReadSchema', 'Schema']:
                    if base_name.endswith(suffix):
                        base_name = base_name[:-len(suffix)]
                        break
                if not base_name:
                    base_name = schema.name

                # Путь: target_base_path / <schema_file.stem> / model / <BaseName>.ts
                ts_dir = target_base_path + '/' + schema_file.stem + '/' + 'model'
                ts_dir.mkdir(parents=True, exist_ok=True)
                ts_file = ts_dir + '/' + f"{base_name}.ts"

                ts_code = generate_ts_class(schema)
                with open(ts_file, 'w', encoding='utf-8') as f:
                    f.write(ts_code)

                log_info(f"Сгенерирована TS-модель {base_name} в {ts_file}")

        except Exception as e:
            log_error(f"Ошибка при обработке {schema_file}: {e}")
            traceback.print_exc()

    log_info("Обработка завершена.")


# --- Запуск ---


if __name__ == '__main__':
    try:
        # Можно добавить парсинг аргументов для target_base_path
        process_all_schemas(TARGET_BASE_PATH)
    except Exception as e:
        log_error(f"Критическая ошибка: {e}")
        traceback.print_exc()
        sys.exit(1)
