from app.model.table import CellData


class ColumnHeaderData(CellData):
    def __init__(self, data, max_length, order=0, column_order=0, modifier=None):
        super().__init__(data, modifier, order)
        self.max_length = max_length
        self.column_order = column_order
