from app.model.node import Node
from app.model.enums import MenuType
from app.model.step import Step
from app.model.view_state import ViewState, ViewType, ViewMode
from app.views.common.button_interface import ButtonInterface
from app.views.step.stepview import StepView


class AddButton(ButtonInterface):
    def __init__(self, view_state: ViewState):
        self.view_state = view_state
        self.menu_type = MenuType.ADD
        self.view_modes = [ViewMode.EDIT]

    def action(self):
        self.view_state.deactivate()
        self.view_state.data_node.get_selected().deactivate()
        details_view_state = StepView(
            parent=self.view_state,
            view_type=ViewType.STEP_DETAILS,
            view_mode=ViewMode.NEW,
            source=Node(
                parent=self.view_state.data_node.get_selected(),
                owner=self.view_state,
                entry=Step(
                    parent_id=self.view_state.data_node.get_selected().parent.id,
                    order=0
                )
            )
        )
        self.view_state.child = details_view_state

    def condition(self):
        return self.view_state.active and self.view_state.view_mode in self.view_modes

    def show(self):
        return self.get_data().text

    def get_type(self):
        return self.menu_type

    def get_data(self):
        return self.menu_type.value