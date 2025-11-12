from enum import Enum


class SubjectType(str, Enum):
    WRITTEN = "written"
    PRACTICAL = "practical"
    PROJECT = "project"


class SubjectStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

