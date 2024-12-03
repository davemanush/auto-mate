from dependency_injector import containers, providers
from app.service.broadcast_service import BroadcasterService

class DependencyContainer(containers.DeclarativeContainer):
    broadcaster_service = providers.Singleton(BroadcasterService)