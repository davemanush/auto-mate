from app.model.enums import MenuType
from app.model.view_state import ViewState, ViewMode
from app.views.button_interface import ButtonInterface


class RestoreButton(ButtonInterface):
    def __init__(self, view_state: ViewState):
        self.view_state = view_state
        self.menu_type = MenuType.RESTORE
        self.view_modes = [ViewMode.EDIT]

    def action(self):
        self.view_state.virtual_data.get_selected().restore()

    def condition(self):
        return self.view_state.active and self.view_state.view_mode in self.view_modes \
            and self.view_state.virtual_data.get_selected().is_deleted()

    def show(self):
        return self.get_type().update_text("step")

    def get_type(self):
        return self.menu_type

    def get_data(self):
        return self.menu_type.value