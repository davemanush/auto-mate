from app.model.enums import MenuType
from app.model.view_state import ViewState, ViewType, ViewMode
from app.views.button_interface import ButtonInterface
from app.views.script import ScriptView


class DetailsButton(ButtonInterface):
    def __init__(self, view_state: ViewState):
        self.view_state = view_state
        self.menu_type = MenuType.DETAILS
        self.view_modes = [ViewMode.VIEW, ViewMode.EDIT]

    def action(self):
        self.view_state.deactivate_view()
        details_view_state = ScriptView(
            parent=self.view_state,
            view_type=ViewType.SCRIPT_DETAILS,
            view_mode=self.view_state.view_mode,
            source=self.view_state.data_node.get_selected(),
        )
        details_view_state.activate_view()
        self.view_state.child = details_view_state

    def condition(self):
        return self.view_state.active and self.view_state.view_mode in self.view_modes

    def show(self):
        return self.get_data().text

    def get_type(self):
        return self.menu_type

    def get_data(self):
        return self.menu_type.value