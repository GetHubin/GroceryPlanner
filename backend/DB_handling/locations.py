from operator import truediv

from backend.DB_handling.storage import  load_db
from backend.DB_handling.users import get_user
import sqlite3

def update_location_history(user_id, location_id):
    db = load_db()
    cur = db.cursor()

    # 1. update current location
    cur.execute(
        "UPDATE users SET current_location_id = ? WHERE user_id = ?",
        (location_id, user_id)
    )

    # 2. insert into history (no duplicate check needed if we don't care)
    cur.execute(
        "INSERT INTO location_history (user_id, location_id) VALUES (?, ?)",
        (user_id, location_id)
    )

    # 3. keep only last 3 entries (by rowid)
    cur.execute("""
            DELETE FROM location_history
            WHERE rowid NOT IN (
                SELECT rowid FROM location_history
                WHERE user_id = ?
                ORDER BY rowid DESC
                LIMIT 3
            )
            AND user_id = ?
        """, (user_id, user_id))

    db.commit()
    db.close()
    return True

def get_recent_locations(user_id):
    db = load_db()
    cur = db.cursor()
    cur.execute("SELECT location_id FROM location_history WHERE user_id = ?", (user_id,))
    locations = cur.fetchall()
    loc_list = []
    for location in locations:
        loc_list.append(location["location_id"])
    db.close()
    return loc_list



def get_current_location(user_id):
    db = load_db()
    cur = db.cursor()
    cur.execute("SELECT current_location_id FROM users WHERE user_id = ?", (user_id,))
    user = cur.fetchone()
    if user:
        return user["current_location_id"]
    return None