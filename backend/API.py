import httpx
import base64
import json
from pathlib import Path
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.APISupport import simplify_location, simplify_product_response
from backend.DB_handling.cart import update_cart, get_cart
from backend.DB_handling.locations import update_location_history, get_recent_locations
from backend.DB_handling.users import get_user, create_user, login_user, delete_user, change_user_password

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LIMIT = 50
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

@app.get("/locations/{zip_code}/zip")
async def get_location_on_zip(zip_code: str):
    token = (await get_token())["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.kroger.com/v1/locations?filter.zipCode.near={zip_code}&filter.limit=100", headers=headers)
    response = response.json()
    return simplify_location(response)

@app.get("/locations/{location_id}/id")
async def get_location_on_location_id(location_id: str):
    token = (await get_token())["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.kroger.com/v1/locations?filter.locationId={location_id}", headers=headers)
    response = response.json()
    return simplify_location(response)

@app.get("/locations/{latitude}/{longitude}")
async def get_location(latitude: str, longitude: str):
    token = (await get_token())["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.kroger.com/v1/locations?filter.latLong.near={latitude},{longitude}", headers=headers)
    response = response.json()
    return simplify_location(response)

@app.get("/products/{product_id}/{user_id}")
async def search_product(product_id: str, user_id: int):
    token = (await get_token())["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    user = get_user(user_id)
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.kroger.com/v1/products?filter.productId={product_id}&filter.limit={LIMIT}&filter.locationId={user['current_location_id']}",
            headers=headers
        )
    response = response.json()
    return simplify_product_response(response)

@app.get("/search/{search_term}/{user_id}")
async def search(search_term: str, user_id: int):
    token = (await get_token())["access_token"]
    user = get_user(user_id)
    print(user["current_location_id"])
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.kroger.com/v1/products?filter.term={search_term}&filter.limit={LIMIT}&filter.locationId={user['current_location_id']}", headers=headers
        )
    response = response.json()
    print(response)
    return simplify_product_response(response)

@app.post("/accounts/signup")
async def create_account(info: dict):

    user_id = create_user(
        info["username"],
        info["password"]
    )

    if user_id:
        return {"message": "success", "userId": user_id}

    return {"message": "username already exists"}

@app.post("/accounts/login")
async def login(info: dict):

    user_id = login_user(
        info["username"],
        info["password"]
    )
    if user_id:
        return {"message": "success", "userId": user_id}

    return {"message": "User not found"}

@app.delete("/accounts/{user_id}")
async def delete_account(user_id: int):

    delete_user(user_id)

    return {"message": "success"}

@app.get("/accounts/{user_id}")
async def get_account(user_id: int):

    user = get_user(user_id)

    if user:
        return user

    return {"message": "User not found"}

@app.patch("/accounts/{user_id}/cart")
async def update_cart_route(user_id: int, cart: dict):

    if update_cart(
        user_id,
        cart.get("items", [])
    ):
        return {"message": "success"}

    return {"message": "user not found"}

@app.patch("/accounts/{user_id}/locations")
async def update_location(user_id: int, locations: dict):

    success = update_location_history(
        user_id,
        locations["locationId"]
    )

    if success:
        return {"message": "success"}

    return {"message": "User not found"}

@app.patch("/accounts/{user_id}/change_password")
async def change_password(user_id: int, passwords: dict):

    result = change_user_password(
        user_id,
        passwords["oldPassword"],
        passwords["newPassword"]
    )

    return {"message": result}

@app.get("/accounts/{user_id}/prevLocations")
async def get_prev_locations(user_id: int):

    locations = get_recent_locations(user_id)

    if locations is not None:
        return locations

    return {"message": "User not found"}

@app.get("/accounts/{user_id}/savedCart")
async def get_saved_cart(user_id: int):

    cart = get_cart(user_id)

    if cart is not None:
        return cart

    return {"message": "User not found"}

