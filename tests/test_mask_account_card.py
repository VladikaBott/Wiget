from typing import List, Tuple

import pytest

from src.wiget import mask_account_card


@pytest.mark.parametrize(
    "input_str, expected",
    [
        # Тесты для счетов
        ("Счет 1234567890123456", "Счет **3456"),
        ("Счет 1234 5678 9012 3456", "Счет **3456"),  # С пробелами
        # Тесты для карт
        ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
        ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
    ],
)
def test_mask_account_card_valid(input_str: str, expected: str) -> None:
    """Тестирование корректного маскирования карт и счетов."""
    assert mask_account_card(input_str) == expected


@pytest.mark.parametrize(
    "invalid_input",
    [
        "Счет 123",  # Слишком короткий номер счета
        "Visa 1234567890",  # Слишком короткий номер карты
        "Счет",  # Нет номера счета
        "Visa Platinum",  # Нет номера карты
        "НеизвестныйТип 123456",  # Неподдерживаемый тип
        "",  # Пустая строка
    ],
)
def test_mask_account_card_invalid(invalid_input: str) -> None:
    """Тестирование обработки некорректных входных данных."""
    assert mask_account_card(invalid_input) == invalid_input


@pytest.fixture
def valid_accounts_cards() -> List[Tuple[str, str]]:
    """Фикстура возвращает список валидных карт/счетов и ожидаемых результатов."""
    return [
        ("Счет 1234567890123456", "Счет **3456"),
        ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
    ]


def test_mask_with_fixture(valid_accounts_cards: List[Tuple[str, str]]) -> None:
    """Тестирование с использованием фикстуры."""
    for input_str, expected in valid_accounts_cards:
        assert mask_account_card(input_str) == expected
