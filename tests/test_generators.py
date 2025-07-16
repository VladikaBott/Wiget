import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

@pytest.fixture
def sample_transactions():
    return [
        {
            "operationAmount": {
                "currency": {"code": "USD"}
            },
            "description": "Payment 1"
        },
        {
            "operationAmount": {
                "currency": {"code": "EUR"}
            },
            "description": "Payment 2"
        }
    ]

def test_filter_by_currency(sample_transactions):
    usd = list(filter_by_currency(sample_transactions, "USD"))
    assert len(usd) == 1
    assert usd[0]['description'] == "Payment 1"

def test_transaction_descriptions(sample_transactions):
    desc = list(transaction_descriptions(sample_transactions))
    assert desc == ["Payment 1", "Payment 2"]

def test_card_number_generator():
    cards = list(card_number_generator(1, 3))
    assert cards == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003"
    ]