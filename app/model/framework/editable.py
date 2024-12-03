from enum import Enum

from colorama import Back, Fore, Style

from app.model.framework.renderable import Renderable


class DataUpdateType(Enum):
    DELETE = 1
    ADD = 2
    OVERRIDE = 3

class StepDataType(Enum):
    NAME=("name", "Step name")
    X=("x", "X Coordinate")
    Y=("y", "Y Coordinate")
    ORDER=("order", "Order")
    DELAY=("delay", "Delay")
    DELAY_TYPE=("delay_type", "Delay type")
    CREATED_DATETIME=("created_datetime", "Created")
    LAST_UPDATE_DATETIME=("last_update_datetime", "Last updated")

class ScriptDataType(Enum):
    NAME=("name", "Step name")
    CREATED_DATETIME=("created_datetime", "Created")
    LAST_UPDATE_DATETIME=("last_update_datetime", "Last updated")
    LAST_RUN_DATETIME=("last_run_datetime", "Last updated")

class Editable(Renderable):
    def __init__(self, clazz=None, original=None, virtual_data=None, read_only=False):
        super().__init__()
        self.wrapper = virtual_data
        self.original = original
        self.read_only = read_only
        self.clazz = clazz
        self.deleted = False
        self.nodes = []
        self.data_type = None

    def discard_change(self):
        self.wrapper = self.original

    def get_data(self):
        return self.original

    def get_wrapper(self):
        return self.wrapper

    def is_read_only(self):
        return self.read_only

    def is_edited(self):
        if isinstance(self.original, str):
            return self.wrapper != self.original
        return any(item.is_edited() for item in self.wrapper)

    def is_new(self):
        return self.new

    def delete(self):
        self.deleted = True

    def is_deleted(self):
        return self.deleted

