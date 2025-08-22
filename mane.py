from datetime import datetime
from typing import Dict, List

from src.utils import count_operations_by_category, filter_operations_by_description, load_transactions


def display_operation(op: Dict, index: int = None) -> None:
    """Отображает одну операцию в заданном формате."""
    prefix = f"{index}. " if index is not None else ""
    date = op.get("date", "Дата не указана")
    description = op.get("description", "Без описания")

    # Форматирование счета/карты (упрощенная версия)
    from_info = op.get("from", "")
    to_info = op.get("to", "")

    amount = op.get("amount", 0)
    currency = op.get("currency", "")

    print(f"{prefix}{date} {description}")
    if from_info:
        print(f"   {from_info} -> {to_info}")
    else:
        print(f"   {to_info}")
    print(f"   Сумма: {amount} {currency}")
    print()


def display_operations(operations: List[Dict], title: str) -> None:
    """Отображает список операций."""
    if not operations:
        print(f"{title}: не найдено операций")
        return

    print(f"\n{title}:")
    print("=" * 50)
    for i, op in enumerate(operations, 1):
        display_operation(op, i)
    print(f"Всего банковских операций в выборке: {len(operations)}")
    print("=" * 50)


def filter_by_status(operations: List[Dict], target_status: str) -> List[Dict]:
    """Фильтрует операции по статусу (регистронезависимо)."""
    if not target_status:
        return operations

    target_status_lower = target_status.lower()
    return [op for op in operations if op.get("state", "").lower() == target_status_lower]


def sort_by_date(operations: List[Dict], reverse: bool = False) -> List[Dict]:
    """Сортирует операции по дате."""

    def get_date(op):
        date_str = op.get("date", "")
        try:
            return datetime.strptime(date_str, "%d.%m.%Y")
        except (ValueError, TypeError):
            return datetime.min

    return sorted(operations, key=get_date, reverse=reverse)


def filter_by_currency(operations: List[Dict], currency: str) -> List[Dict]:
    """Фильтрует операции по валюте."""
    if not currency:
        return operations

    currency_lower = currency.lower()
    return [op for op in operations if op.get("currency", "").lower() == currency_lower]


def get_user_choice(prompt: str, valid_choices: List[str]) -> str:
    """Получает выбор пользователя с валидацией."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_choices:
            return choice
        print(f"Неверный выбор. Доступные варианты: {', '.join(valid_choices)}")


def get_status_from_user() -> str:
    """Получает статус операции от пользователя."""
    valid_statuses = ["executed", "canceled", "pending"]

    print("\nДоступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

    while True:
        status = input("Введите статус, по которому необходимо выполнить фильтрацию: ").strip().lower()

        if status in valid_statuses:
            return status.upper()
        else:
            print(f'Статус операции "{status.upper()}" недоступен.')


def main():
    """Основная функция программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # Выбор типа файла
    file_choice = get_user_choice("Ваш выбор (1-3): ", ["1", "2", "3"])

    file_types = {"1": ("JSON", ".json"), "2": ("CSV", ".csv"), "3": ("XLSX", ".xlsx")}

    file_type, extension = file_types[file_choice]
    print(f"\nДля обработки выбран {file_type}-файл.")

    # Загрузка файла (пока только JSON поддерживается)
    if file_choice != "1":
        print(f"Обработка {file_type}-файлов пока не реализована.")
        return

    file_path = input("Введите путь к JSON-файлу: ").strip()
    operations = load_transactions(file_path)

    if not operations:
        print("Не удалось загрузить операции из файла.")
        return

    # Фильтрация по статусу
    status = get_status_from_user()
    filtered_operations = filter_by_status(operations, status)

    print(f"\nОперации отфильтрованы по статусу '{status.upper()}'")
    print(f"Найдено операций: {len(filtered_operations)}")

    if not filtered_operations:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Сортировка по дате
    sort_choice = get_user_choice("\nОтсортировать операции по дате? (да/нет): ", ["да", "нет"])

    if sort_choice == "да":
        order_choice = get_user_choice(
            "Отсортировать по возрастанию или по убыванию? (возрастанию/убыванию): ", ["возрастанию", "убыванию"]
        )
        reverse = order_choice == "убыванию"
        filtered_operations = sort_by_date(filtered_operations, reverse)
        print("Операции отсортированы по дате.")

    # Фильтрация по валюте
    currency_choice = get_user_choice("\nВыводить только рублевые транзакции? (да/нет): ", ["да", "нет"])

    if currency_choice == "да":
        filtered_operations = filter_by_currency(filtered_operations, "RUB")
        print("Оставлены только рублевые транзакции.")

    # Поиск по описанию
    search_choice = get_user_choice(
        "\nОтфильтровать список транзакций по определенному слову в описании? (да/нет): ", ["да", "нет"]
    )

    if search_choice == "да":
        search_word = input("Введите слово для поиска в описании: ").strip()
        if search_word:
            filtered_operations = filter_operations_by_description(filtered_operations, search_word)
            print(f"Выполнен поиск по слову '{search_word}'.")

    # Вывод результатов
    if not filtered_operations:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print("\nРаспечатываю итоговый список транзакций...")
        display_operations(filtered_operations, "Итоговый список транзакций")

        # Дополнительная статистика
        categories = ["Перевод организации", "Оплата услуг связи", "Доставка еды", "Пополнение счета"]
        stats = count_operations_by_category(filtered_operations, categories)
        print("\nСтатистика по категориям:")
        for category, count in stats.items():
            if count > 0:
                print(f"{category}: {count} операций")


if __name__ == "__main__":
    main()
