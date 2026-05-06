from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from services.parser import parse_ingredients
from services.matcher import match_ingredients
from templates.result import format_result

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "<b>CheckToxicity Bot</b> \U0001f9ea\n\n"
        "Я проверяю состав косметики и бытовой химии на токсичные компоненты.\n\n"
        "<b>Как пользоваться:</b>\n"
        "\U0001f4dd <b>Текст</b> — пришлите список ингредиентов\n"
        "\U0001f4f8 <b>Фото</b> — пришлите фотографию состава\n"
        "\U0001f4e6 <b>Штрихкод</b> — пришлите число штрихкода\n\n"
        "Команды:\n"
        "  /start — это сообщение\n"
        "  /help — справка\n"
        "  /categories — категории токсичности\n"
    )
    await message.answer(text, parse_mode="HTML")


@router.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "<b>Справка</b>\n\n"
        "<b>Текстовый ввод:</b>\n"
        "Отправьте список ингредиентов через запятую, точку с запятой или с новой строки.\n"
        "Пример: Aqua, Sodium Lauryl Sulfate, Glycerin, Parfum\n\n"
        "<b>Фото:</b>\n"
        "Сфотографируйте состав на упаковке так, чтобы текст был чётким и горизонтальным.\n\n"
        "<b>Штрихкод:</b>\n"
        "Отправьте число штрихкода (8, 12, 13 цифр). Бот найдёт продукт в базе OpenFoodFacts.\n\n"
        "<b>Уровни опасности:</b>\n"
        "\u2622 — высокий (канцерогены, эндокринные разрушители, запрещённые)\n"
        "\u26a0 — средний (аллергены, раздражители)\n"
        "\u2139 — низкий (потенциально небезопасные)"
    )
    await message.answer(text, parse_mode="HTML")


@router.message(Command("categories"))
async def cmd_categories(message: Message):
    text = (
        "<b>Категории токсичных веществ</b>\n\n"
        "\U0001f480 <b>Канцерогены</b> — вещества, вызывающие рак\n"
        "<i>Формальдегид, BHA, гидрохинон, бензол, свинец, ртуть</i>\n\n"
        "\U0001f9ec <b>Эндокринные разрушители</b> — нарушают гормональный баланс\n"
        "<i>Парабены, фталаты, триклозан, оксибензон, BHT</i>\n\n"
        "\U0001f98f <b>Аллергены</b> — вызывают аллергические реакции\n"
        "<i>Метилизотиазолинон, DMDM Гидантоин, парафенилендиамин</i>\n\n"
        "\U0001f915 <b>Раздражители</b> — раздражают кожу и слизистые\n"
        "<i>SLS, SLES, минеральное масло, ПЭГ, силиконы</i>"
    )
    await message.answer(text, parse_mode="HTML")


@router.message(F.text & ~F.text.startswith("/"))
async def handle_text(message: Message):
    text = message.text.strip()

    if len(text) < 20:
        await message.answer(
            "Слишком короткий текст. Пришлите полный список ингредиентов состава."
        )
        return

    if len(text) > 5000:
        await message.answer(
            "Слишком длинный текст. Пожалуйста, сократите до списка ингредиентов "
            "(обычно состав умещается в 5000 символов)."
        )
        return

    ingredients = parse_ingredients(text)

    if not ingredients:
        await message.answer(
            "Не удалось распознать ингредиенты. Попробуйте разделить их запятыми "
            "или точкой с запятой."
        )
        return

    matches = match_ingredients(ingredients)

    result = format_result(ingredients, matches)
    await message.answer(result, parse_mode="HTML")
