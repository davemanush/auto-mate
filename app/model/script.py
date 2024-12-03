import uuid
from datetime import datetime
from typing import List

from app.model.entry import Entry
from app.model.step import Step

class Script(Entry):
    def __init__(
            self,
            order: int,
            entry_id: uuid.UUID=None,
            name: str=None,
            steps: List[Step]=None,
            last_run_datetime=None,
            last_update_datetime: datetime | None = None,
            created_datetime: datetime | None = None):
        Entry.__init__(self,
                       entry_id=entry_id,
                       order=order,
                       name=name,
                       created_datetime=created_datetime,
                       last_update_datetime=last_update_datetime
                       )
        self.steps: List[Step] = steps
        self.last_run_datetime: datetime = last_run_datetime
