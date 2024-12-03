import uuid
from datetime import datetime


class Entry:
    def __init__(self, entry_id=uuid.uuid4(), name="", order=0, created_datetime=datetime.now(), last_update_datetime=datetime.now()):
        self.entry_id: uuid.UUID = entry_id
        self.name: str = name
        self.order: int = order
        self.created_datetime: datetime = created_datetime
        self.last_update_datetime: datetime = last_update_datetime