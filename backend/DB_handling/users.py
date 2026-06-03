from backend.DB_handling.storage import load_db, save_db


def get_user(username):
    db = load_db()

    for user in db["users"]:
        if user["username"] == username:
            return user

    return None


def create_user(username, password):
    db = load_db()

    for user in db["users"]:
        if user["username"] == username:
            return False

    db["users"].append({
        "username": username,
        "password": password,
        "recentLocations": [],
        "cart": [],
        "curr_location_id": None
    })

    save_db(db)
    return True


def login_user(username, password):
    user = get_user(username)

    if user is None:
        return False

    return user["password"] == password


def delete_user(username):
    db = load_db()

    db["users"] = [
        user
        for user in db["users"]
        if user["username"] != username
    ]

    save_db(db)



def change_user_password(username, old_password, new_password):
    db = load_db()

    for user in db["users"]:
        if user["username"] == username:

            if user["password"] != old_password:
                return False

            user["password"] = new_password

            save_db(db)

            return True

    return None