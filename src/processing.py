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


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Сортирует список словарей по ключу 'date'"""
    return sorted(transactions, key=lambda x: x["date"], reverse=reverse)
