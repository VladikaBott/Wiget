# 🏦 Banking Widget

Профессиональный инструмент для обработки банковских операций с поддержкой JSON, CSV и Excel форматов.

## 📦 Основные модули

### 🔒 masks.py
```python
def get_mask_card_number(card_number: str) -> str:
    """1234567890123456 → 1234 56** **** 3456"""
def get_mask_account(account_number: str) -> str:
    """12345678901234567890 → **7890"""
```
### 📦 utils.py (Базовые утилиты)
```python
def load_transactions(file_path: str) -> list[dict]:
    """
    Универсальный загрузчик транзакций
    Поддерживает:
    - JSON (оригинальный формат)
    - CSV (через pandas)
    - Excel (через pandas)
    """
```
### 🎛 widget.py
```python
def mask_account_card(info: str) -> str:
    """Visa 1234567890123456 → Visa 1234 56** **** 3456"""
def get_date(date_str: str) -> str:
    """2023-05-20T12:30:00 → 20.05.2023"""
```

### 🔄 processing.py
```python
def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Фильтрация по статусу (EXECUTED/CANCELED)"""
def sort_by_date(transactions: list[dict], reverse: bool = True) -> list[dict]:
    """Сортировка по дате (по умолчанию - новые сначала)"""
```
### 📝 logger.py
```python
def setup_logger(name: str, log_file: str) -> logging.Logger:
    """Настройка системы логирования"""
```
### 🌐 external_api.py
```python
def get_amount_in_rub(transaction: dict) -> float:
    """Конвертация суммы в рубли через API"""
```
### 📁 file_processor.py
```python
def load_csv_transactions(file_path: str) -> list[dict]:
    """Загрузка данных из CSV"""
def load_excel_transactions(file_path: str) -> list[dict]:
    """Загрузка данных из Excel"""
```
### 🎀 decorators.py
```python
@log(filename=None)
def func(*args, **kwargs):
    """Декоратор для логирования вызовов"""
```    
### ♻️ generators.py
```python
def filter_by_currency(transactions, currency) -> Iterator[dict]:
    """Фильтр транзакций по валюте"""
def card_number_generator(start, end) -> Iterator[str]:
    """Генератор номеров карт 0000...0001 до 0000...9999"""
```
### 🚀 Быстрый старт
### Установите зависимости:

```bash
pip install pandas openpyxl python-dotenv requests
```
### Пример использования:

```python
from src.widget import mask_account_card
from src.processing import sort_by_date

print(mask_account_card("Счет 12345678901234567890"))  # → "Счет **7890"
transactions = sort_by_date(load_csv_transactions("data.csv"))
```
### 📊 Особенности
* Поддержка JSON/CSV/Excel форматов

* Конвертация валют через API

* Детальное логирование операций

* Генераторы для потоковой обработки

* Полная аннотация типов

### 📝 Логирование
### Все операции записываются в папку logs/:

* masks.log - маскирование данных

* widget.log - форматирование вывода

* processing.log - фильтрация и сортировка
### 🌐 Внешние зависимости
* Конвертация валют через exchangeratesapi.io