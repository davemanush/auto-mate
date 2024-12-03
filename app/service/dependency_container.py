from dependency_injector import containers, providers
from app.service.broadcast_service import BroadcasterService
from app.service.render_service import RenderService


class DependencyContainer(containers.DeclarativeContainer):
    broadcaster_service = providers.Singleton(BroadcasterService)
    render_service = providers.Singleton(RenderService)