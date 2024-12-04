from app.model.node import Node
from app.model.enums import MenuType
from app.model.view_state import ViewState, ViewMode
from app.views.common.button_interface import ButtonInterface


class DiscardButton(ButtonInterface):
    def __init__(self, view_state: ViewState):
        self.view_state = view_state
        self.menu_type = MenuType.DISCARD
        self.view_modes = [ViewMode.EDIT, ViewMode.NEW]

    def action(self):
        view_state = self.view_state
        if view_state.view_mode == ViewMode.NEW:
            view_state.parent.activate()
            view_state.deactivate()
            view_state.parent.child = None
            return
        for item in self.view_state.data_node.nodes:
            if isinstance(item, Node) and item.is_edited():
                item.discard_change()
                item.clear_error()
        view_state.parent.activate()
        view_state.deactivate()
        view_state.parent.child = None

    def condition(self):

        return  self.view_state.active and \
            (self.view_state.view_mode is ViewMode.EDIT
             and any([isinstance(item, Node) and item.is_edited() for item in self.view_state.data_node.nodes])) \
                or self.view_state.view_mode is ViewMode.NEW


    def show(self):
        if self.view_state.view_mode == ViewMode.EDIT:
            return self.get_type().get_text()
        return self.get_type().override_text("Discard new step")

    def get_type(self):
        return self.menu_type

    def get_data(self):
        return self.menu_type.value