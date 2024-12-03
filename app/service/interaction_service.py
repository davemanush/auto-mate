import os
from datetime import datetime

from pynput import keyboard
from app.model.data_node import DataUpdate, DataUpdateType
from app.model.enums import CursorDirectionType
from app.model.framework.broadcastable import Broadcastable
from app.service.broadcast_service import EventType

class InteractionService(Broadcastable):
    def __init__(self):
        super().__init__()
        self.create = datetime.now()
        with keyboard.Listener(on_press=lambda event: self.on_press(event)) as keyboard_listener:
            keyboard_listener.join()
            
    def on_press(self, key):
        try:
            match key.char:
                case 'í':
                    self._broadcast(EventType.ENTER_PRESS)
                    return
                case _:
                    if str(key.char).isalnum():
                        self._broadcast(EventType.USER_TYPING, DataUpdate(DataUpdateType.ADD, str(key.char)))
                    return
        except AttributeError:
            #print(e.with_traceback())
            ##render_screen(state.active_view_state)
            pass  # Handle special keys if needed
        try:
            match key.value.vk:
                case 65363:
                    ## RIGHT ARROW PRESS
                    self._broadcast(EventType.MENU_NAVIGATION, CursorDirectionType.RIGHT)
                case 65361:
                    ## LEFT ARROW PRESS
                    self._broadcast(EventType.MENU_NAVIGATION, CursorDirectionType.LEFT)
                case 65362:
                    ## UP ARROW PRESS
                    self._broadcast(EventType.DATA_NAVIGATION, CursorDirectionType.UP)
                case 65364:
                    ## DOWN ARROW PRESS
                    self._broadcast(EventType.DATA_NAVIGATION, CursorDirectionType.DOWN)
                case 65288:
                    ## RETURN / ERASE PRESS
                    self._broadcast(EventType.USER_TYPING, DataUpdate(DataUpdateType.DELETE, ""))
        except AttributeError:
            pass  # Handle special keys if needed
        except KeyboardInterrupt:
            exit(1)
