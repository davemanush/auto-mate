import uuid
from datetime import datetime
from typing import List

from app.model.step import Step

class Script:
    def __init__(
            self,
            order: int,
            entry_id: uuid.UUID=None,
            name: str=None,
            steps: List[Step]=None,
            last_run_datetime: datetime | None = None,
            last_update_datetime: datetime | None = None,
            created_datetime: datetime | None = None):
        self.entry_id: uuid.UUID = entry_id if entry_id is not None else uuid.uuid4()
        self.name: str = name if name is not None else ""
        self.order = order
        self.steps: List[Step] = steps if steps is not None else []
        self.last_run_datetime: datetime | None = None
        self.last_update_datetime: datetime | None = None
        self.created_datetime = created_datetime if created_datetime is not None else datetime.now()
        self.last_run_datetime: datetime = last_run_datetime
        self.last_update_datetime: datetime = last_update_datetime
