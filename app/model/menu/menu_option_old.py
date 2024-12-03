from typing import List

from colorama import Style, Back, Fore

from app.model.view_state import ViewMode
from app.model.framework.modifier.editable import Editable
from app.service.broadcast_service import EventType


class MenuOption_OLD(Editable):
    def __init__(self, view_modes: List[ViewMode], menu_type, show_action=None, action=None, condition=None):
        super().__init__()
        self.view_modes = view_modes
        self.menu_type = menu_type
        self.show_action = show_action
        self.action = action
        self.condition = condition

    def handle_event(self):
        if self.selected:
            self.execute()

    def execute(self):
        if self.action and self.condition(view_modes=self.view_modes):
            self.action()
            if self.menu_type.value.rerender():
                self._broadcast(EventType.RENDER)

    def render(self):
        separator = '|'
        color = ''
        color_override = ''
        reset_color = Style.RESET_ALL
        if self.menu_type.value.style_override:
            color_override = self.menu_type.value.style_override
        if self.selected:
            color = Back.LIGHTWHITE_EX + Fore.BLACK
        print(f"{color} {color_override}{self.show_action()}{reset_color}{color} {reset_color}{separator}", end='')
