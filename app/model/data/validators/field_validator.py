import uuid
from datetime import datetime

from app.model.enums import DelayType

def is_valid_string(string):
    return True

def is_valid_uuid(uuid_string):
    try:
        val = uuid.UUID(uuid_string, version=4)
    except ValueError:
        return False
    return str(val) == uuid_string

def is_valid_number(number_string):
    return number_string.isdigit() and len(number_string) < 6

def is_valid_datetime(datetime_string, date_format="%Y-%m-%d %H:%M:%S.%f"):
    try:
        datetime.strptime(datetime_string, date_format)
        return True
    except ValueError:
        return False

def is_valid_delay_type(delay_type):
    return True if DelayType.find_by_name(delay_type) is not None else False