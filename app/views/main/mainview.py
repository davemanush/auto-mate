from typing import List

from colorama import Fore, Back, Style

from app.model.menu.menu_bar import MenuBar
from app.model.menu.menu_option import MenuOption
from app.model.view_state import ViewState, ViewType, ViewMode
from app.service.broadcast_service import EventType
from app.views.main.button import StartButton, DetailsButton, ChangeModeButton, SettingsButton, \
    QuitButton, NewButton, SaveButton, MoveUpButton, MoveDownButton, DeleteButton, \
    RestoreButton


class MainView(ViewState):
    headers_to_fields = {
        'Script ID': 'entry_id',
        'Name': 'name',
        'Order': 'order',
        'Total steps': 'total_steps',
        'Last updated': 'last_update_datetime',
        'Last run date': 'last_run_datetime'
    }

    def __init__(self):
        super().__init__(
            view_type=ViewType.APP,
            view_mode=ViewMode.VIEW
        )
        self.menu = MenuBar(menu_list=self.__define_buttons(), parent=self)
        self._register_listener(EventType.RENDER, self)
        self._broadcast(EventType.RENDER)


    def handle_event(self):
        """React to an event."""
        if self.active:  # Only react to 'enter_press'
            self.render()

    def render(self):
        self._init_max_lengths('script', headers_to_fields=self.headers_to_fields)
        max_lengths = self._calculate_max_lengths(self.data_node.nodes)
        self._render()
        print(Fore.BLACK + Back.WHITE + "    | Script details".ljust(149) + Style.RESET_ALL, end='\n')
        # TODO refactor this later to be dynamic and rely on the settings which field was enabled and in which order
        print(
            f"{Fore.BLACK + Back.WHITE}   {Style.RESET_ALL} | "
            f"{"Script ID".ljust(max_lengths['script']['entry_id'])} | "
            f"{"Name".ljust(max_lengths['script']['name'])} | "
            f"{"Total steps".ljust(max_lengths['script']['total_steps'])} | "
            f"{"Last updated".ljust(max_lengths['script']['last_update_datetime'])} | "
            f"{"Last run date".ljust(max_lengths['script']['last_run_datetime'])} | ",
            end='\n')
        [item.render(max_lengths['script']) for item in self.data_node.nodes]

    def __define_buttons(self) -> List[MenuOption]:
        return [
            MenuOption(object_implementation=StartButton(view_state=self)),
            MenuOption(object_implementation=DetailsButton(view_state=self)),
            MenuOption(object_implementation=ChangeModeButton(view_state=self)),
            MenuOption(object_implementation=SettingsButton(view_state=self)),
            MenuOption(object_implementation=QuitButton(view_state=self)),

            ## EDIT MENU
            MenuOption(object_implementation=NewButton(view_state=self)),
            MenuOption(object_implementation=SaveButton(view_state=self)),
            MenuOption(object_implementation=MoveUpButton(view_state=self)),
            MenuOption(object_implementation=MoveDownButton(view_state=self)),
            MenuOption(object_implementation=DeleteButton(view_state=self)),
            MenuOption(object_implementation=RestoreButton(view_state=self)),
        ]