import json
import os
import re
from collections import Counter
from typing import Dict, List

from src.logger import setup_logger

logger = setup_logger("utils", "utils")  # Файл: logs/utils.log в корне проекта


def load_transactions(file_path: str) -> list[dict]:
    """Загружает транзакции из JSON-файла."""
    try:
        if not os.path.exists(file_path):
            logger.warning(f"Файл не найден: {file_path}")
            return []

        if os.path.getsize(file_path) == 0:
            logger.warning(f"Файл пуст: {file_path}")
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            result = data if isinstance(data, list) else []
            logger.info(f"Успешно загружено {len(result)} транзакций")
            return result

    except PermissionError as e:
        logger.error(f"Нет доступа к файлу: {str(e)}")
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON: {str(e)}")
    except OSError as e:  # Общий обработчик для других ошибок файловой системы
        logger.error(f"Ошибка файловой системы: {str(e)}")
    except Exception as e:
        logger.exception(f"Неизвестная ошибка: {str(e)}")

    return []


def filter_operations_by_description(operations: List[Dict], search_string: str) -> List[Dict]:
    """
    Фильтрует список банковских операций, оставляя только те,
    в описании которых присутствует заданная строка (с учетом регистра).
    """
    if not search_string:
        logger.debug("Получена пустая строка для поиска, возвращаем пустой список")
        return []

    try:
        # Компилируем регулярное выражение для поиска строки (экранируем специальные символы)
        pattern = re.compile(re.escape(search_string))

        # Фильтруем операции, оставляя те, где описание совпадает с шаблоном
        filtered_ops = [op for op in operations if op.get("description") and pattern.search(op["description"])]

        logger.info(f"Поиск по строке '{search_string}': найдено {len(filtered_ops)} операций")
        return filtered_ops

    except re.error as e:
        logger.error(f"Ошибка в регулярном выражении: {str(e)}")
        return []
    except Exception as e:
        logger.exception(f"Неизвестная ошибка при фильтрации операций: {str(e)}")
        return []


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций для каждой указанной категории.
    Категория определяется по точному совпадению строки в поле 'description'.

    Args:
        data: Список словарей с данными о банковских операциях.
        categories: Список категорий для поиска в описании.

    Returns:
        Словарь, где ключи - названия категорий, значения - количество операций.
    """
    try:
        if not categories:
            logger.info("Получен пустой список категорий, возвращаем пустой словарь")
            return {}

        # Извлекаем все описания операций
        all_descriptions = [op.get("description", "") for op in data]

        # Создаем счетчик для всех описаний
        description_counter = Counter(all_descriptions)

        # Формируем результат только для запрошенных категорий
        result = {}
        for category in categories:
            result[category] = description_counter.get(category, 0)

        logger.info(f"Подсчет операций по категориям: {result}")
        return result

    except Exception as e:
        logger.exception(f"Ошибка при подсчете операций по категориям: {str(e)}")
        return {category: 0 for category in categories}


def count_operations_by_category(operations: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций для каждой указанной категории.
    Категория определяется по точному совпадению строки в поле 'description'.
    """
    try:
        # Извлекаем все описания операций в один список
        all_descriptions = [op.get("description", "") for op in operations]

        # Создаем счетчик для всех описаний
        description_counter = Counter(all_descriptions)

        # Формируем результат только для запрошенных категорий
        result = {category: description_counter.get(category, 0) for category in categories}

        logger.info(f"Подсчет операций по категориям: {result}")
        return result

    except Exception as e:
        logger.exception(f"Ошибка при подсчете операций по категориям: {str(e)}")
        return {category: 0 for category in categories}
