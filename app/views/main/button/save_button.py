from app.model.enums import MenuType
from app.model.view_state import ViewState, ViewMode
from app.views.common.button_interface import ButtonInterface


class SaveButton(ButtonInterface):
    def __init__(self, view_state: ViewState):
        self.view_state = view_state
        self.menu_type = MenuType.SAVE
        self.view_modes = [ViewMode.EDIT]

    def action(self):
        pass

    def condition(self):
        return self.view_state.active and self.view_state.view_mode in self.view_modes

    def show(self):
        return self.get_data().text

    def get_type(self):
        return self.menu_type

    def get_data(self):
        return self.menu_type.value