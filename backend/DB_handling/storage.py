from pathlib import Path
import sqlite3
import json
import os

DB_PATH = "backend/data.db"
REPO_PATH = Path(__file__).resolve().parents[2]
SQL_PATH = REPO_PATH.joinpath(DB_PATH)


def load_db():
    connection = sqlite3.connect(SQL_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def save_db(db):
    db.commit()





def init_db():
    conn = load_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        curr_location_id TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id TEXT,
        quantity INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS location_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        location_id TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cur.execute("""
    DROP TABLE IF EXISTS price_history
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS price_history (
        product_id TEXT PRIMARY KEY,
        store_id TEXT,
        price REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    print(SQL_PATH)
    init_db()


