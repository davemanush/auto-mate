from typing import List

from app.model.data_node import DataNode
from app.model.enums import MenuType
from app.model.view_state import ViewState, ViewMode
from app.views.button_interface import ButtonInterface


class SaveButton(ButtonInterface):
    def __init__(self, view_state: ViewState):
        self.view_state = view_state
        self.menu_type = MenuType.SAVE
        self.view_modes = [ViewMode.EDIT, ViewMode.NEW]

    def action(self):
        self.view_state.virtual_data.clear_validation_errors()
        error_found = False
        for data_node in self.view_state.virtual_data.nodes:
            if isinstance(data_node, DataNode) and not data_node.data_type.validate(data_node.wrapper):
                error_found = True
                data_node.set_validation_error(data_node.data_type.validation_error_message + " - Value: " + data_node.wrapper)
        if error_found:
            return

        if self.view_state.view_mode == ViewMode.NEW:
            self.view_state.virtual_data.set_newly_created()
            self.view_state.parent.virtual_data.nodes.append(self.view_state.virtual_data)
            self.view_state.parent.activate_view()
            self.view_state.deactivate_view()
            self.view_state.parent.child = None
            return
        if self.view_state.view_mode == ViewMode.EDIT:
            self.view_state.parent.activate_view()
            self.view_state.deactivate_view()
            self.view_state.parent.child = None
        return

    def condition(self):
        return  self.view_state.active and self.view_state.view_mode in self.view_modes \
                and any([isinstance(item, DataNode) and item.is_edited() for item in self.view_state.virtual_data.nodes])

    def show(self):
        return self.get_type().update_text("step")

    def get_type(self):
        return self.menu_type

    def get_data(self):
        return self.menu_type.value