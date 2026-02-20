import json
from typing import List
from . import schemas
import os

DB_FILE = "agent_db.json"

def save_db(db: List[schemas.Agent]):
    """Saves the agent database to a JSON file."""
    with open(DB_FILE, "w") as f:
        json.dump([agent.dict() for agent in db], f, indent=4, default=str)

def load_db() -> List[schemas.Agent]:
    """Loads the agent database from a JSON file."""
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        data = json.load(f)
        return [schemas.Agent(**item) for item in data]
