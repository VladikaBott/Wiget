import pytest
from unittest.mock import patch, MagicMock
from src.external_api import get_amount_in_rub
import os


@patch.dict('os.environ', {'EXCHANGE_RATE_API_KEY': 'test_key'})
@patch('requests.get')
def test_usd_conversion(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {'result': 7500.0}
    mock_get.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"}
        }
    }

    assert get_amount_in_rub(transaction) == 7500.0


def test_rub_transaction():
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "RUB"}
        }
    }
    assert get_amount_in_rub(transaction) == 100.0


