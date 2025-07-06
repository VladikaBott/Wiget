from typing import Any, Dict, List

import pytest

from src.processing import sort_by_date

# Тестовые данные
test_data: List[Dict[str, Any]] = [
    {"date": "2023-08-01T12:00:00", "id": 1},
    {"date": "2023-08-15T09:30:00", "id": 2},
    {"date": "2023-07-20T14:15:00", "id": 3},
]


# Проверяю пустой список
def test_empty_list() -> None:
    result: List[Dict[str, Any]] = sort_by_date([])
    assert result == []


# Проверяю список с одной операцией
def test_single_item() -> None:
    data: List[Dict[str, Any]] = [{"date": "2023-01-01T00:00:00", "id": 1}]
    result: List[Dict[str, Any]] = sort_by_date(data)
    assert result[0]["id"] == 1
