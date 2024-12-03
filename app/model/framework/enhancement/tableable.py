from app.model.framework.modifier import Editable


class Tableable(Editable):
    def __init__(self, source=None, clazz=None,  data_type=None):
        Editable.__init__(self, source=source, clazz=clazz, data_type=data_type)
        if self.is_leaf():
            self.nodes = []
        return

    def is_leaf(self):
        return True if self.data_type is not None else False

    def get_data_node(self, data_type):
        return next((item for item in self.nodes if item.data_type == data_type), None)

    def is_edited(self):
        for node in self.nodes:
            if self.is_leaf() and node.is_edited():
                return True
        return False
