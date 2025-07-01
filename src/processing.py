from typing import Any, Dict, List


def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Фильтрует список банковских операций по их статусу."""
    result = []  # Создал пустой список для результата
    # Перебираю все операции по одной
    for operation in operations:
        # Проверяю, что статус операции совпадает с нужным
        if operation["state"] == state:
            # Если совпадает - добавляю операцию в результат
            result.append(operation)
    return result


operations = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

print(filter_by_state(operations))  # Вызов с параметром по умолчанию (EXECUTED)
print(filter_by_state(operations, state="CANCELED"))  # Вызов с указанием статуса CANCELED


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Сортирует список словарей по ключу 'date'"""
    return sorted(transactions, key=lambda x: x["date"], reverse=reverse)


transactions: List[Dict[str, Any]] = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
]

sorted_transactions: List[Dict[str, Any]] = sort_by_date(transactions)
print(sorted_transactions)
