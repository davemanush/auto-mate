from app.model.node import Node
from app.model.enums import MenuType
from app.model.view_state import ViewState, ViewType, ViewMode
from app.views.common.button_interface import ButtonInterface
from app.views.step.stepview import StepView


class DetailsButton(ButtonInterface):
    def __init__(self, view_state: ViewState):
        self.view_state = view_state
        self.menu_type = MenuType.DETAILS
        self.view_modes = [ViewMode.VIEW, ViewMode.EDIT]

    def action(self):
        self.view_state.deactivate_view()
        details_view_state = StepView(
            parent=self.view_state,
            view_type=ViewType.STEP_DETAILS,
            view_mode=self.view_state.view_mode,
            source=self.view_state.data_node.get_selected()
        )
        details_view_state.activate_view()
        self.view_state.child = details_view_state

    def condition(self):
        return self.view_state.active and self.view_state.view_mode in self.view_modes \
            and not self.view_state.data_node.get_selected().is_leaf()

    def show(self):
        if self.view_state.view_mode is ViewMode.VIEW:
            return self.get_data().text
        elif self.view_state.view_mode is ViewMode.EDIT:
            return self.get_type().override_text("Edit step")

    def get_type(self):
        return self.menu_type

    def get_data(self):
        return self.menu_type.value