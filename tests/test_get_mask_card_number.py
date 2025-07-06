from typing import List, Tuple

import pytest

from src.masks import get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567890123456", "1234 56** **** 3456"),  # Без пробелов
        ("1234 5678 9012 3456", "1234 56** **** 3456"),  # С пробелами
        ("123456******3456", "1234 56** **** 3456"),  # Символы вместо цифр
    ],
)
def test_mask_card_number_valid(card_number: str, expected: str) -> None:
    """Тестирование корректного маскирования номера карты."""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "invalid_card_number",
    [
        "1234567890",  # Слишком короткий
        "12345678901234567890",  # Слишком длинный
        "",  # Пустая строка
        "1234 5678 9012",  # Неполный номер
    ],
)
def test_mask_card_number_invalid_length(invalid_card_number: str) -> None:
    """Тестирование обработки некорректной длины номера карты."""
    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
        get_mask_card_number(invalid_card_number)


@pytest.fixture
def valid_card_numbers() -> List[Tuple[str, str]]:
    """Фикстура возвращает список валидных номеров карт и ожидаемых результатов."""
    return [
        ("1234567890123456", "1234 56** **** 3456"),
        ("1111222233334444", "1111 22** **** 4444"),
    ]


def test_mask_with_fixture(valid_card_numbers: List[Tuple[str, str]]) -> None:
    """Тестирование с использованием фикстуры."""
    for card_number, expected in valid_card_numbers:
        assert get_mask_card_number(card_number) == expected
