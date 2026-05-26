from pathlib import Path
import json
import os

DB_PATH = Path(__file__).parent / "db.json"

def load_db():
    if not os.path.exists(DB_PATH):
        print("DB not found")
        return {"repos": {}}

    with open(DB_PATH, "r") as file:
        return json.load(file)

def save_db(db):
    with open(DB_PATH, "w") as file:
        json.dump(db, file, indent=4)

def store_repo(repo, repo_name):
    db = load_db()
    if repo_name in db["repos"]:
        delete_repo(repo_name)
    db["repos"][repo_name] = {"files": repo}
    save_db(db)

def delete_repo(repo_name):
    db = load_db()
    db["repos"].pop(repo_name)
    save_db(db)