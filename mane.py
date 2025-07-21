def filter_by_currency(transactions, currency):
    """Фильтрует транзакции по валюте и возвращает итератор."""
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction
