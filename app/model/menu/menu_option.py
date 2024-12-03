from colorama import Style, Back, Fore

from app.model.framework.enhancement import Broadcastable
from app.model.framework.modifier.editable import Editable
from app.model.framework.modifier.selectable import Selectable
from app.service.broadcast_service import EventType
from app.views.button_interface import ButtonInterface


class MenuOption(Selectable, Broadcastable):
    def __init__(self, object_implementation: ButtonInterface):
        Selectable.__init__(self)
        Broadcastable.__init__(self)
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
