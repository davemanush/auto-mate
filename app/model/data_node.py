from enum import Enum

from app.model.data.data_types import DataType
from app.model.framework.enums import ViewMode
from app.model.framework.errorable import Errorable
from app.model.framework.ownable import Ownable
from app.model.framework.editable import Editable

from app.service.broadcast_service import EventType


class DataUpdateType(Enum):
    DELETE = 1
    ADD = 2
    OVERRIDE = 3

class DataUpdate:
    def __init__(self, step_data_type: DataUpdateType, data: str):
        self.type: DataUpdateType = step_data_type
        self.data: str = data

class DataNode(Editable, Ownable):
    def __init__(self, original, virtual_data, data_type: DataType, clazz, parent=None, owner=None):
        Editable.__init__(self, original=str(original), virtual_data= str(virtual_data), clazz = clazz)
        Ownable.__init__(self, owner=owner)
        self.data_type: DataType = data_type
        self.parent = parent
        if not self.data_type.get_data().is_read_only():
            self._register_listener(EventType.USER_TYPING, self)

    def handle_event(self, update_data: DataUpdate):
        if  self.owner.active and self.selected and (self.owner.view_mode == ViewMode.EDIT or self.owner.view_mode == ViewMode.NEW):
            self.update(update_data)
            self._broadcast(EventType.RENDER)

    def get_entry_wrapper(self):
        return self.parent

    def activate_node(self):
        self.activate()

    def update(self, update_data: DataUpdate):
        if update_data.type is DataUpdateType.DELETE:
            self.wrapper = self.wrapper[:-1]
        elif update_data.type is DataUpdateType.ADD:
            self.wrapper += update_data.data
        elif update_data.type is DataUpdateType.OVERRIDE:
            self.wrapper = update_data.data


    def render(self, attribute_length, max_length):
        print(f'{self._render_cursor()} | {self.data_type.get_data().get_display_name().ljust(attribute_length)} | {self.wrapper.ljust(int(max_length / 2 + 1))} | {self._render_modifier(self)}',
              end='\n')