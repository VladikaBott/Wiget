import os

import requests
from dotenv import load_dotenv

load_dotenv()


def get_amount_in_rub(transaction):
    """
    Конвертирует сумму транзакции в рубли

    """
    if not transaction or "operationAmount" not in transaction:
        return 0.0

    amount = float(transaction["operationAmount"]["amount"])
    currency = transaction["operationAmount"]["currency"]["code"]

    if currency == "RUB":
        return amount

    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        return 0.0

    try:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
        response = requests.get(url, headers={"apikey": api_key}, timeout=5)
        response.raise_for_status()
        return float(response.json()["result"])

    except (requests.RequestException, KeyError, ValueError):
        return 0.0
