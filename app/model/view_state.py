from dependency_injector.wiring import inject

from app.model.node import Node
from app.model.framework.enhancement import Broadcastable
from app.model.framework.enums import ViewType, ViewMode
from app.model.framework.modifier.interactable import Interactable
from app.service.database_service import DatabaseService
from app.service.render_service import RenderService


class ViewState(Broadcastable, Interactable):
    @inject
    def __init__(
            self,
            view_type: ViewType,
            view_mode: ViewMode,
            menu=None,
            parent=None,
            child=None,
            source=None):
        Broadcastable.__init__(self)
        Interactable.__init__(self, parent=parent)
        self.render_service = RenderService()
        self.database_service = DatabaseService()
        self.view_type = view_type
        self.view_mode = view_mode
        self.menu = menu
        self.data = source.get_data() if source and source.get_data() is not None else self.database_service.get_all_scripts()
        self.data_node = source if source is not None else Node(
            parent=self,
            owner=self,
            source=self.data
        )
        self.data_node.sort_nodes()
        self.update_entry_owner()
        self.activate()
        self.data_node.activate()
        self.data_node.nodes[0].select()
        self.child = child

    def render_view(self):
        self.render_service.render(self)

    def activate_view(self):
        self.activate()
        self.menu.activate()
        self.data_node.activate_node()

    def deactivate_view(self):
        self.deactivate()
        self.menu.deactivate()
        self.data_node.deactivate_node()

    def update_entry_owner(self):
        self.data_node.update_node_owner(self)


