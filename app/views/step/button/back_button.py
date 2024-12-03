from app.model.enums import MenuType
from app.model.view_state import ViewState, ViewMode
from app.views.button_interface import ButtonInterface


class BackButton(ButtonInterface):
    def __init__(self, view_state: ViewState):
        self.view_state = view_state
        self.menu_type = MenuType.BACK
        self.view_modes = [ViewMode.VIEW, ViewMode.EDIT]

    def action(self):
        self.view_state.deactivate_view()
        self.view_state.parent.activate_view()
        self.view_state.parent.child = None

    def condition(self):
        return self.view_state.active and self.view_state.view_mode in self.view_modes

    def show(self):
        return self.get_data().text

    def get_type(self):
        return self.menu_type

    def get_data(self):
        return self.menu_type.value