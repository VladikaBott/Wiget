import json
import os


def load_transactions(file_path):
    """
    Загружает транзакции из JSON-файла

    Args:
        file_path: Путь к JSON-файлу

    Returns:
        List[dict]: Список транзакций или пустой список при ошибках
    """
    try:
        if not os.path.exists(file_path):
            return []

        if os.path.getsize(file_path) == 0:
            return []

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []

    except (json.JSONDecodeError, PermissionError, OSError):
        return []