"""
# call LLM to generate recipes and ingredients in a structured format
"""
from dotenv import load_dotenv
from model import Ingredient, Recipe, RecipeChoices
from google import genai
from google.genai import types

load_dotenv()  # Load environment variables from .env file
client = genai.Client()

prompt = "Give me 2 recipes for chocolate chip cookies with their ingredients and preparation time in minutes."

response = client.models.generate_content(
    model = "gemini-3.8-flash",
    contents = prompt,
    config = types.GenerateContentConfig(
        response_mime_type = "application/json",
        response_schema = RecipeChoices,
        system_instruction = "You are a meal-planning assistant. Output clean, searchable grocery terms suitable for an automated ordering API"
    )
)

parsed_data = response.parsed
print(response.text)

for i, recipe in enumerate(parsed_data.recipes,1):
    print(f"\nOption {i}: {recipe.name} (Prep time: {recipe.prep_time_minutes} minutes)")
    for item in recipe.ingredients:
        print(f"- {item.quantity} {item.unit} of {item.name}")
