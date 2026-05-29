def simplifyLocation(response):
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
    if len(simplified) == 1:
        return simplified[0]
    return simplified