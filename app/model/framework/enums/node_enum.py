from enum import Enum


class DataUpdateType(Enum):
    DELETE = 1
    ADD = 2
    OVERRIDE = 3