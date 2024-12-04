from enum import Enum
from wsgiref.validate import validator

from app.model.data.field.render import default_render, datetime_render, delay_render
from app.model.data.field.validator import is_valid_uuid, is_valid_number, is_valid_delay_type, \
    is_valid_datetime, is_valid_string


class DataTypeData:
    def __init__(self, name: str, display_name: str, read_only: bool, show_in_details: bool, show_in_list: bool):
        self.name = name
        self.display_name = display_name
        self.read_only = read_only
        self.show_in_details = show_in_details
        self.show_in_list = show_in_list
    def get_name(self):
        return self.name
    def get_display_name(self):
        return self.display_name
    def is_read_only(self):
        return self.read_only
    def is_in_details(self):
        return self.show_in_details
    def is_in_list(self):
        return self.show_in_list

## TODO REFACTOR: Remove the enum part and make it a list of objects, also add if it can be a step or a script, since from the settings we will be able to add mode fields
class DataType(Enum):
    ID = (DataTypeData(name="entry_id", display_name="Entity ID", read_only=True, show_in_details=True, show_in_list=False), is_valid_uuid, "UUID format is not valid")
    PARENT_ID = (DataTypeData(name="parent_id", display_name="Script ID", read_only=True, show_in_details=False, show_in_list=False), is_valid_uuid, "UUID format is not valid")
    NAME = (DataTypeData(name="name", display_name="Name", read_only=False, show_in_details=True, show_in_list=True), is_valid_string, "String is not valid")
    X = (DataTypeData(name="x", display_name="X Coordinate", read_only=False, show_in_details=True, show_in_list=False), is_valid_number, "Not a valid number")
    Y = (DataTypeData(name="y", display_name="Y Coordinate", read_only=False, show_in_details=True, show_in_list=False), is_valid_number, "Not a valid number")
    ORDER = (DataTypeData(name="order", display_name="Order", read_only=True, show_in_details=True, show_in_list=True), is_valid_number, "Not a valid number")
    DELAY = (DataTypeData(name="delay", display_name="Delay", read_only=False, show_in_details=True, show_in_list=True), is_valid_number, "Not a valid number", delay_render)
    DELAY_TYPE = (DataTypeData(name="delay_type", display_name="Delay type", read_only=False, show_in_details=True, show_in_list=True), is_valid_delay_type, "Delay type is not valid")
    LAST_UPDATE_DATETIME = (DataTypeData(name="last_update_datetime", display_name="Last updated", read_only=True, show_in_details=False, show_in_list=True), is_valid_datetime, "Datetime is not valid", datetime_render)
    LAST_RUN_DATETIME = (DataTypeData(name="last_run_datetime", display_name="Last ran", read_only=True, show_in_details=False, show_in_list=True), is_valid_datetime, "Datetime is not valid", datetime_render)
    CREATED_DATETIME = (DataTypeData(name="created_datetime", display_name="Created", read_only=True, show_in_details=True, show_in_list=False), is_valid_datetime, "Datetime is not valid", datetime_render)

    def __init__(self, data, data_validator, error_message="", render_function=default_render):
        self.data = data
        self.validator = data_validator
        self.validation_error_message = f"{self.data.get_display_name()} is not valid. {error_message}"
        self.render_function = render_function

    def validate(self, a):
        return self.validator(a)

    def get_data(self):
        return self.data

    def render(self, value):
        return self.render_function(value)

    @staticmethod
    def find_by_attribute_name(name):
        for data_type in DataType:
            if data_type.get_data().get_name() == name:
                return data_type
        return None

    @staticmethod
    def find_by_enum(self, enum):
        for data_type in DataType:
            if enum == data_type:
                return data_type
        return None
