from typing import List
from colorama import Back, Fore

from app.model.data.field.data_types import DataType
from app.model.node import Node
from app.model.script import Script
from app.model.step import Step
from app.model.table import ColumnHeaderData, CellData, CellModifierData

class TableService:
    def __init__(self):
        pass

    def init_table(self, node, search_leafs):
        table = []
        data_type_list = []

        if isinstance(node.source, list):
            data_type_list = self.__get_default_script_data_list()
        elif isinstance(node.source, Script):
            data_type_list = self.__get_default_script_data_list()
        elif isinstance(node.source, Step):
            data_type_list = self.__get_defult_step_details_list()
        if not search_leafs:
            sorted_child_list: List[Node] = sorted([child for child in node.nodes if child.is_leaf() == search_leafs], key=lambda child: child.order)
            table = self.get_node_table(data_type_list, sorted_child_list)
        else:
            table = self.get_attribute_table(data_type_list, node)
        return table

    def get_attribute_table(self, data_type_list, node):
        attribute_list = [ColumnHeaderData(data="Attribute", modifier=CellModifierData(), max_length=0, column_order=0, order=0)]
        value_list = [ColumnHeaderData(data="Field Value", modifier=CellModifierData(), max_length=0, column_order=1, order=0)]
        row_modifier_list = [ColumnHeaderData(data='', max_length=0, modifier=CellModifierData(), column_order=99999, order=0)]
        for index, data_type in enumerate(data_type_list):
            leaf_with_type = node.get_data_node(data_type)
            if leaf_with_type is not None:
                attribute_list.append(ColumnHeaderData(data=data_type.get_data().get_display_name(), modifier=self.add_cell_modifier(node=node, selected=leaf_with_type.is_selected(), index=index).modifier, max_length=0, column_order=0, order=index + 1))
                value_list.append(CellData(data=leaf_with_type.get_virtual(), modifier=self.add_cell_modifier(node=node, selected=leaf_with_type.is_selected(), index=index).modifier, order=index + 1))
                row_modifier_list.append(self.add_cell_modifier(node=leaf_with_type, selected=leaf_with_type.is_selected(), index=index + 1))
            #else:
                #TODO We are not showing not existing attributes, but later with custom fields we will have to show them and make a node out of them.
                #attribute_list.append([ColumnHeaderData(data=data_type.get_data().get_display_name(), modifier=CellModifierData(), max_length=0, column_order=0, order=index + 1)])
                #value_list.append([ColumnHeaderData(data='', modifier=CellModifierData(), max_length=0, column_order=1, order=index + 1)])
                #row_modifier_list.append(self.__add_cell_modifier(leaf_with_type, leaf_with_type.is_selected(), index + 1))
        return [attribute_list, value_list, row_modifier_list]

    def get_node_table(self, data_type_list, sorted_child_list):
        node_table = []
        for index, data_type in enumerate(data_type_list):
            column = [ColumnHeaderData(data=data_type.get_data().get_display_name(), modifier=CellModifierData(), max_length=0, column_order=index, order=0)]
            for row_index, sorted_node in enumerate(sorted_child_list):
                data_node = sorted_node.get_data_node(data_type)
                if data_node is not None:
                    self.__append_column(data_type=data_type, node=data_node, column=column, index=row_index+1, selected=sorted_node.is_selected())
                else:
                    column.append(CellData(data='', modifier=CellModifierData(), order=row_index+1))
            column = sorted(column, key=lambda x: x.order)
            node_table.append(column)
        self.__row_modifier(sorted_child_list, node_table, selected=False)
        sorted(node_table, key=lambda x: x[0].order)
        return node_table

    def __append_column(self, data_type, node, column, index, selected):
        column[0].max_length = max(column[0].max_length, len(node.get_virtual()))
        if data_type == node.data_type:
            column.append(CellData(data=node.get_virtual(), modifier=self.add_cell_modifier(node=node, selected=selected, index=index).modifier, order=index))

    def __row_modifier(self, sorted_child_list, table, selected):
        modifier_column = [ColumnHeaderData(data='', max_length=0, modifier=CellModifierData(), column_order=99999)]
        for index, leaf in enumerate(sorted_child_list):
            modifier_column.append(self.add_cell_modifier(node=leaf, index=index + 1, selected=selected))
        table.append(modifier_column)

    def add_cell_modifier(self, node, selected, index=0):
        if node.has_error():
            return CellData(data='<validation error>', modifier=CellModifierData(style=Back.LIGHTRED_EX + Fore.BLACK, is_cursor=selected, message=node.validation_error), order=index)
        if node.is_deleted():
            return CellData(data='<deleted>', modifier=CellModifierData(Back.RED + Fore.BLACK, is_cursor=selected), order=index)
        if node.data_type is not None and node.data_type.get_data().is_read_only():
            return CellData(data='<read_only>', modifier=CellModifierData(style=Back.LIGHTWHITE_EX + Fore.BLACK, is_cursor=selected), order=index)
        if node.is_created():
            return CellData(data='<new>', modifier=CellModifierData(style=Back.BLUE + Fore.BLACK, is_cursor=selected), order=index)
        if node.is_edited():
            return CellData(data='<edited>', modifier=CellModifierData(style=Back.YELLOW + Fore.BLACK, is_cursor=selected), order=index)
        return CellData(data='', modifier=CellModifierData(style='', is_cursor=selected), order=index)

    def __get_default_script_data_list(self):
        return [DataType.ID, DataType.NAME, DataType.CREATED_DATETIME, DataType.LAST_RUN_DATETIME]

    def __get_defult_step_data_list(self):
        return [DataType.ORDER, DataType.ID, DataType.NAME, DataType.DELAY, DataType.DELAY_TYPE, DataType.LAST_UPDATE_DATETIME]

    def __get_defult_step_details_list(self):
        return [DataType.ID, DataType.NAME, DataType.ORDER, DataType.X, DataType.Y, DataType.DELAY, DataType.DELAY_TYPE, DataType.CREATED_DATETIME, DataType.LAST_UPDATE_DATETIME]