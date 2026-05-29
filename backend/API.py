import httpx
import base64
import json
from pathlib import Path
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from backend.db_handling import load_db, save_db


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

@app.get("/locations/{zip_code}")
async def get_location_on_zip(zip_code: str):
    token = (await get_token())["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.kroger.com/v1/locations?filter.zipCode.near={zip_code}&filter.limit=100", headers=headers)
    response = response.json()
    simplified = []
    for item in response["data"]:
        address = item["address"]["addressLine1"] + " " + item["address"]["city"] + ", " + item["address"]["state"] + " " + item["address"]["zipCode"]
        simplified.append({
            "name": item["name"],
            "locationId": item["locationId"],
            "storeNumber": item["storeNumber"],
            "address": address,
        })
    return simplified

@app.get("/locations/{latitude}/{longitude}")
async def get_location(latitude: str, longitude: str):
    token = (await get_token())["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.kroger.com/v1/locations?filter.latLong.near={latitude},{longitude}", headers=headers)
    response = response.json()
    simplified = []
    if "data" in response:
        for item in response["data"]:
            address = item["address"]["addressLine1"] + " " + item["address"]["city"] + ", " + item["address"][
                "state"] + " " + item["address"]["zipCode"]
            simplified.append({
                "name": item["name"],
                "locationId": item["locationId"],
                "storeNumber": item["storeNumber"],
                "address": address,
            })
    else :
        print(response["errors"]["reason"])
    return simplified

@app.patch("/locations/{location_id}")
async def update_product(location_id: str):
    db = load_db()
    db["location_id"] = location_id
    save_db(db)
    if db["location_id"] != 0:
        print ("location_id now " + str(location_id))

@app.get("/search/{search_term}")
async def search(search_term: str):
    token = (await get_token())["access_token"]
    db = load_db()
    print(db)
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.kroger.com/v1/products?filter.term={search_term}&filter.limit={LIMIT}&filter.locationId={db["location_id"]}", headers=headers
        )
    response = response.json()
    simplified = []
    price = None
    if "data" in response:
        for item in response["data"]:
            if (
                    item.get("items")
                    and len(item["items"]) > 0
                    and item["items"][0].get("price")
            ):
                price = item["items"][0]["price"].get("regular")

            description = (
                item["aisleLocations"][0]["description"]
                if item["aisleLocations"]
                else "Unknown"
            )
            imageURL = None
            for image in item["images"]:
                if image["perspective"] == "front":
                    imageURL = image["sizes"][0]["url"]

            simplified.append({
                "productId": item["productId"],
                "description": item["description"],
                "price": price,
                "aisleLocations": description,
                "manufacturerDeclarations": item.get("manufacturerDeclarations", []),
                "allergensDescription": item.get("allergensDescription", []),
                "imageUrl": imageURL,
                "quantity": 1
            })
    else:
        print("hey you need help")
    return simplified

@app.post("/accounts")
async def create_account(info: dict):

    db = load_db()

    for user in db:

        if user["username"] == info["username"]:

            return {
                "message": "username already exists"
            }

    db.append({
        "username": info["username"],
        "password": info["password"],
        "recentLocations": [],
        "cart": []
    })

    save_db(db)

    return {
        "message": "success"
    }

@app.get("/accounts")
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
    db = load_db()
    for user in db["users"]:
        if user["username"] == username:
            user["cart"] = cart["items"]
    save_db(db)
    return {"message": "success"}

@app.patch("/accounts/{username}/locations")
async def update_locations(username: str, locations: dict):
    db = load_db()
    for user in db["users"]:
        if user["username"] == username:
            if locations["locationID"] not in user["locations"]:
                if len(user["locations"]) < 3:
                    user["locations"].append(locations["locationId"])
                else:
                    user["locations"][0] = [locations["locationId"]]
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
            return user["locations"]
    return {"message": "User not found"}

@app.get("/accounts/{username}/savedCart")
async def get_saved_cart(username: str):
    db = load_db()
    for user in db["users"]:
        if user["username"] == username:
            return user["cart"]
    return {"message": "User not found"}