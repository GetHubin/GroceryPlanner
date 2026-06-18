import base64
import httpx
CLIENT_ID = "goceryplanner-bbcfygmt"
CLIENT_SECRET = "eVJd97wJrSNkkABBxrGRKh319eCL-WJBxAwrEew-"


def simplify_location(response):
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
    else:
        print(response["errors"]["reason"])

    return simplified

def simplify_product_response(response):
    simplified = []
    price = None
    promo = None
    if "data" in response:
        for item in response["data"]:
            if (
                    item.get("items")
                    and len(item["items"]) > 0
                    and item["items"][0].get("price")
            ):
                price = item["items"][0]["price"].get("regular")

            if (
                    item.get("items")
                    and len(item["items"]) > 0
                    and item["items"][0].get("price")
            ):
                promo = item["items"][0]["price"].get("promo")

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
                "promoPrice": promo,
                "aisleLocations": description,
                "manufacturerDeclarations": item.get("manufacturerDeclarations", []),
                "allergensDescription": item.get("allergensDescription", []),
                "imageUrl": imageURL,
                "quantity": 1
            })
    else:
        print("hey you need help")
    print (len(simplified))
    if len(simplified) == 1:
        return simplified[0]
    return simplified

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