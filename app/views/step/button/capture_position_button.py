import pyautogui

from app.model.data.field.data_types import DataType
from app.model.enums import MenuType
from app.model.view_state import ViewState, ViewMode
from app.views.common.button_interface import ButtonInterface


class CapturePositionButton(ButtonInterface):
    def __init__(self, view_state: ViewState):
        self.view_state = view_state
        self.menu_type = MenuType.CAPTURE_POSITION
        self.view_modes = [ViewMode.EDIT, ViewMode.NEW]

    def action(self):
        x, y = pyautogui.position()
        self.view_state.data_node.get_data_node(DataType.X).virtual = str(x)
        self.view_state.data_node.get_data_node(DataType.Y).virtual = str(y)

    def condition(self):
        return self.view_state.active and self.view_state.view_mode in self.view_modes

    def show(self):
        return self.get_data().text

    def get_type(self):
        return self.menu_type

    def get_data(self):
        return self.menu_type.value