from sys import implementation
from typing import List

from colorama import Style, Back, Fore

from app.model.view_state import ViewMode
from app.model.framework.editable import Editable
from app.service.broadcast_service import EventType
from app.views.button_interface import ButtonInterface


class MenuOption(Editable):
    def __init__(self, object_implementation: ButtonInterface):
        super().__init__()
        self.show = object_implementation.show
        self.action = object_implementation.action
        self.condition = object_implementation.condition
        self.get_type = object_implementation.get_type()
        self.get_data = object_implementation.get_data()

    def handle_event(self):
        if self.selected:
            self.execute()

    def execute(self):
        if self.action and self.condition():
            self.action()
            if self.get_data.rerender():
                self._broadcast(EventType.RENDER)

    def render(self):
        separator = '|'
        color = ''
        color_override = ''
        reset_color = Style.RESET_ALL
        if self.get_data.style_override:
            color_override = self.get_data.style_override
        if self.selected:
            color = Back.LIGHTWHITE_EX + Fore.BLACK
        print(f"{color} {color_override}{self.show()}{reset_color}{color} {reset_color}{separator}", end='')
