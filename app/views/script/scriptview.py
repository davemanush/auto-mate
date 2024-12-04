from typing import List

from colorama import Fore, Back, Style

from app.model.node import Node
from app.model.menu.menu_bar import MenuBar
from app.model.menu.menu_option import MenuOption
from app.model.view_state import ViewState, ViewType, ViewMode
from app.service.broadcast_service import EventType
from app.views.script.button import AddButton, BackButton, ChangeModeButton, DeleteButton, DetailsButton, DiscardButton, \
    DryRunButton, EditButton, RestoreButton, SaveButton

class ScriptView(ViewState):
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
                 source=None):
        super().__init__(
            view_type=view_type,
            view_mode=view_mode,
            parent=parent,
            child=child,
            source=source)
        self.menu = MenuBar(menu_list=self.__define_buttons(), parent=self)
        self._register_listener(EventType.RENDER, self)
        self.activate_view()
        self.data_node.nodes[0].select()
        self.broadcaster.broadcast(EventType.RENDER)

    def handle_event(self):
        """React to an event."""
        if self.active:  # Only react to 'enter_press'
            self.render()

    def render(self):
        self.render_service.render(self)

    def __define_buttons(self) -> List[MenuOption]:
        return [
            MenuOption(object_implementation=AddButton(view_state=self)),
            MenuOption(object_implementation=BackButton(view_state=self)),
            MenuOption(object_implementation=ChangeModeButton(view_state=self)),
            MenuOption(object_implementation=DeleteButton(view_state=self)),
            MenuOption(object_implementation=DetailsButton(view_state=self)),

            ## EDIT MENU
            MenuOption(object_implementation=DiscardButton(view_state=self)),
            MenuOption(object_implementation=DryRunButton(view_state=self)),
            #MenuOption(object_implementation=EditButton(view_state=self)),
            MenuOption(object_implementation=RestoreButton(view_state=self)),
            MenuOption(object_implementation=SaveButton(view_state=self))
        ]