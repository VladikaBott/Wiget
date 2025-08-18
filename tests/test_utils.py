import json
from unittest.mock import patch

import pytest

from src.utils import load_transactions


@pytest.fixture
def mock_logger():
    with patch('src.utils.logger') as mock:
        yield mock


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
    with patch("os.path.exists", return_value=True), \
            patch("os.path.getsize", return_value=100), \
            patch("builtins.open", side_effect=PermissionError("Access denied")):
        result = load_transactions("restricted.json")
        assert result == []
        mock_logger.error.assert_called_once_with(
            "Нет доступа к файлу: Access denied"
        )


def test_non_list_json(mock_logger, tmp_path):
    test_data = {"id": 1}
    file_path = tmp_path / "not_list.json"
    file_path.write_text(json.dumps(test_data))

    result = load_transactions(str(file_path))
    assert result == []
    mock_logger.info.assert_called_once()
