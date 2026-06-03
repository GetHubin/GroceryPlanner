from backend.DB_handling.storage import load_db
import sqlite3

def get_user(username):
    db = load_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
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
    user = get_user(username)
    if user is None:
        return False
    elif user["password"] == password:
        return True
    return False


def delete_user(username):
    db = load_db()
    cur = db.cursor()
    cur.execute("DELETE FROM users WHERE username = ?", (username,))
    db.commit()
    deleted = cur.rowcount
    db.close()
    if deleted != 0:
        return True
    else:
        return False



def change_user_password(username, old_password, new_password):
    db = load_db()
    cur = db.cursor()

    cur.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )
    row = cur.fetchone()

    if row is None:
        db.close()
        return False

    if row[0] != old_password:
        db.close()
        return False

    cur.execute(
        "UPDATE users SET password = ? WHERE username = ?",
        (new_password, username)
    )

    db.commit()
    db.close()
    return True
