from backend.DB_handling.storage import load_db
import sqlite3

def get_user(user_id):
    db = load_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cur.fetchone()
    db.close()
    if user is None:
        return None
    return dict(user)

def get_user_id(username):
    db = load_db()
    cur = db.cursor()
    cur.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user_id = cur.fetchone()
    db.close()
    if user_id is None:
        return None
    return dict(user_id)

def create_user(username, password):
    db = load_db()
    cur = db.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    db.commit()
    db.close()
    return True


def login_user(username, password):
    user_id = get_user_id(username)["user_id"]
    user = get_user(user_id)
    if user is None:
        return False
    elif user["password"] == password:
        return user_id
    return None


def delete_user(user_id):
    db = load_db()
    cur = db.cursor()
    cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    db.commit()
    deleted = cur.rowcount
    db.close()
    if deleted != 0:
        return True
    else:
        return False



def change_user_password(user_id, old_password, new_password):
    db = load_db()
    cur = db.cursor()

    cur.execute(
        "SELECT password FROM users WHERE user_id = ?",
        (user_id,)
    )
    row = cur.fetchone()

    if row is None:
        db.close()
        return False

    if row["password"] != old_password:
        db.close()
        return False

    cur.execute(
        "UPDATE users SET password = ? WHERE user_id = ?",
        (new_password, user_id)
    )

    db.commit()
    db.close()
    return True
