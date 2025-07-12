from typing import List, Tuple

import pytest

from src.masks import get_mask_account


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("1234567890", "**7890"),  # 10 цифр без пробелов
        ("1234 5678 9012 3456", "**3456"),  # С пробелами
        ("00001234", "**1234"),  # Крайний случай: ровно 4 цифры
        ("12 34 56 78", "**5678"),  # Нестандартное форматирование
    ],
)
def test_mask_account_valid(account_number: str, expected: str) -> None:
    """Тестирование корректного маскирования номера счета."""
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize(
    "invalid_account_number",
    [
        "123",  # 3 цифры
        "",  # Пустая строка
    ],
)
def test_mask_account_invalid_length(invalid_account_number: str) -> None:
    """Тестирование обработки некорректной длины номера счета."""
    with pytest.raises(ValueError, match="Номер счёта должен содержать как минимум 4 цифры"):
        get_mask_account(invalid_account_number)


@pytest.fixture
def valid_account_numbers() -> List[Tuple[str, str]]:
    """Фикстура возвращает список кортежей с тестовыми номерами счетов и ожидаемыми результатами."""
    return [
        ("12345678", "**5678"),
        ("111122223333", "**3333"),
    ]


def test_mask_account_with_fixture(valid_account_numbers: List[Tuple[str, str]]) -> None:
    """Тестирование с использованием фикстуры."""
    for account_number, expected in valid_account_numbers:
        assert get_mask_account(account_number) == expected
