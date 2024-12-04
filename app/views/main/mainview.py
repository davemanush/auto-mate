from typing import List

from app.model.menu.menu_bar import MenuBar
from app.model.menu.menu_option import MenuOption
from app.model.view_state import ViewState, ViewType, ViewMode
from app.service.broadcast_service import EventType
from app.views.main.button import StartButton, DetailsButton, ChangeModeButton, SettingsButton, \
    QuitButton, NewButton, SaveButton, MoveUpButton, MoveDownButton, DeleteButton, \
    RestoreButton


class MainView(ViewState):
    def __init__(self):
        super().__init__(
            view_type=ViewType.APP,
            view_mode=ViewMode.VIEW
        )
        self.menu = MenuBar(menu_list=self.define_buttons(), parent=self)
        self.activate_view()
        self._register_listener(EventType.RENDER, self)
        self.data_node.nodes[0].select()
        self._broadcast(EventType.RENDER)

    def handle_event(self):
        """React to an event."""
        if self.active:  # Only react to 'enter_press'
            self.render()

    def render(self):
        self.render_view()

    def define_buttons(self) -> List[MenuOption]:
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