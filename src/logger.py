import logging
import os
from pathlib import Path


def setup_logger(name: str, log_file: str) -> logging.Logger:
    """Настройка логгера с записью в файл в папке logs/ корня проекта."""

    # Путь до корня проекта (на уровень выше src/)
    project_root = Path(__file__).parent.parent
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)  # Создаем папку, если её нет

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = logging.FileHandler(filename=logs_dir / f"{log_file}.log", mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
