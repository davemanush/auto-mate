
from app.model.enums import MenuType
from app.model.node import Node
from app.model.view_state import ViewState, ViewMode
from app.views.common.button_interface import ButtonInterface


class SaveButton(ButtonInterface):
    def __init__(self, view_state: ViewState):
        self.view_state = view_state
        self.menu_type = MenuType.SAVE
        self.view_modes = [ViewMode.EDIT, ViewMode.NEW]

    def action(self):
        self.view_state.data_node.clear_validation_errors()
        error_found = False
        for data_node in self.view_state.data_node.nodes:
            if data_node.data_type.get_data().is_read_only() and not data_node.data_type.validate(data_node.wrapper):
                error_found = True
                data_node.set_validation_error(data_node.data_type.validation_error_message + " - Value: " + data_node.wrapper)
        if error_found:
            return

        if self.view_state.view_mode == ViewMode.NEW:
            self.view_state.data_node.set_newly_created()
            self.view_state.parent.data_node.nodes.append(self.view_state.data_node)
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
                and any([isinstance(item, Node) and item.is_edited() for item in self.view_state.data_node.nodes])

    def show(self):
        return self.get_type().update_text("step")

    def get_type(self):
        return self.menu_type

    def get_data(self):
        return self.menu_type.value