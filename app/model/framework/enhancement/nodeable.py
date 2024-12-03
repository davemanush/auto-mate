from app.model.enums import CursorDirectionType
from app.model.framework.enhancement import Broadcastable
from app.model.framework.enhancement.tableable import Tableable
from app.model.framework.enums import DataUpdateType, ViewMode
from app.model.framework.modifier.interactable import Interactable
from app.service.broadcast_service import EventType

class DataUpdate:
    def __init__(self, step_data_type: DataUpdateType, data: str):
        self.type: DataUpdateType = step_data_type
        self.data: str = data

class Nodeable(Tableable, Broadcastable, Interactable):
    def __init__(self, node_id=None, source=None, data_type=None, clazz=None, order=0, owner=None, parent=None):
        Interactable.__init__(self, owner=owner, parent=parent)
        Broadcastable.__init__(self)
        Tableable.__init__(self, source=source, data_type=data_type, clazz=clazz)
        self.node_id = node_id
        self.order = order

    def _register_listener(self, event_type: EventType, listener):
        if len(self.nodes) > 0:
            self.nodes[0].select()
            self._register_listener(EventType.DATA_NAVIGATION, self)
        if self.is_leaf() and not self.data_type.get_data().is_read_only():
            self._register_listener(EventType.USER_TYPING, self)

    def handle_event(self, update_data: DataUpdate=None, cursor_direction: CursorDirectionType=None):
        if self.is_leaf() and update_data is not None and self.owner.active and self.selected and (self.owner.view_mode in [ViewMode.EDIT, ViewMode.NEW]):
            self.update_data(update_data)
            self._broadcast(EventType.RENDER)
        if self.owner.active and cursor_direction is not None:
            self.update_active_data(cursor_direction)

    def update_node_owner(self, owner):
        self.update_owner(owner)
        for data in self.nodes:
            data.update_owner(owner)

    def restore_node(self):
        for node in self.nodes:
            node.restore()
        self.restore_node()

    def get_nodes(self):
        return [node for node in self.nodes if not node.is_leaf()] or None

    def get_leafs(self):
        return [node for node in self.nodes if node.is_leaf()] or None

    def get_leaf(self, data_type):
        return next((item for item in self.nodes if item.data_type == data_type), None)

    def get_node(self, id):
        return next((item for item in self.nodes if item.id == id), None)

    def activate_node(self):
        for node in self.nodes:
            node.activate()
        if not self.is_active():
            self.activate()

    def deactivate_node(self):
        for node in self.nodes:
            node.deactivate()
        if self.is_active():
            self.deactivate()

    def clear_validation_errors(self):
        for node in self.nodes:
            node.clear_error()

    def sort_nodes(self):
        self.nodes = sorted(self.nodes, key=lambda node: (0 if node.is_leaf() else 1, node.order))

    def update_data(self, update_data: DataUpdate):
        if update_data.type is DataUpdateType.DELETE:
            self.wrapper = self.wrapper[:-1]
        elif update_data.type is DataUpdateType.ADD:
            self.wrapper += update_data.data
        elif update_data.type is DataUpdateType.OVERRIDE:
            self.wrapper = update_data.data

    def discard_node_changes(self):
        for data in self.nodes:
            data.discard_change()
        if self.is_edited():
            self.discard_change()

    def drop_new_nodes(self):
        items_to_delete = []
        for data in self.nodes:
            if data.is_new():
                items_to_delete.append(data)
        self.nodes = [item for item in self.nodes if item not in items_to_delete]

    def update_active_data(self, direction: CursorDirectionType):
        active_data = self.get_selected()
        active_index = self.nodes.index(active_data)
        if direction == CursorDirectionType.UP:
            if not active_index - 1 < 0:
                new_active_data: Nodeable = self.nodes[active_index - 1]
                new_active_data.select()
                active_data.unselect()
        if direction == CursorDirectionType.DOWN:
            if not active_index + 1 > len(self.nodes) - 1:
                new_active_data: Nodeable = self.nodes[active_index + 1]
                new_active_data.select()
                active_data.unselect()
        ## broadcast the event to update the menu
        self._broadcast(EventType.MENU_NAVIGATION, CursorDirectionType.NONE)

    def get_selected(self):
        return next((item for item in self.nodes if item.selected), None)

    def render(self, attribute_length, max_length):
        if self.is_leaf():
            print(f'{self._render_cursor()} | {self.data_type.get_data().get_display_name().ljust(attribute_length)} | {self.wrapper.ljust(int(max_length / 2 + 1))} | {self._render_modifier(self)}',
                  end='\n')