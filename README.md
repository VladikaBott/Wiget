# BankingWidget

## Описание
Учебный проект "Банковский виджет"

## Установка и запуск
Установка не требуется.
Запуск производится через файлы src/masks.py, src/widget.py, src/processing.py.

## Авторы
Проект разрабатывается в процессе освоения образовательной программы Skypro.



# Модуль generators

Модуль содержит генераторы для обработки финансовых данных.

## Функции

### 1. `filter_by_currency(transactions, currency)`
Фильтрует транзакции по заданной валюте.

**Параметры:**
- `transactions` - список транзакций (словарей)
- `currency` - код валюты (например, "USD")

**Возвращает:**
- Итератор по транзакциям с указанной валютой

# Модуль masks

Модуль содержит функции для маскирования номеров банковских карт и счетов.

## Функции

### `get_mask_card_number(card_number: str) -> str`
Маскирует номер банковской карты, оставляя первые 6 и последние 4 цифры.

**Параметры:**
- `card_number` - строка с номером карты (16 цифр, может содержать пробелы)

**Возвращает:**
- Маскированный номер в формате `XXXX XX** **** XXXX`

**Исключения:**
- `ValueError` - если номер не содержит 16 цифр

**Пример использования:**
```python
from masks import get_mask_card_number

masked_card = get_mask_card_number("1234567890123456")
print(masked_card)  # "1234 56** **** 3456"

masked_card = get_mask_card_number("1234 5678 9012 3456")
print(masked_card)  # "1234 56** **** 3456"

# Модуль processing

Модуль содержит функции для обработки банковских операций.

## Функции

### `filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]`
Фильтрует список операций по статусу.

**Параметры:**
- `operations` - список операций (словарей)
- `state` - статус для фильтрации (по умолчанию "EXECUTED")

**Возвращает:**
- Список операций с указанным статусом

**Пример использования:**
```python
from processing import filter_by_state

operations = [
    {"id": 1, "state": "EXECUTED"},
    {"id": 2, "state": "PENDING"},
    {"id": 3, "state": "EXECUTED"}
]

executed_ops = filter_by_state(operations)
print(executed_ops)  # [{"id": 1, "state": "EXECUTED"}, {"id": 3, "state": "EXECUTED"}]

pending_ops = filter_by_state(operations, "PENDING")
print(pending_ops)  # [{"id": 2, "state": "PENDING"}]

## Логирующий декоратор для Python

## Установка
Просто скопируйте этот код в файл `decorators.py`:

```python
from functools import wraps
from datetime import datetime

def log(filename=None, level="INFO", ignore_exceptions=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Форматирование сообщения
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            call_msg = f"{timestamp} [{level}] {func.__name__} - Called with args={args}, kwargs={kwargs}"
            
            try:
                # Вывод/запись лога вызова
                if filename:
                    with open(filename, 'a') as f:
                        f.write(call_msg + "\n")
                else:
                    print(call_msg)
                
                result = func(*args, **kwargs)
                
                # Лог успешного выполнения
                success_msg = f"{timestamp} [{level}] {func.__name__} - Returned: {result}"
                if filename:
                    with open(filename, 'a') as f:
                        f.write(success_msg + "\n")
                else:
                    print(success_msg)
                
                return result
            
            except Exception as e:
                if ignore_exceptions and type(e) in ignore_exceptions:
                    raise
                
                # Лог ошибки
                error_msg = f"{timestamp} [ERROR] {func.__name__} - Raised {type(e).__name__}: {str(e)}"
                if filename:
                    with open(filename, 'a') as f:
                        f.write(error_msg + "\n")
                else:
                    print(error_msg)
                raise

        return wrapper
    return decorator