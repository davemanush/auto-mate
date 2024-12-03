from dependency_injector.wiring import Provide, inject

from app.service import DependencyContainer
from app.service.broadcast_service import EventType, BroadcasterService

class Broadcastable:
    @inject
    def __init__(self, broadcaster_service: BroadcasterService = Provide[DependencyContainer.broadcaster_service]):
        self.broadcaster: BroadcasterService = broadcaster_service

    def _get_broadcastable(self):
        return self.broadcaster

    def _register_listener(self, event_type: EventType, listener):
        self.broadcaster.register_listener(event_type, listener)

    def _remove_listener(self, listener):
        self.broadcaster.unregister_listener(listener)

    def _broadcast(self, event_name: EventType, *args, **kwargs):
        self.broadcaster.broadcast(event_name, *args, **kwargs)