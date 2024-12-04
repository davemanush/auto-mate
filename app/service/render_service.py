## TODO render service and move ALL data into data table objects so it can be rendered dinamically
from colorama import Back, Fore, Style
from dependency_injector.wiring import inject

from app.model.framework.enums import ViewType, ViewMode
from app.model.table import ColumnHeaderData, CellData
from app.service.table_service import TableService


class RenderService:
    @inject
    def __init__(self):
       self.table_service = TableService()

    def render(self, view_state):
        self.__render_main_title()
        self.__render_menu(view_state.menu)
        self.__render_menu_separator()
        self.__mode_bar_render(view_state)
        self.__warning_bar_render(view_state)
        self.__render_section(view_state)

    def __render_main_title(self):
        print('Auto Mate - Automation support tool', end='\n\n')

    def __render_menu(self, menu_bar):
        for menu in menu_bar.get_menu_options():
            separator = '|'
            color = ''
            color_override = ''
            reset_color = Style.RESET_ALL
            if menu.get_data.style_override:
                color_override = menu.get_data.style_override
            if menu.selected:
                color = Back.LIGHTWHITE_EX + Fore.BLACK
            print(f"{color} {color_override}{menu.show()}{reset_color}{color} {reset_color}{separator}", end='')
        print('', end='\n')

    def __render_menu_separator(self):
        print(
            '-------------------------------------------------------------------------------------------------------------',
            end='\n')

    def __mode_bar_render(self, view_state):
        bg_color = ''
        fr_color = ''
        mode = ''
        view = ''
        if view_state.view_type is ViewType.APP:
            view = 'Script list'
        if view_state.view_type is ViewType.SCRIPT_DETAILS:
            view = 'Script details'
        if view_state.view_type is ViewType.STEP_DETAILS:
            view = 'Step details'
        if view_state.view_type is ViewType.SETTINGS:
            view = 'Settings'
        if view_state.view_mode is ViewMode.VIEW:
            bg_color = Back.GREEN
            fr_color = Fore.BLACK
            mode = 'view'
        if view_state.view_mode is ViewMode.EDIT:
            bg_color = Back.YELLOW
            fr_color = Fore.BLACK
            mode = 'edit'
        if view_state.view_mode is ViewMode.NEW:
            bg_color = Back.BLUE
            fr_color = Fore.BLACK
            mode = 'creation'
        print(f'{bg_color}{fr_color}{self.__center_text(view + " - " + mode + " mode", width=150)}{Style.RESET_ALL}', end='\n')

    def __warning_bar_render(self, item):
        critical_color = Back.LIGHTRED_EX + Fore.BLACK
        warning_color = Back.LIGHTYELLOW_EX + Fore.BLACK
        warnings = []
        if item.view_type == ViewType.APP and item.view_mode is ViewMode.VIEW and item.data_node.is_node_edited():
            warnings.append(critical_color + self.__center_text('Unsaved changes detected - Script run disabled', width=149) + Style.RESET_ALL)
        if item.view_type == ViewType.SCRIPT_DETAILS and item.view_mode is ViewMode.VIEW and item.data_node.is_node_edited():
            warnings.append(warning_color + self.__center_text('Unsaved changes detected', width=149) + Style.RESET_ALL)
        for warning in warnings:
            print(warning, end='\n')

    def __render_section(self, view_state):
        if view_state.view_type is ViewType.APP:
            print(Fore.BLACK + Back.WHITE + "    | Script List".ljust(149) + Style.RESET_ALL, end='\n')
            self.__render_table(self.table_service.init_table(view_state.data_node, False))
        elif view_state.view_type is ViewType.SCRIPT_DETAILS:
            print(Fore.BLACK + Back.WHITE + "    | Script Details".ljust(149) + Style.RESET_ALL, end='\n')
            self.__render_table(self.table_service.init_table(view_state.data_node, True))
            print(Fore.BLACK + Back.WHITE + "    | Step List".ljust(149) + Style.RESET_ALL, end='\n')
            self.__render_table(self.table_service.init_table(view_state.data_node, False))
        elif view_state.view_type is ViewType.STEP_DETAILS:
            print(Fore.BLACK + Back.WHITE + "    | Step Details".ljust(149) + Style.RESET_ALL, end='\n')
            self.__render_table(self.table_service.init_table(view_state.data_node, True))

    def __render_table(self, table):
        table_width_last_index = len(table) - 1
        for row in range(len(table[0])):
            line = f"{self.__render_cursor(table[0][row].modifier.is_cursor if row > 0 else False)} "
            for index, column in enumerate(table):
                if index == len(table) and row == 0:
                    continue
                cell = column[row]
                column_max_length = column[0].max_length
                if isinstance(cell, ColumnHeaderData) and index != table_width_last_index :
                    line += f"| {cell.data.ljust(column_max_length)} "
                elif isinstance(cell, CellData) and index != table_width_last_index:
                    line += f"| {cell.modifier.style}{cell.data.ljust(column_max_length)}{Style.RESET_ALL} {cell.modifier.message if cell.modifier.message and index == table_width_last_index else ''}"
            print(line, end='\n')

    def __render_cursor(self, selected):
        if selected:
            return Back.LIGHTWHITE_EX + Fore.BLACK + ">>>" + Style.RESET_ALL
        return "   "

    def __center_text(self, text, width=150):
        padding = (width - len(text)) // 2
        return ' ' * padding + text + ' ' * padding
