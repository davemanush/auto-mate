from app.model.composite_node import CompositeNode
from app.model.enums import MenuType
from app.model.view_state import ViewState, ViewMode
from app.views.button_interface import ButtonInterface


class DeleteButton(ButtonInterface):
    def __init__(self, view_state: ViewState):
        self.view_state = view_state
        self.menu_type = MenuType.DELETE
        self.view_modes = [ViewMode.EDIT]

    def action(self):
        self.view_state.virtual_data.get_selected().delete()

    def condition(self):
        return self.view_state.active and self.view_state.view_mode in self.view_modes \
            and isinstance(self.view_state.virtual_data.get_selected(), CompositeNode) \
            and not self.view_state.virtual_data.get_selected().is_deleted()

    def show(self):
        return self.get_type().update_text("step")

    def get_type(self):
        return self.menu_type

    def get_data(self):
        return self.menu_type.value