import aiohttp
from loguru import logger

OPENFOODFACTS_BASE = "https://world.openfoodfacts.org/api/v2"


async def lookup_barcode(barcode: str) -> dict | None:
    url = f"{OPENFOODFACTS_BASE}/product/{barcode}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
    except Exception as e:
        logger.warning(f"OpenFoodFacts lookup failed for '{barcode}': {e}")
        return None

    product = data.get("product", {})
    if not product:
        return None

    return {
        "name": product.get("product_name", ""),
        "brand": product.get("brands", ""),
        "ingredients_text": product.get("ingredients_text", ""),
        "categories": product.get("categories", ""),
        "image_url": product.get("image_url", ""),
    }
