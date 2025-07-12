from typing import List, Tuple

import pytest

from src.wiget import get_date


@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),  # Стандартный случай
        ("1999-12-31T23:59:59.999999", "31.12.1999"),  # Граничная дата
        ("2000-01-01T00:00:00.000000", "01.01.2000"),  # Начало нового века
        ("2024-02-29T15:30:00.000000", "29.02.2024"),  # Високосный год
    ],
)
def test_get_date_valid(input_date: str, expected: str) -> None:
    """Тестирование корректного преобразования даты."""
    assert get_date(input_date) == expected


@pytest.fixture
def valid_dates() -> List[Tuple[str, str]]:
    """Фикстура возвращает список кортежей с тестовыми датами и ожидаемыми результатами."""
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("1999-12-31T23:59:59.999999", "31.12.1999"),
    ]


def test_get_date_with_fixture(valid_dates: List[Tuple[str, str]]) -> None:
    """Тестирование с использованием фикстуры."""
    for input_date, expected in valid_dates:
        assert get_date(input_date) == expected
