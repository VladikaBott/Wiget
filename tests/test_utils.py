import json
import re
from unittest.mock import patch

import pytest

from src.utils import (
    count_operations_by_category,
    filter_operations_by_description,
    load_transactions,
    process_bank_operations,
)


@pytest.fixture
def mock_logger():
    with patch("src.utils.logger") as mock:
        yield mock


@pytest.fixture
def sample_operations():
    return [
        {"id": 1, "description": "Перевод организации", "amount": 100, "currency": "RUB"},
        {"id": 2, "description": "Оплата услуг связи", "amount": 50, "currency": "RUB"},
        {"id": 3, "description": "Доставка еды Pizza", "amount": 75, "currency": "USD"},
        {"id": 4, "description": "Перевод со счета на счет", "amount": 200, "currency": "EUR"},
        {"id": 5, "description": "Оплата налогов (Налог.)", "amount": 150, "currency": "RUB"},
        {"id": 6, "description": None, "amount": 10, "currency": "RUB"},
        {"id": 7, "description": "Доставка еды Sushi", "amount": 90, "currency": "RUB"},
        {"id": 8, "description": "Перевод организации", "amount": 300, "currency": "RUB"},
    ]


# Тесты для load_transactions
def test_load_valid_json_file(mock_logger, tmp_path):
    test_data = [{"id": 1}, {"id": 2}]
    file_path = tmp_path / "test.json"
    file_path.write_text(json.dumps(test_data))

    result = load_transactions(str(file_path))
    assert result == test_data
    mock_logger.info.assert_called_once()


def test_load_empty_file(mock_logger, tmp_path):
    file_path = tmp_path / "empty.json"
    file_path.write_text("")

    result = load_transactions(str(file_path))
    assert result == []
    mock_logger.warning.assert_called_once()


def test_file_not_found(mock_logger):
    result = load_transactions("nonexistent.json")
    assert result == []
    mock_logger.warning.assert_called_once()


def test_invalid_json(mock_logger, tmp_path):
    file_path = tmp_path / "bad.json"
    file_path.write_text("{invalid}")

    result = load_transactions(str(file_path))
    assert result == []
    mock_logger.error.assert_called_once()


def test_permission_error(mock_logger):
    with (
        patch("os.path.exists", return_value=True),
        patch("os.path.getsize", return_value=100),
        patch("builtins.open", side_effect=PermissionError("Access denied")),
    ):
        result = load_transactions("restricted.json")
        assert result == []
        mock_logger.error.assert_called_once_with("Нет доступа к файлу: Access denied")


def test_non_list_json(mock_logger, tmp_path):
    test_data = {"id": 1}
    file_path = tmp_path / "not_list.json"
    file_path.write_text(json.dumps(test_data))

    result = load_transactions(str(file_path))
    assert result == []
    mock_logger.info.assert_called_once()


# Тесты для filter_operations_by_description
def test_filter_operations_by_description_found(sample_operations, mock_logger):
    result = filter_operations_by_description(sample_operations, "Pizza")
    assert len(result) == 1
    assert result[0]["id"] == 3
    mock_logger.info.assert_called_with("Поиск по строке 'Pizza': найдено 1 операций")


def test_filter_operations_by_description_multiple_results(sample_operations, mock_logger):
    result = filter_operations_by_description(sample_operations, "Доставка еды")
    assert len(result) == 2
    assert result[0]["id"] == 3
    assert result[1]["id"] == 7


def test_filter_operations_by_description_not_found(sample_operations, mock_logger):
    result = filter_operations_by_description(sample_operations, "Кинотеатр")
    assert len(result) == 0
    mock_logger.info.assert_called_with("Поиск по строке 'Кинотеатр': найдено 0 операций")


def test_filter_operations_by_description_special_chars(sample_operations, mock_logger):
    result = filter_operations_by_description(sample_operations, "Налог.")
    assert len(result) == 1
    assert result[0]["id"] == 5


def test_filter_operations_by_description_empty_search(sample_operations, mock_logger):
    result = filter_operations_by_description(sample_operations, "")
    assert len(result) == 0
    mock_logger.debug.assert_called_with("Получена пустая строка для поиска, возвращаем пустой список")


