from typing import List

from colorama import Fore, Back, Style

from app.model.data_node import DataNode
from app.model.menu.menu_bar import MenuBar
from app.model.menu.menu_option import MenuOption
from app.model.view_state import ViewState, ViewType, ViewMode
from app.service.broadcast_service import EventType

from app.views.step.button import BackButton, ChangeModeButton, CapturePositionButton, DiscardButton, SaveButton


# STEP VIEW
class StepView(ViewState):
    headers_to_fields_steps = {
        'Step ID': 'entry_id',
        'Parent ID': 'parent_id',
        'Name': 'name',
        'X Coordinate': 'x',
        'Y Coordinate': 'y',
        'Order': 'order',
        'Delay Type': 'delay_type',
        'Delay': 'delay',
        'Created Date': 'created_datetime',
        'Last Updated': 'last_update_datetime',
        'Attribute name': 'header'
    }
    def __init__(self,
                 view_type: ViewType,
                 view_mode: ViewMode,
                 parent=None,
                 child=None,
                 virtual_data=None):
        super().__init__(
            view_type=view_type,
            view_mode=view_mode,
            parent=parent,
            child=child,
            virtual_data=virtual_data)
        self.menu = MenuBar(menu_list=self.__define_buttons(), parent=self)
        self._register_listener(EventType.RENDER, self)
        self._broadcast(EventType.RENDER)

    def handle_event(self):
        """React to an event."""
        if self.active:  # Only react to 'enter_press'
            self.render()

    def render(self):
        max_lengths = self._calculate_max_lengths(self.virtual_data.wrapper)
        script_table_left_patting = int(len(max(self.headers_to_fields_steps.keys(), key=len)))
        self._render()
        print(Fore.BLACK + Back.WHITE + "    | Step details".ljust(150) + Style.RESET_ALL, end='\n')
        print(f'{Fore.BLACK + Back.WHITE}    {Style.RESET_ALL}| {"Attribute name".ljust(script_table_left_patting)} | Value', end='\n')
        [item.render(script_table_left_patting, int(max_lengths['step']['sum']/2)) for item in self.virtual_data.nodes if
         isinstance(item, DataNode)]

    def __define_buttons(self) -> List[MenuOption]:
        return [
            MenuOption(object_implementation=BackButton(view_state=self)),
            MenuOption(object_implementation=CapturePositionButton(view_state=self)),
            MenuOption(object_implementation=ChangeModeButton(view_state=self)),
            MenuOption(object_implementation=DiscardButton(view_state=self)),
            MenuOption(object_implementation=SaveButton(view_state=self))
        ]