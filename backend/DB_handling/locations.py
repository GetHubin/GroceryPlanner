from backend.DB_handling.storage import save_db, load_db
from backend.DB_handling.users import get_user


def update_location_history(username, location_id):
    db = load_db()

    for user in db["users"]:
        if user["username"] == username:

            user["curr_location_id"] = location_id

            if location_id in user["recentLocations"]:
                user["recentLocations"].remove(location_id)

            user["recentLocations"].insert(0, location_id)

            user["recentLocations"] = user["recentLocations"][:3]

            save_db(db)

            return True

    return False


def get_recent_locations(username):
    user = get_user(username)

    if user:
        return user["recentLocations"]

    return None



def get_current_location(username):
    user = get_user(username)

    if user:
        return user.get("curr_location_id")

    return None