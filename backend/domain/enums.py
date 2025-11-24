from enum import Enum


class TaskType(str, Enum):
    WRITTEN = "written"
    PRACTICAL = "practical"
    PROJECT = "project"


class TaskStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

