from typing import List
from colorama import Back, Fore, Style

from app.model.enums import ConfirmOption
def render_confirm_options_list(view_state):
    confirm_options: List[ConfirmOption] = view_state.wrapper
    for index, option in enumerate(confirm_options):
        bg_color = ''
        fr_color = ''
        reset_color = Style.RESET_ALL
        if view_state.active_data == option:
            bg_color = Back.LIGHTWHITE_EX
            fr_color = Fore.BLACK
        print(f'> {fr_color}{bg_color}{option.value}{reset_color}', end='\n')
