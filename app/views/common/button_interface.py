from abc import ABC, abstractmethod

from app.model.view_state import ViewState

class ButtonInterface(ABC):
    @abstractmethod
    def __init__(self, view_state: ViewState):
        pass

    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def condition(self):
        return False

    @abstractmethod
    def show(self):
        return ""

    @abstractmethod
    def get_data(self):
        return None

    @abstractmethod
    def get_type(self):
        return None