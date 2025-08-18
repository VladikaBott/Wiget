from unittest.mock import MagicMock, patch

from src.external_api import get_amount_in_rub


@patch.dict("os.environ", {"EXCHANGE_RATE_API_KEY": "test_key"})
@patch("requests.get")
def test_usd_conversion(mock_get):
    """Тест конвертации USD в RUB."""
    # Подготовка тестовых данных
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 7500.0}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"}
        }
    }

    # Проверка
    assert get_amount_in_rub(transaction) == 7500.0
    mock_get.assert_called_once()


def test_rub_transaction_no_conversion():
    """Тест транзакции в RUB (без конвертации)."""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "RUB"}
        }
    }
    assert get_amount_in_rub(transaction) == 100.0


@patch.dict("os.environ", {"EXCHANGE_RATE_API_KEY": "test_key"})
@patch("requests.get")
def test_api_error_handling(mock_get):
    """Тест обработки ошибки API."""
    mock_get.side_effect = Exception("API error")

    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "EUR"}
        }
    }

    assert get_amount_in_rub(transaction) == 0.0


def test_invalid_transaction_data():
    """Тест обработки невалидных данных транзакции."""
    assert get_amount_in_rub(None) == 0.0
    assert get_amount_in_rub({}) == 0.0
    assert get_amount_in_rub({"operationAmount": {}}) == 0.0


@patch.dict("os.environ", {}, clear=True)
def test_missing_api_key():
    """Тест отсутствия API-ключа."""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"}
        }
    }
    assert get_amount_in_rub(transaction) == 0.0
