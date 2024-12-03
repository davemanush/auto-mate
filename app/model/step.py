import uuid
from datetime import datetime

from app.model.entry import Entry
from app.model.enums import DelayType

class Step(Entry):
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
        Entry.__init__(self,
                       entry_id=entry_id,
                       order=order,
                       name=name,
                       created_datetime=created_datetime,
                       last_update_datetime=last_update_datetime
        )
        self.parent_id = parent_id
        self.x: int = x if x is not None else 0
        self.y: int = y if y is not None else 0
        self.delay: int = delay if delay is not None else 0
        self.delay_type: DelayType = delay_type if delay_type is not None else DelayType.BEFORE

