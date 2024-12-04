from colorama import Style, Fore, Back

from app.model.data.field.data_types import DataType
from app.model.entry import Entry
from app.model.framework.enhancement.nodeable import Nodeable
from app.model.script import Script
from app.model.step import Step
from app.service.broadcast_service import EventType
from app.service.database_service import DatabaseService


class Node(Nodeable):
    def __init__(self, node_id=None, source=None, data_type=None, order=0, owner=None, parent=None):
        self.database_service = DatabaseService()
        Nodeable.__init__(self, node_id=node_id, data_type=data_type, source=source, order=order, clazz=type(source), owner=owner, parent=parent)
        if isinstance(source, list):
            self.nodes = [Node(source=node_source, owner=owner, parent=self) for node_source in source]
        elif isinstance(source, Entry):
            self.nodes = self.init_node(source=source)
            self.order = source.order
            self.sort_nodes()
        self._register_node_listeners()

    def init_node(self, source):
        entry_list = []
        for source_attribute in source.__dict__.keys():
            source_attribute_value = source.__getattribute__(source_attribute)
            if isinstance(source_attribute_value, list):
                for entry_data in source_attribute_value:
                    entry_list.append(
                        Node(source=entry_data, parent=self, owner=self.owner, order=source.order)
                    )
            else:
                if source_attribute_value is not None:
                    new_node = Node(
                        node_id=source.entry_id,
                        parent=self,
                        owner=self.owner,
                        source=source_attribute_value,
                        data_type=DataType.find_by_attribute_name(name=source_attribute),
                        order=0 # TODO add order to datatype object
                    )
                    entry_list.append(
                        new_node
                    )
        return entry_list

    def _register_node_listeners(self):
        if self.is_leaf() and not self.data_type.get_data().is_read_only():
            self._register_listener(EventType.USER_TYPING, self)
        if not self.is_leaf() and self.nodes:
            self._register_listener(EventType.DATA_NAVIGATION, self)

    def save(self):
        for data in self.nodes:
            if data.changed:
                if isinstance(self.nodes, Script):
                    self.nodes.__setattr__(DataType.find_by_attribute_name(data.name).get_data().get_name(), data.nodes)
                if isinstance(self.nodes, Step):
                    self.nodes.__setattr__(DataType.find_by_attribute_name(data.name).get_data().get_name(), data.nodes)
        self.nodes.save()