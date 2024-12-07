from app.model.node import Node
from app.model.enums import MenuType
from app.model.view_state import ViewState, ViewMode
from app.views.common.button_interface import ButtonInterface


class DiscardButton(ButtonInterface):
    def __init__(self, view_state: ViewState):
        self.view_state = view_state
        self.menu_type = MenuType.DISCARD
        self.view_modes = [ViewMode.EDIT]

    def action(self):
        items_to_delete = []
        for item in self.view_state.data_node.virtual:
            if isinstance(item, Node) and item.is_edited():
                item.discard_change()
            if isinstance(item, Node):
                if item.is_deleted():
                    item.restore()
                elif item.is_new():
                    items_to_delete.append(item)
                elif item.is_edited():
                    for child in item.nodes:
                        if child.is_edited():
                            child.discard_change()
        self.view_state.data_node.virtual = [item for item in self.view_state.data_node.virtual if item not in items_to_delete]

    def condition(self):
        return  self.view_state.active and self.view_state.view_mode in self.view_modes \
                and (self.view_state.data_node.is_node_edited()
                     or self.view_state.data_node.has_node_deleted()
                     or self.view_state.data_node.has_node_created())

    def show(self):
        return self.get_type().update_text("script")

    def get_type(self):
        return self.menu_type

    def get_data(self):
        return self.menu_type.value