from typing import List, Union

from colorama import Back, Fore, Style
from dependency_injector.wiring import inject

from app.model.node import Node
from app.model.framework.enhancement import Broadcastable
from app.model.framework.enums import ViewType, ViewMode
from app.model.framework.enhancement.renderable import Renderable
from app.model.framework.modifier.interactable import Interactable
from app.model.step import Step
from app.service.database_service import DatabaseService

class ViewState(Renderable, Broadcastable, Interactable):
    max_lengths = {
            'script': {
                'entry_id': 0,
                'name': 0,
                'order': 0,
                'last_update_datetime': 0,
                'created_datetime': 0,
                'last_run_datetime': 0,
                'sum': 0
            },
            'step': {
                'entry_id': 0,
                'parent_id': 0,
                'name': 0,
                'x': 0,
                'y': 0,
                'order': 0,
                'delay_type': 0,
                'delay': 0,
                'created_datetime': 0,
                'last_update_datetime': 0,
                'sum': 0
            }
        }
    @inject
    def __init__(
            self,
            view_type: ViewType,
            view_mode: ViewMode,
            menu=None,
            parent=None,
            child=None,
            source=None):
        Renderable.__init__(self)
        Broadcastable.__init__(self)
        Interactable.__init__(self, parent=parent)
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
        self.update_entry_owner()
        self.activate()
        self.data_node.activate()
        self.child = child

    def activate_view(self):
        self.activate()
        self.menu.activate()
        self.data_node.activate_node()

    def deactivate_view(self):
        self.deactivate()
        self.menu.deactivate()
        self.data_node.deactivate()

    def update_entry_owner(self):
        self.data_node.update_node_owner(self)

    def _render(self):
        self._render_main_title()
        self.menu.render()
        self._render_menu_separator()
        self.__mode_bar_render()
        self._warning_bar_render(self)



    def _init_max_lengths(self, object_type, headers_to_fields):
        if object_type == 'script':
            for header, field in headers_to_fields.items():
                self.max_lengths['script'][field] = len(header)
        elif object_type == 'step':
            for header, field in headers_to_fields.items():
                self.max_lengths['step'][field] = len(header)
        return self.max_lengths

    def _calculate_max_lengths(self, data_list: List[Node]):
        for item in filter(lambda entry: isinstance(entry, Node), data_list):
            if isinstance(item, Node):
                for entry in filter(lambda x: isinstance(x,Node), item.nodes):
                    self.__add_data_wrapper_lengths(entry, self.max_lengths)
            if isinstance(item, Node):
                self.__add_data_wrapper_lengths(item, self.max_lengths)
        self.max_lengths['script']['sum'] = sum(self.max_lengths['script'].values()) - self.max_lengths['script']['sum']
        self.max_lengths['step']['sum'] = sum(self.max_lengths['step'].values()) - self.max_lengths['step']['sum']
        return self.max_lengths

    def __add_data_wrapper_lengths(self, item, max_lengths):
            length_type = 'step' if item.clazz == Step else 'script'
            max_lengths[length_type][item.data_type.get_data().get_name()] = max(max_lengths[length_type][item.data_type.get_data().get_name()], len(str(item.virtual)))



    def __mode_bar_render(self):
        bg_color = ''
        fr_color = ''
        mode = ''
        view = ''
        if self.view_type is ViewType.APP:
            view = 'Script list'
        if self.view_type is ViewType.SCRIPT_DETAILS:
            view = 'Script details'
        if self.view_type is ViewType.STEP_DETAILS:
            view = 'Step details'
        if self.view_type is ViewType.SETTINGS:
            view = 'Settings'
        if self.view_mode is ViewMode.VIEW:
            bg_color = Back.GREEN
            fr_color = Fore.BLACK
            mode = 'view'
        if self.view_mode is ViewMode.EDIT:
            bg_color = Back.YELLOW
            fr_color = Fore.BLACK
            mode = 'edit'
        if self.view_mode is ViewMode.NEW:
            bg_color = Back.BLUE
            fr_color = Fore.BLACK
            mode = 'creation'
        print(f'{bg_color}{fr_color}{self._center_text(view + " - " + mode + " mode", width=150)}{Style.RESET_ALL}', end='\n')
