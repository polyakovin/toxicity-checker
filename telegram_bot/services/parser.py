import re

INGREDIENT_SEPARATORS = re.compile(r"[,;]|\n|\.\s*(?=[A-ZА-Я])")
PERCENTAGE_RE = re.compile(r"\d+[\.,]?\d*\s*%")
PARENTHESIS_RE = re.compile(r"\([^)]*\)")
COLORANT_RE = re.compile(r"CI\s*\d+", re.IGNORECASE)

def parse_ingredients(text: str) -> list[str]:
    text = text.strip()
    text = PARENTHESIS_RE.sub(" ", text)
    text = PERCENTAGE_RE.sub(" ", text)

    parts = INGREDIENT_SEPARATORS.split(text)
    ingredients = []

    for part in parts:
        ingredient = part.strip().strip(".*-–— ")
        if not ingredient:
            continue
        if len(ingredient) < 2:
            continue
        if COLORANT_RE.fullmatch(ingredient):
            continue
        ingredients.append(ingredient)

    return ingredients
