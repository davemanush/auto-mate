import os

from app.service import DependencyContainer, InteractionService
from app.views.main import MainView

def start_app():
    container = DependencyContainer()
    container.wire(modules=["__main__", "app.model.framework.broadcastable"])
    MainView()
    InteractionService()

if __name__ == "__main__":
    os.environ['TERM'] = 'xterm-256color'
    os.system('clear')
    start_app()
