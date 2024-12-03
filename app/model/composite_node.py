from typing import Union, List

from colorama import Style, Fore, Back

from app.model.data_node import DataNode
from app.model.data.data_types import DataType
from app.model.enums import CursorDirectionType
from app.model.framework.ownable import Ownable
from app.model.framework.editable import Editable
from app.model.script import Script
from app.model.step import Step
from app.service.broadcast_service import EventType
from app.service.database_service import DatabaseService


class CompositeNode(Editable, Ownable):
    def __init__(self, owner, parent, entry):
        Editable.__init__(self, original=entry, virtual_data=[], clazz=type(entry))
        Ownable.__init__(self, owner=owner)
        self.parent = parent
        self.owner = owner
        self.database_service = DatabaseService()
        self.order = entry.order if not isinstance(entry, list) else 0
        self.id = entry.entry_id if not isinstance(entry, list) else ""
        self.nodes: List[Union[CompositeNode | DataNode]] = []
        if isinstance(entry, Script | Step):
            self.nodes = self.create_child_entries(entry=entry, owner=owner)
        if isinstance(entry, list):
            self.nodes = [CompositeNode(entry=script_data, owner=owner, parent=self) for script_data in entry]
        self.sort_data()
        if len(self.nodes) > 0:
            self.nodes[0].select()
            self._register_listener(EventType.DATA_NAVIGATION, self)

    def sort_data(self):
        self.nodes = ([item for item in self.nodes if isinstance(item, DataNode)]
                      + sorted([item for item in self.nodes if isinstance(item, CompositeNode)], key=lambda entry: entry.order))

    def create_child_entries(self, entry: Script | Step, owner):
        entry_list = []
        for attr in entry.__dict__.keys():
            if isinstance(entry.__getattribute__(attr), list):
                for entry_data in entry.__getattribute__(attr):
                    entry_list.append(CompositeNode(entry=entry_data, parent=self, owner=owner))
            else:
                if entry.__getattribute__(attr) is not None:
                    entry_data = entry.__getattribute__(attr)
                    new_data_nodes = DataNode(
                        parent=self,
                        owner=owner,
                        original=entry_data,
                        virtual_data=entry_data,
                        data_type=DataType.find_by_attribute_name(name=attr),
                        clazz=type(entry)
                    )
                    entry_list.append(new_data_nodes)
        return entry_list

    def update_branch_owner(self, owner):
        self.owner = owner
        for data in self.nodes:
            data.update_owner(owner)

    ##activates the whole branch but this is not default behaviour
    def activate_branch(self):
        self.activate()
        for node in self.nodes:
            node.activate_branch()

    def activate_node(self):
        self.activate()
        for node in self.nodes:
            node.activate()

    def clear_validation_errors(self):
        for node in self.nodes:
            node.clear_error()

    ##deactivates the whole branch
    def deactivate(self):
        if self.nodes:
            for node in self.nodes:
                node.deactivate()
                return
        if not self.is_active():
            self.deactivate()
        return

    def discard_changes(self):
        for data in self.nodes:
            if isinstance(data, DataNode) and data.is_edited():
                data.discard_change()
            if isinstance(data, CompositeNode):
                self.delete_new_children()
                data.discard_changes()

    def delete_new_children(self):
        items_to_delete = []
        for data in self.nodes:
            if isinstance(data, CompositeNode) and data.is_new():
                items_to_delete.append(data)
        self.nodes = [item for item in self.nodes if item not in items_to_delete]

    def return_nodes_entry(self, data_type: DataType):
        for data in self.nodes:
            if isinstance(data, DataNode) and data.data_type == DataType.find_by_attribute_name(data_type):
                return data
        return None

    def return_nodes_list(self, clazz):
        return [item for item in self.nodes if isinstance(item, clazz)]

    def reset_state(self):
        if self.is_deleted():
            self.restore()

    def handle_event(self, direction: CursorDirectionType):
        """React to an event."""
        if self.owner.active:
            self.update_active_data(direction)

    def update_active_data(self, direction: CursorDirectionType):
        active_data: DataNode | CompositeNode = self.get_selected()
        active_index = self.nodes.index(active_data)
        if direction == CursorDirectionType.UP:
            if not active_index - 1 < 0:
                new_active_data: Union[DataNode | CompositeNode] = self.nodes[active_index - 1]
                new_active_data.select()
                active_data.unselect()
        if direction == CursorDirectionType.DOWN:
            if not active_index + 1 > len(self.nodes) - 1:
                new_active_data: Union[DataNode | CompositeNode] = self.nodes[active_index + 1]
                new_active_data.select()
                active_data.unselect()
        ## broadcast the event to update the menu
        self._broadcast(EventType.MENU_NAVIGATION, CursorDirectionType.NONE)

    def save(self):
        for data in self.nodes:
            if data.changed:
                if isinstance(self.nodes, Script):
                    self.nodes.__setattr__(DataType.find_by_attribute_name(data.name).get_data().get_name(), data.nodes)
                if isinstance(self.nodes, Step):
                    self.nodes.__setattr__(DataType.find_by_attribute_name(data.name).get_data().get_name(), data.nodes)
        self.nodes.save()

    def get_data_node(self, data_type: DataType) -> DataNode:
        return next((item for item in self.nodes if isinstance(item, DataNode) and item.data_type == data_type), None)

    def any_child_edited(self):
        for node in self.nodes:
            if isinstance(node, DataNode) and node.is_edited():
                return True
            if isinstance(node, CompositeNode) and node.any_child_edited():
                return True
        return False

    def get_selected(self):
        return next((item for item in self.nodes if item.selected), None)

    def render(self, max_lengths):
        if self.clazz is Script:
            entry_id_nodes = self.return_nodes_entry(DataType.ID.get_data().get_name())
            name_nodes = self.return_nodes_entry(DataType.NAME.get_data().get_name())
            last_update_datetime_nodes = self.return_nodes_entry(DataType.LAST_UPDATE_DATETIME.get_data().get_name())
            last_run_datetime_nodes = self.return_nodes_entry(DataType.LAST_RUN_DATETIME.get_data().get_name())

            entry_id = entry_id_nodes.wrapper if entry_id_nodes else ''
            name = name_nodes.wrapper if name_nodes else ''
            total_steps = str(len(self.return_nodes_list(CompositeNode)))
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