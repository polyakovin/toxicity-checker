def format_result(ingredients: list[str], matches: list[dict]) -> str:
    total = len(ingredients)
    found = len(matches)
    safe_count = total - found

    danger_counts = {"high": 0, "medium": 0, "low": 0}
    for m in matches:
        danger_counts[m["danger_level"]] += 1

    lines = []

    emoji_line_parts = []
    if danger_counts["high"] > 0:
        emoji_line_parts.append(f"\u2622 {danger_counts['high']} опасных")
    if danger_counts["medium"] > 0:
        emoji_line_parts.append(f"\u26a0 {danger_counts['medium']} средних")
    if danger_counts["low"] > 0:
        emoji_line_parts.append(f"\u2139 {danger_counts['low']} низких")
    emoji_line = " | ".join(emoji_line_parts) if emoji_line_parts else "\u2705 Безопасно"

    if danger_counts["high"] > 0:
        overall = "\u2622\ufe0f ВЫСОКИЙ уровень токсичности"
    elif danger_counts["medium"] > 0:
        overall = "\u26a0\ufe0f СРЕДНИЙ уровень токсичности"
    elif danger_counts["low"] > 0:
        overall = "\u2139\ufe0f Низкий уровень токсичности"
    else:
        overall = "\u2705 Опасные компоненты не найдены"

    lines.append(f"<b>Анализ состава</b>\n")
    lines.append(f"{overall}\n")
    lines.append(f"Проверено компонентов: {total}")
    lines.append(f"Найдено совпадений: {found}")
    lines.append(f"Безопасных: {safe_count}\n")
    lines.append(f"{emoji_line}\n")

    if matches:
        lines.append("<b>\U0001f9ea Найденные токсичные компоненты:</b>\n")
        for i, m in enumerate(matches, 1):
            lines.append(
                f"{i}. {m['danger_emoji']} <b>{m['name_ru']}</b> "
                f"(<i>{m['name_en']}</i>) — {m['category_label']}"
            )
            lines.append(f"   \U0001f4dd {m['description']}")
            lines.append(f"   \U0001f4dc Регулирование: {m['regulation']}")
            lines.append("")

    if len("\n".join(lines)) > 3900:
        lines_truncated = []
        lines_truncated.append(f"<b>Анализ состава</b>\n{overall}\n")
        lines_truncated.append(f"Проверено: {total} | Опасных: {found} | Безопасных: {safe_count}\n")
        lines_truncated.append("<b>Найденные компоненты:</b>\n")
        for m in matches:
            lines_truncated.append(
                f"{m['danger_emoji']} <b>{m['name_ru']}</b> — {m['category_label']}"
            )
        return "\n".join(lines_truncated)

    return "\n".join(lines)
