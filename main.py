from dotenv import load_dotenv
from kroger import get_access_token, find_store, search_products, find_cheapest
from recipes import get_recipes, show_choices, pick_recipe
import os

def main():
    """
    Main function to run the grocery agent application.
    """
    load_dotenv()  # Load environment variables from .env file
    
    # 1. Get Dishes and Ingredients from LLM
    dish = input("Enter the type of dish you want recipes for: ")
    recipe_choices = get_recipes(dish)
    show_choices(recipe_choices)
    recipe = pick_recipe(recipe_choices)

    # 2. Find a nearby Kroger store
    zip_code = os.getenv("ZIP_CODE", "45202")
    token = get_access_token()
    store_id = find_store(token, zip_code)

    for ingredient in recipe.ingredients:
        # 3. Search for products at the Kroger store
        products = search_products(token, ingredient.name, store_id)
        cheapest_product = find_cheapest(products)
        if cheapest_product:
            print(f"\nThe cheapest product for {ingredient.name} is: {cheapest_product.name} at ${cheapest_product.price}")
        else:
            print(f"\nNo product found for {ingredient.name}")


if __name__ == "__main__":
    main()
    