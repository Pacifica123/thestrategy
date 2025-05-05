# src/core/domain/value_objects/event_type.py
from enum import Enum


class EventType(Enum):
    # Проект
    PROJECT_CREATED               = "project_created"
    PROJECT_UPDATED               = "project_updated"
    PROJECT_DELETED               = "project_deleted"
    # Участник
    MEMBER_INVITED                = "member_invited"
    MEMBER_REMOVED                = "member_removed"
    PERMISSIONS_CHANGED           = "permissions_changed"
    # Доска
    TASKBOARD_CREATED             = "taskboard_created"
    TASKBOARD_UPDATED             = "taskboard_updated"
    TASKBOARD_DELETED             = "taskboard_deleted"
    # Колонка
    COLUMN_CREATED                = "column_created"
    COLUMN_MOVED                  = "column_moved"
    COLUMN_UPDATED                = "column_updated"
    COLUMN_DELETED                = "column_deleted"
    # Задача
    TASK_CREATED                  = "task_created"
    TASK_UPDATED                  = "task_updated"
    TASK_MOVED                    = "task_moved"
    TASK_COMPLETED                = "task_completed"
    TASK_REOPENED                 = "task_reopened"
    TASK_DELETED                  = "task_deleted"
    # Чек-лист
    CHECKLIST_CREATED             = "checklist_created"
    CHECKLIST_UPDATED             = "checklist_updated"
    CHECKLIST_DELETED             = "checklist_deleted"
    # Чек-бокс
    CHECKITEM_TOGGLED             = "checkitem_toggled"
    CHECKITEM_CREATED             = "checkitem_created"
    CHECKITEM_DELETED             = "checkitem_deleted"
    # Прочее
    CUSTOM_EVENT                  = "custom_event"
