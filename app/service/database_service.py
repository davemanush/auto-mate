from pathlib import Path

from tinydb import TinyDB, Query
from tinydb.table import Table
from datetime import datetime
from typing import List, Optional
from enum import Enum

# Assuming DelayType, Script, and Step are defined in your imports
from app.model.enums import DelayType
from app.model.script import Script, Step
import os

class DatabaseService:
    from app.model.script import Script, Step

    def __init__(self):
        DB_NAME = "/auto-mate.json"
        DB_PATH = ""
        if os.name == 'nt':
            print("Running on Windows")
            DB_FOLDER = "/auto-mate"
            DB_PATH = os.getenv("APPDATA") + DB_FOLDER
            os.makedirs(DB_PATH, exist_ok=True)
            DB_PATH += DB_NAME
        elif os.name == 'posix':
            DB_FOLDER = "/.auto-mate"
            DB_PATH = Path.home().as_posix() + DB_FOLDER
            os.makedirs(DB_PATH, exist_ok=True)
            DB_PATH += DB_NAME
        else:
            print("Unknown operating system")
            exit(1)
        self.db_path = DB_PATH
        #self.db_path = "/home/rogame-manush/Documents/GitHub/Davemanush/ffautoclicker/model/data_tdb.json"
        self.db = TinyDB(self.db_path)
        self.scripts_table: Table = self.db.table("scripts")
        self.steps_table: Table = self.db.table("steps")

    # --- Helper Functions ---
    def parse_date_or_none(self, data, field_name):
        value = data.get(field_name)
        return datetime.fromisoformat(value) if value else None

    def find_delay_type(self, value):
        if value == DelayType.BEFORE.name:
            return DelayType.BEFORE
        if value == DelayType.AFTER.name:
            return DelayType.AFTER
        raise ValueError(f"Unknown DelayType: {value}")

    # --- Script Management ---
    def save_script(self, script: Script):
        self.scripts_table.upsert({
            "script_id": script.entry_id,
            "name": script.name,
            "order": script.order,
            "created_datetime": script.created_datetime.isoformat() if script.created_datetime else None,
            "last_run_datetime": script.last_run_datetime.isoformat() if script.last_run_datetime else None,
            "last_update_datetime": script.last_update_datetime.isoformat() if script.last_update_datetime else None,
        }, Query().script_id == script.entry_id)
        for step in script.steps:
            self.save_step(str(script.entry_id), step)

    def get_script(self, script_id: str) -> Optional[Script]:
        result = self.scripts_table.get(Query().script_id == script_id)
        if not result:
            return None
        return Script(
            entry_id=result["script_id"],
            name=result["name"],
            order=result["order"],
            created_datetime=self.parse_date_or_none(result, "created_datetime"),
            last_run_datetime=self.parse_date_or_none(result, "last_run_datetime"),
            last_update_datetime=self.parse_date_or_none(result, "last_update_datetime"),
            steps=self.get_steps_by_script(script_id)  # Steps will be loaded separately
        )

    def get_all_scripts(self) -> List[Script]:
        scripts = []
        for result in self.scripts_table.all():
            scripts.append(Script(
                entry_id=result["script_id"],
                name=result["name"],
                order=result["order"],
                created_datetime=self.parse_date_or_none(result, "created_datetime"),
                last_run_datetime=self.parse_date_or_none(result, "last_run_datetime"),
                last_update_datetime=self.parse_date_or_none(result, "last_update_datetime"),
                steps=self.get_steps_by_script(result["script_id"]) # Steps will be loaded separately
            ))
        return scripts

    # --- Step Management ---
    def save_step(self, script_id: str, step: Step):
        self.steps_table.upsert({
            "step_id": step.entry_id,
            "script_id": script_id,
            "name": step.name,
            "x_coordinate": step.x,
            "y_coordinate": step.y,
            "step_order": step.order,
            "delay": step.delay,
            "delay_type": step.delay_type.name,
            "created_datetime": step.created_datetime.isoformat() if step.created_datetime else None,
            "last_update_datetime": step.last_update_datetime.isoformat() if step.last_update_datetime else None,
        }, Query().step_id == step.entry_id)

    def get_steps_by_script(self, script_id: str) -> List[Step]:
        steps = []
        for result in self.steps_table.search(Query().script_id == script_id):
            steps.append(Step(
                entry_id=result["step_id"],
                parent_id=result["script_id"],
                name=result["name"],
                x=result["x_coordinate"],
                y=result["y_coordinate"],
                order=result["step_order"],
                delay=result["delay"],
                delay_type=self.find_delay_type(result["delay_type"]),
                created_datetime=self.parse_date_or_none(result, "created_datetime"),
                last_update_datetime=self.parse_date_or_none(result, "last_update_datetime"),
            ))
        return steps

    # --- Utility Methods ---
    def load_full_script(self, script_id: str) -> Optional[Script]:
        script = self.get_script(script_id)
        if script:
            script.steps = self.get_steps_by_script(script_id)
        return script

    def close(self):
        """Close the database (optional for TinyDB)."""
        self.db.close()