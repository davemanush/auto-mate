from enum import Enum

from colorama import Fore, Back

from app.model.menu.menu_type_data import MenuTypeData


class CursorDirectionType(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    NONE = 5

class DelayType(Enum):
    BEFORE = "Before"
    AFTER = "After"
    def find_by_name(name):
        for delay_type in DelayType:
            if delay_type.name == name:
                return delay_type
        return None

    def __str__(self):
        return self.name

class ConfirmOption(Enum):
    YES = "Yes"
    NO = "No"

class MenuType(Enum):
    SCRIPT_CREATE_NEW = MenuTypeData(11, "Create new script", 30, False)
    DETAILS = MenuTypeData(12, "View Details", 21, False)
    DELETE = MenuTypeData(13, "Delete <text>", 80, True, Fore.BLACK+Back.RED)
    START = MenuTypeData(14, "Start", 1, False)
    PAUSE_RUN = MenuTypeData(15, "Pause Run", 95, True)
    STOP = MenuTypeData(16, "Stop Run", 96, True)
    SAVE = MenuTypeData(17, "Save <text>", 10, True, Fore.BLACK+Back.LIGHTGREEN_EX)
    ADD = MenuTypeData(18, "Add step", 20, False, Fore.BLACK+Back.LIGHTBLUE_EX)
    EDIT = MenuTypeData(19, "Edit <text>", 30, False)
    DRY_RUN = MenuTypeData(20, "Dry run", 50, True, Fore.BLACK+Back.LIGHTYELLOW_EX)
    CAPTURE_POSITION = MenuTypeData(21, "Capture position", 40, True)
    RESTORE = MenuTypeData(21, "Restore <text>", 80, True, Fore.BLACK+Back.LIGHTGREEN_EX)
    CHANGE_MODE = MenuTypeData(21, "<text> mode", 22, True)
    MOVE_UP = MenuTypeData(21, "Move up", 40, True)
    MOVE_DOWN = MenuTypeData(21, "Move down", 40, True)

    # Step related
    SETTINGS = MenuTypeData(21, "Settings", 70, False)

    # GENERAL
    BACK = MenuTypeData(93, "Back", 99, True)
    DISCARD = MenuTypeData(94, "Discard changes", 99, True, Fore.BLACK+Back.LIGHTYELLOW_EX)
    QUIT_WINDOW = MenuTypeData(95, "Quit", 99, False)

    def update_text(self, text: str) -> str:
        return str(self.value.text.replace('<text>', text))

    def override_text(self, text: str) -> str:
        return str(text)

    def get_text(self) -> str:
        return self.value.text