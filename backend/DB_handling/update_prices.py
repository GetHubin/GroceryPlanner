import asyncio
import sqlite3
import httpx
from backend.APISupport import *
from storage import load_db
async def update_prices():
    db = load_db()
    cur = db.cursor()
    cur.execute("SELECT DISTINCT product_id,location_id FROM price_history ORDER BY product_id")
    products = cur.fetchall()
    final_list = []
    token = (await get_token())["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    for product in products:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.kroger.com/v1/products?filter.productId={product['product_id']}&filter.locationId={product['location_id']}",
                headers=headers
            )
        response = response.json()
        simplified = simplify_product_response(response)
        print(simplified)
        cur.execute("INSERT INTO price_history (product_id, location_id, norm_price, promo_price) VALUES (?, ?, ?, ?)",
                    (simplified["productId"], product["location_id"], simplified["price"], simplified["promoPrice"]))
    db.commit()
    db.close()

if __name__ == "__main__":
    asyncio.run(update_prices())