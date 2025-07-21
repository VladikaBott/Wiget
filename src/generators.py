def filter_by_currency(transactions, currency):
    """Фильтрует транзакции по валюте и возвращает итератор"""
    for transaction in transactions:
        try:
            if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
                yield transaction
        except AttributeError:
            continue


def transaction_descriptions(transactions):
    """Генератор описаний транзакций"""
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start, end):
    """Генератор номеров карт в заданном диапазоне"""
    for number in range(start, end + 1):
        card_str = f"{number:016d}"
        yield f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"
