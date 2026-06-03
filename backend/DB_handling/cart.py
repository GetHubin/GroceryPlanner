from backend.DB_handling.storage import load_db
from backend.DB_handling.users import get_user


def update_cart(user_id, items):
    db = load_db()
    cur = db.cursor()
    cur.execute("DELETE FROM cart WHERE (user_id = ?)", (user_id,))
    for item in items:
        cur.execute("INSERT INTO cart (user_id, item) VALUES (?, ?)", (user_id, item))
    db.commit()
    db.close()
    return True


def get_cart(user_id):
    db = load_db()
    cur = db.cursor()
    cur.execute("SELECT item_id FROM cart WHERE user_id = ?", (user_id,))
    cart = cur.fetchall()
    id_list = []
    for item in cart:
        id_list.append(item["item_id"])
    return id_list
