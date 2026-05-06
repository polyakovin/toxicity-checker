import re
from aiogram import Router, F
from aiogram.types import Message
from loguru import logger

from services.barcode import lookup_barcode
from services.parser import parse_ingredients
from services.matcher import match_ingredients
from templates.result import format_result

router = Router()

BARCODE_RE = re.compile(r"^\d{8,14}$")


@router.message(F.text & ~F.text.startswith("/"))
async def handle_barcode(message: Message):
    text = message.text.strip()
    if not BARCODE_RE.match(text):
        return

    await message.answer("\U0001f50d Ищу продукт по штрихкоду...")

    try:
        product = await lookup_barcode(text)
    except Exception as e:
        logger.error(f"Barcode lookup failed: {e}")
        await message.answer("\u274c Ошибка при поиске продукта. Попробуйте позже.")
        return

    if not product or not product.get("ingredients_text"):
        await message.answer(
            "\u274c Продукт с таким штрихкодом не найден в базе или у него нет состава.\n"
            "Попробуйте отправить состав текстом вручную."
        )
        return

    lines = []
    if product.get("name"):
        lines.append(f"<b>{product['name']}</b>")
    if product.get("brand"):
        lines.append(f"Бренд: {product['brand']}")

    ingredients = parse_ingredients(product["ingredients_text"])

    if not ingredients:
        await message.answer(
            "\u274c Не удалось разобрать состав продукта из базы.\n"
            "Отправьте состав текстом вручную."
        )
        return

    matches = match_ingredients(ingredients)

    result = format_result(ingredients, matches)
    header = "\n".join(lines) if lines else ""
    result = f"{header}\n\n{result}" if header else result

    await message.answer(result, parse_mode="HTML")
