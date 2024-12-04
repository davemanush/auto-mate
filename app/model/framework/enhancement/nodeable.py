from app.model.enums import CursorDirectionType
from app.model.framework.enhancement import Broadcastable
from app.model.framework.enums import DataUpdateType, ViewMode
from app.model.framework.modifier import Editable
from app.model.framework.modifier.interactable import Interactable
from app.service.broadcast_service import EventType

class DataUpdate:
    def __init__(self, step_data_type: DataUpdateType, data: str):
        self.type: DataUpdateType = step_data_type
        self.data: str = data

class Nodeable(Editable, Broadcastable, Interactable):
    def __init__(self, node_id=None, source=None, data_type=None, clazz=None, order=0, owner=None, parent=None):
        Interactable.__init__(self, owner=owner, parent=parent)
        Broadcastable.__init__(self)
        Editable.__init__(self, source=source, clazz=clazz, data_type=data_type)
        self.node_id = node_id
        self.order = order
        if self.is_leaf():
            self.nodes = []

    def is_leaf(self):
        return True if self.data_type is not None else False

    def get_data_node(self, data_type):
        return next((item for item in self.nodes if item.data_type == data_type), None)

    def is_node_edited(self):
        for node in self.nodes:
            if self.is_leaf() and node.is_node_edited():
                return True
        return self.is_edited()

    def is_nodes_active(self):
        for node in self.nodes:
            if node.is_active():
                return True
        return False

    def handle_event(self, data):
        if isinstance(data , CursorDirectionType):
            if not self.is_leaf() and self.active and self.parent and self.owner.active and data is not None and self.is_nodes_active():
                self.update_active_data(data)
        if isinstance(data, DataUpdate):
            if self.is_leaf() and data is not None and self.parent.active and self.owner.active and self.is_active() and self.selected and (self.owner.view_mode in [ViewMode.EDIT, ViewMode.NEW]):
                self.update_data(data)
                self._broadcast(EventType.RENDER)

    def update_data(self, update_data: DataUpdate):
        if update_data.type is DataUpdateType.DELETE:
            self.virtual = self.virtual[:-1]
        elif update_data.type is DataUpdateType.ADD:
            self.virtual += update_data.data
        elif update_data.type is DataUpdateType.OVERRIDE:
            self.virtual = update_data.data

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

    def get_node(self, entry_id):
        return next((item for item in self.nodes if item.id == entry_id), None)

    def activate_node(self):
        for node in self.nodes:
            node.activate()
        self.activate()

    def deactivate_node(self):
        for node in self.nodes:
            if node.is_leaf():
                node.deactivate()
            else:
                node.deactivate_node()
        self.deactivate()

    def clear_validation_errors(self):
        for node in self.nodes:
            node.clear_error()

    def sort_nodes(self):
        self.nodes = sorted(self.nodes, key=lambda node: (0 if node.is_leaf() else 1, node.order))

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

    def get_selected(self):
        return next((item for item in self.nodes if item.selected), None)
