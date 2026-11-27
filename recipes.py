"""
# call LLM to generate recipes and ingredients in a structured format
"""
from dotenv import load_dotenv
from model import Ingredient, Recipe, RecipeChoices
from google import genai
from google.genai import types


def get_recipes(dish: str) -> RecipeChoices:
    """
    Calls the LLM to generate recipes and ingredients in a structured format.

    Args:
        dish (str): The type of dish to generate recipes for.
    """
    load_dotenv()  # Load environment variables from .env file
    client = genai.Client()

    prompt = f"Give me 2 recipes for {dish} with their ingredients and preparation time in minutes."

    response = client.models.generate_content(
        model = "gemini-3.5-flash-lite",
        contents = prompt,
        config = types.GenerateContentConfig(
            response_mime_type = "application/json",
            response_schema = RecipeChoices,
            system_instruction = "You are a meal-planning assistant. Output clean, searchable grocery terms suitable for an automated ordering API"
        )
    )

    parsed_data = response.parsed
    return parsed_data

def show_choices(recipe_choices: RecipeChoices):
    """
    Displays the recipe choices to the user.

    Args:
        recipe_choices (RecipeChoices): The recipe choices to display.
    """
    for i, recipe in enumerate(recipe_choices.recipes, 1):
        print(f"\nOption {i}: {recipe.name} (Prep time: {recipe.prep_time_minutes} minutes)")
        for item in recipe.ingredients:
            print(f"- {item.quantity} {item.unit} of {item.name}")

def pick_recipe(recipe_choices: RecipeChoices) -> Recipe:
    """
    Allows the user to pick a recipe from the available choices.

    Args:
        recipe_choices (RecipeChoices): The recipe choices to pick from.

    Returns:
        Recipe: The selected recipe.
    """
    while True:
        try:
            choice = int(input(f"\nEnter the option number of the recipe you want to choose (1-{len(recipe_choices.recipes)}): "))
            if 1 <= choice <= len(recipe_choices.recipes):
                return recipe_choices.recipes[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(recipe_choices.recipes)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
