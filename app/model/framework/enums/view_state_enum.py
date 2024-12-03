from enum import Enum

class ViewType(Enum):
    APP = 1
    SCRIPT_DETAILS = 2
    STEP_DETAILS = 3
    SETTINGS = 3
    RUN = 4
    CONFIRM_PAGE = 5


class ViewMode(Enum):
    VIEW = 1
    EDIT = 2
    NEW = 3