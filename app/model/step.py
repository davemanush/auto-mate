import uuid
from datetime import datetime

from app.model.enums import DelayType

class Step:
    def __init__(
            self,
            parent_id,
            order: int,
            entry_id: uuid.UUID=None,
            name: str=None,
            x: int=None,
            y: int=None,
            delay: int=None,
            delay_type: DelayType=None,
            created_datetime: datetime=None,
            last_update_datetime: datetime=None):
        self.entry_id: uuid = entry_id if entry_id is not None else uuid.uuid4()
        self.parent_id = parent_id
        self.name: str = name if name is not None else ""
        self.x: int = x if x is not None else 0
        self.y: int = y if y is not None else 0
        self.order: int = order
        self.delay: int = delay if delay is not None else 0
        self.delay_type: DelayType = delay_type if delay_type is not None else DelayType.BEFORE
        self.created_datetime: datetime = created_datetime if entry_id is not None else datetime.now()
        self.last_update_datetime: last_update_datetime = last_update_datetime
