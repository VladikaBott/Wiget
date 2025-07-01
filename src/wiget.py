from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """Функция маскирует номер карты или счета в переданной строке."""
    parts = info.split()

    if not parts:
        return info  # Если строка пустая, возвращаем как есть

    if parts[0] == "Счет":
        # Маскируем номер счета
        if len(parts) < 2:
            return info  # Если нет номера счета, возвращаем как есть
        account_number = parts[-1]
        try:
            masked_number = get_mask_account(account_number)
            return f"Счет {masked_number}"
        except ValueError:
            return info  # Если номер счета некорректен, возвращаем исходную строку
    else:
        # Маскируем номер карты
        if len(parts) < 2:
            return info  # Если нет номера карты, возвращаем как есть
        card_name = " ".join(parts[:-1])
        card_number = parts[-1]
        try:
            masked_number = get_mask_card_number(card_number)
            return f"{card_name} {masked_number}"
        except ValueError:
            return info  # Если номер карты некорректен, возвращаем исходную строку


def get_date(date_str: str) -> str:
    """Преобразует дату из формата '2024-03-11T02:26:18.671407' в '11.03.2024'"""
    # Беру только часть до буквы T (это будет дата)
    date_part = date_str.split("T")[0]

    # Разбиваем дату на части через дефис
    year, month, day = date_part.split("-")

    # Собираем в новом формате
    return f"{day}.{month}.{year}"
