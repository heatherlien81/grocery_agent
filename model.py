"""
This module defines the data models for the recipe and ingredient information used in the application.
"""

from pydantic import BaseModel, Field

class Ingredient(BaseModel):
    name: str = Field(..., description="The name of the ingredient")
    quantity: float = Field(..., description="The quantity of the ingredient")
    unit: str = Field(..., description="The unit of measurement for the ingredient")

class Recipe(BaseModel):
    name: str = Field(..., description="The name of the recipe")
    prep_time_minutes: int = Field(..., description="Preparation time in minutes")
    ingredients: list[Ingredient] = Field(..., description="List of ingredients required for the recipe")

class RecipeChoices(BaseModel):
    recipes: list[Recipe] = Field(..., description="List of recipe choices")

class Product(BaseModel):
    name: str = Field(..., description="The name of the product")
    brand: str | None = Field(None, description="The brand of the product")
    size: str = Field(..., description="The size of the product")
    price: float | None = Field(None, description="The price of the product")
    upc: str = Field(..., description="The UPC code of the product")
