from typing import List

from app.model.enums import CursorDirectionType
from app.model.framework.enhancement import Broadcastable
from app.model.framework.modifier.interactable import Interactable
from app.model.menu.menu_option import MenuOption
from app.service.broadcast_service import EventType


class MenuBar(Interactable, Broadcastable):
    def __init__(
            self,
            parent,
            menu_list: List[MenuOption]):
        Interactable.__init__(self)
        Broadcastable.__init__(self)
        self.menu_list: List[MenuOption] = menu_list
        self.parent = parent
        self._get_menu_options()[0].select()
        self._register_listener(EventType.MENU_NAVIGATION, self)
        self._register_menu_to_listener()
        self.activate()

    def _register_menu_to_listener(self):
        for entry in self.menu_list:
            self._register_listener(EventType.ENTER_PRESS, entry)

    def handle_event(self, direction: CursorDirectionType):
        """React to an event."""
        if self.parent.active:
            self.update_active_menu(direction)

    def update_active_menu(self, direction: CursorDirectionType):
        active_index = 0
        menu_options = self._get_menu_options()
        active_menu: MenuOption = self._get_active_menu()

        if menu_options.count(active_menu) != 0:
                active_index = menu_options.index(active_menu)
                if direction == CursorDirectionType.LEFT:
                    if not active_index - 1 < 0:
                        active_index -= 1
                if direction == CursorDirectionType.RIGHT:
                    if not active_index + 1 > len(menu_options) - 1:
                        active_index += 1
        new_active_menu: MenuOption = menu_options[active_index]
        active_menu.unselect()
        new_active_menu.select()
        self._broadcast(EventType.RENDER)
        return self

    def _get_active_menu(self):
        menu_list: List[MenuOption] = self.menu_list
        return list(filter(lambda item: item.selected, menu_list))[0]

    def _get_menu_options(self):
        menu_list: List[MenuOption] = self.menu_list
        filtered_list = list(filter(lambda item: item.condition(), menu_list))
        return sorted(filtered_list, key=lambda menu: menu.get_data.order)

    def render(self):
        for menu in self._get_menu_options(): # TEH SHOW_CONDITION FILES AND FUNCTIONS DECIDE IF THE MENU IS SHOWN OR NOT!
            menu.render()
        print('', end='\n') # next line! important to have it here