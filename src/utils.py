# utils.py
import json
import os
from pathlib import Path

from logger import setup_logger

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

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON: {str(e)}")
    except PermissionError as e:
        logger.error(f"Нет доступа к файлу: {str(e)}")
    except OSError as e:
        logger.error(f"Ошибка файловой системы: {str(e)}")
    except Exception as e:
        logger.exception(f"Неизвестная ошибка: {str(e)}")

    return []
