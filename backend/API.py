import httpx
import base64
import json
from pathlib import Path
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from backend.db_handling import load_db, save_db
from backend.APISupport import simplifyLocation, simplify_product_response

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
    return simplifyLocation(response)

@app.get("/locations/{location_id}/id")
async def get_location_on_location_id(location_id: str):
    token = (await get_token())["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.kroger.com/v1/locations?filter.locationId={location_id}", headers=headers)
    response = response.json()
    return simplifyLocation(response)

@app.get("/locations/{latitude}/{longitude}")
async def get_location(latitude: str, longitude: str):
    token = (await get_token())["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.kroger.com/v1/locations?filter.latLong.near={latitude},{longitude}", headers=headers)
    response = response.json()
    return simplifyLocation(response)



@app.patch("/locations/{location_id}")
async def update_product(location_id: str):
    db = load_db()
    db["location_id"] = location_id
    save_db(db)
    if db["location_id"] != 0:
        print ("location_id now " + str(location_id))

@app.get("/products/{product_id}")
async def search_product(product_id: str):
    token = (await get_token())["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    db = load_db()
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.kroger.com/v1/products?filter.productId={product_id}&filter.limit={LIMIT}&filter.locationId={db['location_id']}",
            headers=headers
        )
    response = response.json()
    return simplify_product_response(response)

@app.get("/search/{search_term}")
async def search(search_term: str):
    token = (await get_token())["access_token"]
    db = load_db()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.kroger.com/v1/products?filter.term={search_term}&filter.limit={LIMIT}&filter.locationId={db["location_id"]}", headers=headers
        )
    response = response.json()
    return simplify_product_response(response)

@app.post("/accounts/signup")
async def create_account(info: dict):

    db = load_db()

    for user in db["users"]:

        if user["username"] == info["username"]:

            return {
                "message": "username already exists"
            }

    db["users"].append({
        "username": info["username"],
        "password": info["password"],
        "recentLocations": [],
        "cart": []
    })

    save_db(db)

    return {
        "message": "success"
    }

@app.post("/accounts/login")
async def login(info: dict):
    db = load_db()
    for user in db["users"]:
        if user["username"] == info["username"] and user["password"] == info["password"]:
            return {"message": "success"}
    return {"message": "User not found"}

@app.delete("/accounts/{username}")
async def delete_account(username: str):
    db = load_db()
    db.remove({"username": username})
    save_db(db)
    return {"message": "success"}

@app.get("/accounts/{username}")
async def get_account(username: str):
    db = load_db()
    for user in db["users"]:
        if user["username"] == username:
            return user
    return {"message": "User not found"}

@app.patch("/accounts/{username}/cart")
async def update_cart(username: str, cart: dict):
    print(cart)
    db = load_db()
    for user in db["users"]:

        if user["username"] == username:

            items = cart.get("items", [])

            user["cart"] = items

            save_db(db)

            return {"message": "success"}

    return {"message": "user not found"}

@app.patch("/accounts/{username}/locations")
async def update_locations(username: str, locations: dict):

    db = load_db()

    for user in db["users"]:

        if user["username"] == username:

            if "recentLocations" not in user:
                user["recentLocations"] = []

            loc_id = locations["locationId"]

            # remove if already exists (avoid duplicates)
            if loc_id in user["recentLocations"]:
                user["recentLocations"].remove(loc_id)

            # add newest to front
            user["recentLocations"].insert(0, loc_id)

            # keep only last 3
            user["recentLocations"] = user["recentLocations"][:3]

            save_db(db)

            return {"message": "success"}

    return {"message": "User not found"}

@app.patch("/accounts/{username}/change_password")
async def change_password(username: str, passwords: dict):
    db = load_db()
    for user in db["users"]:
        if user["username"] == username:
            if user["password"] == passwords["oldPassword"]:
                user["password"] = passwords["newPassword"]
                return {"message": "success"}
            else:
                return {"message": "incorrect old password"}

@app.get("/accounts/{username}/prevLocations")
async def get_prev_locations(username: str):
    db = load_db()
    for user in db["users"]:
        if user["username"] == username:
            return user["recentLocations"]
    return {"message": "User not found"}

@app.get("/accounts/{username}/savedCart")
async def get_saved_cart(username: str):
    db = load_db()
    for user in db["users"]:
        if user["username"] == username:
            return user["cart"]
    return {"message": "User not found"}

