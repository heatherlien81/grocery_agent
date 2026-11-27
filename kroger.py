import os
import base64
import requests
from dotenv import load_dotenv
from helper import to_product
from model import Product

def get_base_url() -> str:
    """
    Returns the base URL for the Kroger API based on the environment variable KROGER_ENV.
    """
    load_dotenv()
    KROGER_ENV = os.getenv("KROGER_ENV", "certification")
    
 
    if KROGER_ENV == "production":
        return "https://api.kroger.com/v1"
    else:
        return "https://api-ce.kroger.com/v1"

def get_access_token():
    load_dotenv()
    CLIENT_ID = os.getenv("KROGER_CLIENT_ID")
    CLIENT_SECRET = os.getenv("KROGER_CLIENT_SECRET")
    BASE_URL = get_base_url()

    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    response = requests.post(
        f"{BASE_URL}/connect/oauth2/token",
        headers={
            "Authorization": f"Basic {b64_auth_str}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "client_credentials",
            "scope": "product.compact",
        },
    )
    response.raise_for_status()
    return response.json()["access_token"]

def find_store(token: str, zip_code: str) -> str:
    BASE_URL = get_base_url()
    response = requests.get(
        f"{BASE_URL}/locations",
        headers={"Authorization": f"Bearer {token}"},
        params={
            "filter.zipCode.near": zip_code, 
            },
    )
    response.raise_for_status()
    return response.json()["data"][0]["locationId"]  # Return the first store's locationId

def search_products(token: str, term: str, location_id: str):
    BASE_URL = get_base_url()
    response = requests.get(
        f"{BASE_URL}/products",
        headers={"Authorization": f"Bearer {token}"},
        params={
            "filter.term": term, 
            "filter.locationId": location_id,
            "filter.limit": 5,
            },
    )
    response.raise_for_status()

    raw_products = response.json().get("data", [])
    product_list = [to_product(raw) for raw in raw_products]
    return product_list

def find_cheapest(products: list[Product]) -> Product | None:
    """
    Finds the cheapest product.

    Args:
        products (list[Product]): The list of products to evaluate.
    Returns:
        Product | None: The cheapest product, or None if the list is empty.
    """

    if not products:
        return None

    priced = [p for p in products if p.price is not None] 
    if priced:
        cheapest_products = min(priced, key=lambda x: x.price)
    else:
        cheapest_products = None

    return cheapest_products


