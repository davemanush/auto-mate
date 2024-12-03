from typing import Union, List

from colorama import Style, Fore, Back

from app.model.data.field.data_types import DataType
from app.model.entry import Entry
from app.model.framework.enhancement import Renderable
from app.model.framework.enhancement.nodeable import Nodeable
from app.model.script import Script
from app.model.step import Step
from app.service.database_service import DatabaseService


class Node(Nodeable, Renderable):
    def __init__(self, node_id=None, source=None, data_type=None, order=0, owner=None, parent=None):
        self.database_service = DatabaseService()
        Nodeable.__init__(self, node_id=node_id, data_type=data_type, source=source, order=order, clazz=type(source), owner=owner, parent=parent)
        Renderable.__init__(self)
        if isinstance(source, list):
            self.nodes = [Node(source=node_source, owner=owner, parent=self) for node_source in source]
        elif isinstance(source, Entry):
            self.nodes = self.init_node(source=source)
            self.sort_nodes()

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

    def save(self):
        for data in self.nodes:
            if data.changed:
                if isinstance(self.nodes, Script):
                    self.nodes.__setattr__(DataType.find_by_attribute_name(data.name).get_data().get_name(), data.nodes)
                if isinstance(self.nodes, Step):
                    self.nodes.__setattr__(DataType.find_by_attribute_name(data.name).get_data().get_name(), data.nodes)
        self.nodes.save()

    def render(self, max_lengths):
        if self.clazz is Script:
            entry_id_nodes = self.return_nodes_entry(DataType.ID.get_data().get_name())
            name_nodes = self.return_nodes_entry(DataType.NAME.get_data().get_name())
            last_update_datetime_nodes = self.return_nodes_entry(DataType.LAST_UPDATE_DATETIME.get_data().get_name())
            last_run_datetime_nodes = self.return_nodes_entry(DataType.LAST_RUN_DATETIME.get_data().get_name())

            entry_id = entry_id_nodes.wrapper if entry_id_nodes else ''
            name = name_nodes.wrapper if name_nodes else ''
            total_steps = str(len(self.return_nodes_list(Node)))
            last_update_datetime = last_update_datetime_nodes.wrapper if last_update_datetime_nodes else ''
            last_run_datetime = last_run_datetime_nodes.wrapper if last_run_datetime_nodes else ''
            ## TODO add dynamic dta render by the DataType show_in_list and show_in_details attributes
            print(
                f"{self._render_cursor()} | "
                f"{entry_id.ljust(max_lengths['entry_id'])} | "
                f"{name.ljust(max_lengths['name'])} | "
                f"{total_steps.ljust(max_lengths['total_steps'])} | "
                f"{last_update_datetime.ljust(max_lengths['last_update_datetime']) 
                    if last_update_datetime is not None or last_update_datetime == '' else ''.ljust(max_lengths['last_update_datetime'])} | ",
                f"{last_run_datetime.ljust(max_lengths['last_run_datetime'])
                if last_run_datetime is not None or last_run_datetime == '' else ''.ljust(max_lengths['last_run_datetime'])}| ",
                f"{self._render_modifier(self)}",
                end='\n')
        if self.clazz is Step:
            print(
                f"{self._render_cursor()} | "
                f"{self.render_field(DataType.ID.get_data().get_name(), max_lengths)} | "
                f"{self.render_field(DataType.NAME.get_data().get_name(), max_lengths)} | "
                f"{self.render_field(DataType.LAST_UPDATE_DATETIME.get_data().get_name(), max_lengths)} | "
                f"{self._render_modifier(self)}",
                end='\n')

    def render_field(self, field_name, max_lengths):
        color = ''
        field_nodes = self.return_nodes_entry(field_name)
        field = field_nodes.wrapper if field_nodes else ''
        if field_nodes and field_nodes.is_edited() and not field_nodes.parent.is_created():
            color = Back.YELLOW + Fore.BLACK
        return color + field.ljust(max_lengths.get(field_nodes.data_type.get_data().get_name())) + Style.RESET_ALL