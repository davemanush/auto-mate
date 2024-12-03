from app.model.enums import MenuType
from app.model.view_state import ViewState, ViewMode
from app.views.button_interface import ButtonInterface


class ChangeModeButton(ButtonInterface):
    def __init__(self, view_state: ViewState):
        self.view_state = view_state
        self.menu_type = MenuType.CHANGE_MODE
        self.view_modes = [ViewMode.VIEW, ViewMode.EDIT]

    def action(self):
        if self.view_state.active:
            if self.view_state.view_mode is ViewMode.VIEW:
                self.view_state.view_mode = ViewMode.EDIT
                return
            if self.view_state.view_mode is ViewMode.EDIT:
                self.view_state.view_mode = ViewMode.VIEW

    def condition(self):
        return self.view_state.active and self.view_state.view_mode in self.view_modes

    def show(self):
        if self.view_state.view_mode is ViewMode.VIEW:
            return self.menu_type.update_text("Edit")
        if self.view_state.view_mode is ViewMode.EDIT:
            return self.menu_type.update_text("View")

    def get_data(self):
        return self.menu_type.value

    def get_type(self):
        return self.menu_type
