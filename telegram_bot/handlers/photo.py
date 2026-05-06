from aiogram import Router, F
from aiogram.types import Message
from loguru import logger

from services.ocr import extract_text_from_image
from services.parser import parse_ingredients
from services.matcher import match_ingredients
from templates.result import format_result

router = Router()


@router.message(F.photo)
async def handle_photo(message: Message):
    await message.answer("\U0001f4f8 Распознаю текст с фотографии...")

    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    image_bytes = await message.bot.download_file(file.file_path)
    image_bytes = image_bytes.read()

    try:
        raw_text = extract_text_from_image(image_bytes)
    except Exception as e:
        logger.error(f"OCR failed: {e}")
        await message.answer(
            "\u274c Не удалось распознать текст. Убедитесь, что фото чёткое, "
            "текст горизонтальный и хорошо освещён."
        )
        return

    if not raw_text or len(raw_text) < 10:
        await message.answer(
            "\u274c Текст на фото не найден. Попробуйте сфотографировать состав "
            "крупнее и без бликов."
        )
        return

    ingredients = parse_ingredients(raw_text)

    if not ingredients:
        await message.answer(
            "\u274c Не удалось выделить ингредиенты из текста. "
            "Попробуйте отправить состав текстом."
        )
        return

    matches = match_ingredients(ingredients)

    result = format_result(ingredients, matches)
    result = f"<i>Распознанный текст:</i>\n{raw_text[:200]}...\n\n{result}"
    await message.answer(result, parse_mode="HTML")
