from pathlib import Path
import sqlite3

DB_PATH = "backend/data.db"
REPO_PATH = Path(__file__).resolve().parents[2]
SQL_PATH = REPO_PATH.joinpath(DB_PATH)


def load_db():
    connection = sqlite3.connect(SQL_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    conn = load_db()
    cur = conn.cursor()

    # cur.execute("""
    # CREATE TABLE location_history (
    # user_id INTEGER NOT NULL,
    # location_id INTEGER NOT NULL,
    #
    # PRIMARY KEY (user_id, location_id),
    #
    # FOREIGN KEY (user_id) REFERENCES users(user_id)
    # )
    # """)
    #
    # cur.execute("""
    # CREATE TABLE cart (
    # user_id INTEGER NOT NULL,
    # item_id INTEGER NOT NULL,
    #
    # PRIMARY KEY (user_id, item_id),
    #
    # FOREIGN KEY (user_id) REFERENCES users(user_id)
    # )
    # """)
    #
    # cur.execute("""
    # CREATE TABLE users (
    # user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    # username TEXT NOT NULL UNIQUE,
    # password TEXT NOT NULL,
    # current_location_id INTEGER
    # )
    # """)
    # cur.execute("""
    # CREATE TABLE price_history (
    # item_id INTEGER NOT NULL,
    # week_date DATE NOT NULL,
    # price REAL NOT NULL,
    #
    # PRIMARY KEY (item_id, week_date)
    # )
    # """)
    #
    # conn.commit()
    # conn.close()

if __name__ == "__main__":
    print(SQL_PATH)
    init_db()


