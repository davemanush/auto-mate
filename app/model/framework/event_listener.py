from app.service.broadcast_service import BroadcasterService

class EventListener:
    def __init__(self, broadcast: BroadcasterService):
        self.listener = broadcast