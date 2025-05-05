# src/core/domain/value_objects/entity_type.py
from enum import Enum


class EntityType(Enum):
    USER                          = "user"
    PROJECT                       = "project"
    TASKBOARD                     = "taskboard"
    COLUMN                        = "column"
    TASK                          = "task"
    CHECKLIST                     = "checklist"
    CHECKITEM                     = "checkitem"
    PROJECT_MEMBER                = "project_member"
    PROJECT_MEMBER_PERMISSION     = "project_member_permission"
