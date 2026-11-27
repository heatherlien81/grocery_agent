from dotenv import load_dotenv
from kroger import get_access_token, find_store, search_products
from recipes import get_recipes, show_choices, pick_recipe

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
    # zip_code = input("Enter your zip code: ")
    # token = get_access_token()
    # location_id = find_store(token, zip_code)

if __name__ == "__main__":
    main()
    