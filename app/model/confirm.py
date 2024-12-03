from typing import List

from app.model.enums import ConfirmOption
class Confirm:
    def __init__(self):
        self.options: List[ConfirmOption] = [ConfirmOption.YES, ConfirmOption.NO]

