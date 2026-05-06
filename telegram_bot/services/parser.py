import re

INGREDIENT_SEPARATORS = re.compile(r"[,;]|\n|\.\s*(?=[A-ZА-Я])")
PERCENTAGE_RE = re.compile(r"\d+[\.,]?\d*\s*%")
PARENTHESIS_RE = re.compile(r"\([^)]*\)")
COLORANT_RE = re.compile(r"CI\s*\d+", re.IGNORECASE)

SAFE_STOP_WORDS = frozenset({
    "aqua", "water", "вода", "glycerin", "глицерин",
    "tocopherol", "токоферол", "vitamin e", "витамин e",
})


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
        if ingredient.lower() in SAFE_STOP_WORDS:
            continue
        ingredients.append(ingredient)

    return ingredients
