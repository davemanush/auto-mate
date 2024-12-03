from app.model.data_node import DataNode
from app.model.composite_node import CompositeNode
from app.model.enums import MenuType
from app.model.view_state import ViewState, ViewMode
from app.views.button_interface import ButtonInterface


class DiscardButton(ButtonInterface):
    def __init__(self, view_state: ViewState):
        self.view_state = view_state
        self.menu_type = MenuType.DISCARD
        self.view_modes = [ViewMode.EDIT]

    def action(self):
        items_to_delete = []
        for item in self.view_state.virtual_data.wrapper:
            if isinstance(item, DataNode) and item.is_edited():
                item.discard_change()
            if isinstance(item, CompositeNode):
                if item.is_deleted():
                    item.restore()
                elif item.is_new():
                    items_to_delete.append(item)
                elif item.any_child_edited():
                    for child in item.nodes:
                        if child.is_edited():
                            child.discard_change()
        self.view_state.virtual_data.wrapper = [item for item in self.view_state.virtual_data.wrapper if item not in items_to_delete]

    def condition(self):
        return  self.view_state.active and self.view_state.view_mode in self.view_modes \
                and (
                        any([isinstance(item, DataNode) and item.is_edited() for item in self.view_state.virtual_data.wrapper])
                        or any([isinstance(item, CompositeNode) and item.is_edited() or item.is_deleted() or item.is_created() for item in self.view_state.virtual_data.wrapper])
                    )

    def show(self):
        return self.get_type().update_text("script")

    def get_type(self):
        return self.menu_type

    def get_data(self):
        return self.menu_type.value