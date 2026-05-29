from pathlib import Path
import json
import os

DB_PATH = Path(__file__).parent / "Users.json"

def load_db():
    if not os.path.exists(DB_PATH):
        print("DB not found")
        return {"repos": {}}

    with open(DB_PATH, "r") as file:
        return json.load(file)

def save_db(db):
    with open(DB_PATH, "w") as file:
        json.dump(db, file, indent=4)

def new_user():
    pass

def update_user():
    pass

def delete_user():
    pass
