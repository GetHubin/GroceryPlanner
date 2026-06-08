from backend.DB_handling.storage import load_db
from backend.DB_handling.users import get_user


def update_cart(user_id, items):
    db = load_db()
    cur = db.cursor()
    cur.execute("DELETE FROM cart WHERE (user_id = ?)", (user_id,))
    for item in items:
        cur.execute("INSERT INTO cart (user_id, item_id, quantity) VALUES (?, ?, ?)", (user_id, item["itemId"], item["quantity"]))
    db.commit()
    db.close()
    return True


def get_cart(user_id):
    db = load_db()
    cur = db.cursor()
    cur.execute("SELECT item_id, quantity FROM cart WHERE user_id = ?", (user_id,))
    cart = cur.fetchall()
    id_list = []
    for item in cart:
        id_list.append({"item_id": item["item_id"], "quantity": item["quantity"]})
    db.close()
    return id_list
