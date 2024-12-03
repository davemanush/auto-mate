from enum import Enum

from app.model.data.field.data_types import DataType
from app.model.framework.enhancement.renderable import Renderable
from app.model.framework.modifier.creatable import Creatable
from app.model.framework.modifier.deletable import Deletable
from app.model.framework.modifier.errorable import Errorable

class Editable(Renderable, Deletable, Creatable, Errorable):
    def __init__(self, clazz=None, source=None, data_type=None):
        super().__init__()
        Deletable.__init__(self)
        Creatable.__init__(self)
        Errorable.__init__(self)
        self.data_type: DataType = data_type
        if data_type is not None:
            self.virtual = str(source)
            self.source = str(source)
            self.clazz = clazz
        self.source = source

    def discard_change(self):
        self.virtual = self.source

    def get_data(self):
        return self.source

    def get_wrapper(self):
        return self.virtual

    def is_edited(self):
        if isinstance(self.source, str):
            return self.virtual != self.source

    def is_new(self):
        return self.new
