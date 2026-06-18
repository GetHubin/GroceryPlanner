from PIL.ImageFont import truetype

from backend.DB_handling.storage import  load_db
from backend.DB_handling.users import get_user
import sqlite3


def add_product_to_history(info):
    db = load_db()
    cur = db.cursor()
    user = get_user(info["user_id"])
    location_id = user["current_location_id"]
    cur.execute("INSERT INTO price_history (product_id, location_id, norm_price, promo_price) VALUES (?, ?, ?, ?)",
                (info["product_id"], location_id, info["regular_price"], info["promo_price"]))
    db.commit()
    db.close()
    return True

def delete_product_from_history(product_id):
    db = load_db()
    cur = db.cursor()
    cur.execute("DELETE FROM price_history WHERE product_id = ?", (product_id,))
    db.commit()
    db.close()
    return True

def find_product_history(product_id):
    db = load_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM price_history WHERE product_id = ?", (product_id,))
    history = cur.fetchall()
    db.close()
    print( product_id)
    return [dict(row) for row in history]

def is_product_tracking(product_id):
    db = load_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM price_history WHERE product_id = ?", (product_id,))
    if cur.rowcount == 0:
        return False
    db.close()
    return True

def get_list_of_products_history():
    db = load_db()
    cur = db.cursor()
    cur.execute("SELECT DISTINCT product_id FROM price_history ORDER BY product_id")
    products = cur.fetchall()
    product_list = []
    for product in products:
        product_list.append(product["product_id"])
    db.close()
    return product_list
