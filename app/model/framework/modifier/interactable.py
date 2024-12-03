from app.model.framework.modifier.activatable import Activatable
from app.model.framework.modifier.ownable import Ownable
from app.model.framework.modifier.selectable import Selectable


class Interactable(Activatable, Selectable, Ownable):
    def __init__(self, owner=None, parent=None):
        Ownable.__init__(self, owner=owner, parent=parent)
        Activatable.__init__(self)
        Selectable.__init__(self)
