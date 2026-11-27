from model import Product

def to_product(raw: dict) -> Product:
    return Product(
        name=raw.get("description"),
        brand=raw.get("brand"),
        size=raw.get("items", [{}])[0].get("size"),
        price=raw.get("items", [{}])[0].get("price", {}).get("regular"),
        upc=raw.get("upc")
    )