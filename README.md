# grocery_agent

A smart grocery planning workflow: tell it what you want to cook, pick a recipe, and it finds the cheapest matching products at a nearby Kroger store.

> **Status:** early learning project, version 1. The app searches products and prices but does not add items to a cart yet.

## How it works

```text
You type a dish ("chicken soup")
   → Gemini suggests 2 recipes with structured ingredient lists
   → You choose one
   → Kroger API: find the nearest store, search each ingredient
   → Gemini filters out wrong matches (e.g. "olive oil" ≠ "sherry vinegar")
   → Pick the cheapest matching product per ingredient
   → Print a shopping list with an estimated total
```

The AI only *chooses* between real products returned by Kroger. Product names, prices and UPCs always come from Kroger's data, never from the model.

## Example output

```text
Enter the type of dish you want recipes for: chicken soup

Option 2: Hearty Chicken and Rice Soup (Prep time: 40 minutes)
...
The cheapest product for chicken thighs is: Heritage Farm Boneless Skinless Fresh Chicken Thighs at $3.49
The cheapest product for chicken broth is: Kroger® Less Sodium Fat Free Chicken Broth at $1.59
The cheapest product for white rice is: Riceland Extra Long Grain White Rice at $2.19
...
```

## Requirements

- Python 3.13+
- A free **Gemini API key**, from [Google AI Studio](https://aistudio.google.com)
- A **Kroger developer app** (client ID and secret), from [developer.kroger.com](https://developer.kroger.com)

## Setup

```bash
git clone https://github.com/heatherlien81/grocery_agent.git
cd grocery_agent

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root. It is listed in `.gitignore`, so it is never committed.

```text
GEMINI_API_KEY=your-gemini-key
KROGER_CLIENT_ID=your-kroger-client-id
KROGER_CLIENT_SECRET=your-kroger-client-secret
KROGER_ENV=certification
ZIP_CODE=45202
```

| Variable | Meaning |
| --- | --- |
| `KROGER_ENV` | `certification` (Kroger's test environment) or `production`. It must match the environment your Kroger app is registered for. |
| `ZIP_CODE` | Where to look for a store. The certification environment only has some stores, so a Cincinnati ZIP (45202) is a reliable test value. |

## Run

```bash
python main.py
```

## Project structure

| File | Purpose |
| --- | --- |
| `main.py` | Runs the full flow |
| `recipes.py` | Gemini: generate recipes; show them and let the user pick one |
| `LLM.py` | Gemini: filter Kroger search results to real matches |
| `kroger.py` | Kroger API: access token, store lookup, product search, cheapest pick |
| `helper.py` | Converts Kroger's raw product data into `Product` objects |
| `model.py` | Pydantic data models (`Ingredient`, `Recipe`, `Product`, ...) |

## Known limitations

- Picks the cheapest product by **total price**, not price per ounce or pound.
- Recipe wording doesn't always match store products (e.g. "garlic cloves" finds nothing; "garlic" would).
- Calls Gemini once per ingredient, so it's slower and uses more of the free-tier quota than necessary.
- Gemini's free tier sometimes returns `503` (high demand). Wait a moment and run again.

## Roadmap

- [ ] Separate shopping search terms from recipe wording
- [ ] Let the user remove pantry items they already have
- [ ] Compare price per unit
- [ ] Confirm the list, then add items to a real Kroger cart (production app + OAuth sign-in)
- [ ] Freshness reminders for perishable items
- [ ] Compare prices across stores (Instacart, Weee!)
