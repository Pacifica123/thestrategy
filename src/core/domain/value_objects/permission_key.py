# src/core/domain/value_objects/permission_key.py
from enum import Enum


class PermissionKey(Enum):
    VIEW_PROJECT           = "view_project"           # читать данные проекта
    EDIT_PROJECT           = "edit_project"           # менять настройки проекта
    DELETE_PROJECT         = "delete_project"         # удалять проект
    INVITE_MEMBER          = "invite_member"          # приглашать участников
    REMOVE_MEMBER          = "remove_member"          # убирать участников
    MANAGE_PERMISSIONS     = "manage_permissions"     # менять чужие разрешения
    CREATE_TASKBOARD       = "create_taskboard"       # создавать доски
    EDIT_TASKBOARD         = "edit_taskboard"         # редактировать доски
    DELETE_TASKBOARD       = "delete_taskboard"       # удалять доски
    CREATE_COLUMN          = "create_column"          # создавать колонки
    EDIT_COLUMN            = "edit_column"            # редактировать колонки
    DELETE_COLUMN          = "delete_column"          # удалять колонки
    CREATE_TASK            = "create_task"            # создавать задачи
    EDIT_TASK              = "edit_task"              # редактировать задачи
    DELETE_TASK            = "delete_task"            # удалять задачи
    CHECK_TASK             = "check_task"             # отмечать чекбоксы
    # …и т. д., можно добавлять по мере необходимости
