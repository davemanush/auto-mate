import os
from enum import Enum
from typing import List


class EventType(Enum):
    ENTER_PRESS = 1
    MENU_NAVIGATION = 2
    DATA_NAVIGATION = 3
    USER_TYPING = 4
    RENDER = 5

class BroadcastWrapper:
    def __init__(
            self,
            event_type: EventType,
            object):
        self.event_type = event_type
        self.object = object

class BroadcasterService:
    def __init__(self):
        self.listeners: List[BroadcastWrapper] = []  # Keep weak references to listeners

    def register_listener(self, event_type: EventType, listener):
        """Register a listener to this broadcaster."""
        self.listeners.append(BroadcastWrapper(event_type, listener))

    def unregister_listener(self, listener):
        """Unregister a listener."""
        self.listeners.remove(listener)

    def broadcast(self, event_name: EventType, *args, **kwargs):
        """Broadcast an event to all registered listeners."""
        for listener in list(self.listeners):
            if listener.event_type is event_name:
                if event_name is EventType.RENDER:
                    os.system('clear')
                    listener.object.handle_event()
                if event_name is EventType.MENU_NAVIGATION:
                    listener.object.handle_event(args[0])
                if event_name is EventType.DATA_NAVIGATION:
                    listener.object.handle_event(args[0])
                if event_name is EventType.ENTER_PRESS:
                    listener.object.handle_event()
                if event_name is EventType.USER_TYPING:
                    asd = self.listeners.index(listener)
                    listener.object.handle_event(args[0])
