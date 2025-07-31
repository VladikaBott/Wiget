from pycodestyle import continued_indentation

number_card = 2222222222222222


def mask_card(number_card: str) -> str:
    clear = number_card.replace(" ", "")
    """Функция которая частично маскирует номер карты"""

    if len(clear) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")
    masked = f"{clear[:4]} {clear[4:6]}** **** {clear[-4:]}"
    return masked


number_card = "2222222222222222"
print(mask_card(number_card))


def mask_account(number: str):
    """Функция которая маскирует счет"""
    clining = number.replace(" ", "")
    if len(clining) < 4:
        raise ValueError("Номер счета должен содержать не меньше 4 символов")
    mask = f"**{clining[-4:]}"
    return mask


number = "30135874305"
print(mask_account(number))


def my_pro(number_int_str: str) -> str:
    """Функция, которая различает счёт и карты и маскирует их номера."""
    parts = number_int_str.lower().split()

    # Если нет номера (только тип "Счет" или "Visa")
    if len(parts) < 2:
        return number_int_str

    # Извлекаем номер (последний элемент)
    number = parts[-1]

    if parts[0] == "счет":
        # Маскируем номер счёта
        if not number.isdigit():
            return number_int_str  # Если номер не цифровой
        masked_number = mask_account(number)  # Маска для счёта: **4305
        return f"Счет {masked_number}"
    else:
        # Маскируем номер карты
        if not number.isdigit() or len(number) < 8:
            return number_int_str  # Если номер некорректный
        masked_number = mask_card(number)
        card_name = " ".join(parts[:-1])  # Сохраняем исходный регистр названия карты
        return f"{card_name} {masked_number}"


print(my_pro("Visa Platinum 1111111111111111"))
print(my_pro("счет 1111111111111111"))
