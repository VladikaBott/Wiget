def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты, оставляя первые 6 и последние 4 цифры."""
    cleaned_number = card_number.replace(" ", "")
    if len(cleaned_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")
    # Форматируем номер карты
    masked = f"{cleaned_number[:4]} {cleaned_number[4:6]}** **** {cleaned_number[-4:]}"
    return masked


print(get_mask_card_number("7000792289606361"))


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счёта, оставляя последние 4 цифры."""
    cleaned_number = account_number.replace(" ", "")
    if len(cleaned_number) < 4:
        raise ValueError("Номер счёта должен содержать как минимум 4 цифры")
    # Форматируем номер счёта
    masked = f"**{cleaned_number[-4:]}"
    return masked


print(get_mask_account("73654108430135874305"))