from backend.DB_handling.storage import load_db, save_db
from backend.DB_handling.users import get_user


def update_cart(username, items):
    db = load_db()

    for user in db["users"]:
        if user["username"] == username:
            user["cart"] = items
            save_db(db)
            return True

    return False


def get_cart(username):
    user = get_user(username)

    if user:
        return user["cart"]

    return None
