from colorama import Back, Fore, Style
from dependency_injector.wiring import inject, Provide
from app.model.framework.enums import ViewType, ViewMode
from app.service import DependencyContainer
from app.service.render_service import RenderService


class Renderable:
    @inject
    def __init__(self, render_service: RenderService = Provide[DependencyContainer.render_service]):
        self.render_service = render_service

    def render(self):
        self.render_service.render()

    def _print_tabs(self, amount: int):
        tabs = ''
        for x in range(0, amount):
            tabs += '\t'
        return tabs

    def _render_main_title(self):
        print('Auto Mate - Automation support tool', end='\n\n')

    def _render_cursor(self):
        if self.selected:
            return Back.LIGHTWHITE_EX + Fore.BLACK + ">>>" + Style.RESET_ALL
        return "   "

    def _render_menu_separator(self):
        print(
            '-------------------------------------------------------------------------------------------------------------',
            end='\n')
    def _center_text(self, text, width=150):
        padding = (width - len(text)) // 2
        return ' ' * padding + text + ' ' * padding

    def _warning_bar_render(self, item):
        critical_color = Back.LIGHTRED_EX + Fore.BLACK
        warning_color = Back.LIGHTYELLOW_EX + Fore.BLACK
        warnings = []
        if item.view_type == ViewType.APP and item.view_mode is ViewMode.VIEW and item.data_node.any_child_edited():
            warnings.append(critical_color + self._center_text('Unsaved changes detected - Script run disabled', width=149) + Style.RESET_ALL)
        if item.view_type == ViewType.SCRIPT_DETAILS and item.view_mode is ViewMode.VIEW and item.data_node.any_child_edited():
            warnings.append(warning_color + self._center_text('Unsaved changes detected', width=149) + Style.RESET_ALL)
        for warning in warnings:
            print(warning, end='\n')

    def _render_modifier(self, item):
        if self.has_error():
            return Back.LIGHTRED_EX + Fore.BLACK + '<validation error>' + Style.RESET_ALL + ' ' + item.validation_error
        if self.is_deleted():
            return Back.RED + Fore.BLACK + '<deleted>' + Style.RESET_ALL
        if item.data_type is not None and item.data_type.get_data().is_read_only():
            return Back.LIGHTWHITE_EX + Fore.BLACK + '<read only>' + Style.RESET_ALL
        if item.is_created():
            return Back.BLUE + Fore.BLACK + '<new>' + Style.RESET_ALL
        if (item.nodes and item.any_child_edited()) \
            or (not item.nodes and item.virtual and item.is_edited()):
            return Back.YELLOW + Fore.BLACK + '<edited>' + Style.RESET_ALL


        return ''