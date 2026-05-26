import httpx
import base64
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LIMIT = 50
LOCATION_ID = "01400376"
CLIENT_ID = "goceryplanner-bbcfygmt"
CLIENT_SECRET = "eVJd97wJrSNkkABBxrGRKh319eCL-WJBxAwrEew-"


async def get_token():

    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {auth_base64}"
    }

    data = {
        "grant_type": "client_credentials",
        "scope": "product.compact"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.kroger.com/v1/connect/oauth2/token",
            headers=headers,
            data=data
        )

    return response.json()



@app.get("/search/{search_term}")
async def search(search_term: str):
    token = (await get_token())["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.kroger.com/v1/products?filter.term={search_term}&filter.limit={LIMIT}&filter.locationId={LOCATION_ID}", headers=headers
        )
    response = response.json()
    simplified = []
    price = None
    for item in response["data"]:
        if (
                item.get("items")
                and len(item["items"]) > 0
                and item["items"][0].get("price")
        ):
            price = item["items"][0]["price"].get("regular")

        simplified.append({
            "productId": item["productId"],
            "description": item["description"],
            "price": price,
            "quantity": 1
        })
    return simplified