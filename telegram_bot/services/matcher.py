import json
from pathlib import Path
from rapidfuzz import fuzz, process

DB_PATH = Path(__file__).parent.parent / "db" / "substances.json"

DANGER_EMOJI = {
    "low": "\u26a0\ufe0f",
    "medium": "\u26a0\ufe0f",
    "high": "\u2622\ufe0f",
}

CATEGORY_LABELS = {
    "carcinogen": "Канцероген",
    "allergen": "Аллерген",
    "endocrine_disruptor": "Эндокринный разрушитель",
    "irritant": "Раздражитель",
}

MATCH_THRESHOLD = 85


def _load_db() -> list[dict]:
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _build_index(substances: list[dict]) -> dict[str, dict]:
    index = {}
    for sub in substances:
        for name in (sub["name_ru"], sub["name_en"], *sub["synonyms"]):
            index[name.lower()] = sub
    return index


def _length_ratio_ok(query: str, target: str) -> bool:
    ratio = len(query) / len(target)
    return 0.25 <= ratio <= 4.0


def match_ingredients(ingredients: list[str]) -> list[dict]:
    substances = _load_db()
    index = _build_index(substances)
    names = list(index.keys())

    results = []
    seen_ids = set()

    for ingredient in ingredients:
        ingredient_lower = ingredient.lower().strip()
        best_name = None
        best_score = 0

        for name in names:
            if not _length_ratio_ok(ingredient_lower, name):
                continue

            score = fuzz.WRatio(ingredient_lower, name)
            if score > best_score:
                best_score = score
                best_name = name

        if best_name is None or best_score < MATCH_THRESHOLD:
            continue

        substance = index[best_name]
        sub_id = substance["name_en"]

        if sub_id in seen_ids:
            continue

        seen_ids.add(sub_id)
        results.append({
            "ingredient": ingredient,
            "matched_as": best_name,
            "score": best_score,
            "name_ru": substance["name_ru"],
            "name_en": substance["name_en"],
            "category": substance["category"],
            "danger_level": substance["danger_level"],
            "description": substance["description"],
            "source": substance["source"],
            "regulation": substance["regulation"],
            "danger_emoji": DANGER_EMOJI.get(substance["danger_level"], ""),
            "category_label": CATEGORY_LABELS.get(substance["category"], substance["category"]),
        })

    results.sort(key=lambda r: {"high": 0, "medium": 1, "low": 2}[r["danger_level"]])
    return results