def test_filter_operations_by_description_case_sensitive(sample_operations, mock_logger):
    result = filter_operations_by_description(sample_operations, "pizza")
    assert len(result) == 0


def test_filter_operations_by_description_no_description_field(sample_operations, mock_logger):
    result = filter_operations_by_description(sample_operations, "Перевод")
    assert len(result) == 3
    assert all(op["id"] in [1, 4, 8] for op in result)


def test_filter_operations_by_description_regex_error(mock_logger):
    with patch("re.compile", side_effect=re.error("Invalid regex")):
        result = filter_operations_by_description([{"description": "test"}], "test")
        assert result == []
        mock_logger.error.assert_called_with("Ошибка в регулярном выражении: Invalid regex")


# Тесты для process_bank_operations
def test_process_bank_operations_exists(sample_operations, mock_logger):
    categories = ["Перевод организации", "Оплата услуг связи", "Доставка еды Pizza"]
    result = process_bank_operations(sample_operations, categories)

    assert result["Перевод организации"] == 2
    assert result["Оплата услуг связи"] == 1
    assert result["Доставка еды Pizza"] == 1
    mock_logger.info.assert_called_with(
        "Подсчет операций по категориям: {'Перевод организации': 2, 'Оплата услуг связи': 1, 'Доставка еды Pizza': 1}"
    )


def test_process_bank_operations_non_existent(sample_operations, mock_logger):
    categories = ["Несуществующая категория", "Другая категория"]
    result = process_bank_operations(sample_operations, categories)

    assert result["Несуществующая категория"] == 0
    assert result["Другая категория"] == 0


def test_process_bank_operations_empty_categories(sample_operations, mock_logger):
    result = process_bank_operations(sample_operations, [])
    assert result == {}
    mock_logger.info.assert_called_with("Получен пустой список категорий, возвращаем пустой словарь")


def test_process_bank_operations_error_handling(mock_logger):
    with patch("collections.Counter", side_effect=Exception("Test error")):
        categories = ["Категория 1", "Категория 2"]
        result = process_bank_operations([{"description": "test"}], categories)

        assert result == {"Категория 1": 0, "Категория 2": 0}
        mock_logger.exception.assert_called_with("Ошибка при подсчете операций по категориям: Test error")


# Тесты для count_operations_by_category
def test_count_operations_by_category_exists(sample_operations, mock_logger):
    categories = ["Перевод организации", "Оплата услуг связи", "Доставка еды Pizza"]
    result = count_operations_by_category(sample_operations, categories)

    assert result["Перевод организации"] == 2
    assert result["Оплата услуг связи"] == 1
    assert result["Доставка еды Pizza"] == 1
    mock_logger.info.assert_called_with(
        "Подсчет операций по категориям: {'Перевод организации': 2, 'Оплата услуг связи': 1, 'Доставка еды Pizza': 1}"
    )


def test_count_operations_by_category_non_existent(sample_operations, mock_logger):
    categories = ["Несуществующая категория", "Другая категория"]
    result = count_operations_by_category(sample_operations, categories)

    assert result["Несуществующая категория"] == 0
    assert result["Другая категория"] == 0


def test_count_operations_by_category_empty_categories(sample_operations, mock_logger):
    result = count_operations_by_category(sample_operations, [])
    assert result == {}
    mock_logger.info.assert_called_with("Подсчет операций по категориям: {}")


def test_count_operations_by_category_error_handling(mock_logger):
    with patch("collections.Counter", side_effect=Exception("Test error")):
        categories = ["Категория 1", "Категория 2"]
        result = count_operations_by_category([{"description": "test"}], categories)

        assert result == {"Категория 1": 0, "Категория 2": 0}
        mock_logger.exception.assert_called_with("Ошибка при подсчете операций по категориям: Test error")


# Сравниваем, что обе функции дают одинаковый результат
def test_functions_equivalence(sample_operations, mock_logger):
    categories = ["Перевод организации", "Оплата услуг связи"]

    result1 = process_bank_operations(sample_operations, categories)
    result2 = count_operations_by_category(sample_operations, categories)

    assert result1 == result2
    assert result1["Перевод организации"] == 2
    assert result1["Оплата услуг связи"] == 1
