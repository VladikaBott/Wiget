from pathlib import Path

import pandas as pd

from logger import setup_logger

logger = setup_logger("file_processor", "file_processor")


def load_csv_transactions(file_path: str) -> list[dict]:
    """
    Загружает транзакции из CSV-файла.
    """
    try:
        if not Path(file_path).exists():
            logger.error(f"CSV-файл не найден: {file_path}")
            return []

        data_frame = pd.read_csv(file_path)
        transactions = data_frame.to_dict("records")
        logger.info(f"Загружено {len(transactions)} транзакций из CSV")
        return transactions

    except pd.errors.EmptyDataError:
        logger.error("CSV-файл пуст")
    except Exception as error:
        logger.exception(f"Ошибка загрузки CSV: {str(error)}")
    return []


def load_excel_transactions(file_path: str) -> list[dict]:
    """Загружает транзакции из Excel-файла."""
    try:
        if not Path(file_path).exists():
            logger.error(f"Excel-файл не найден: {file_path}")
            return []

        data_frame = pd.read_excel(file_path)
        transactions = data_frame.to_dict("records")
        logger.info(f"Загружено {len(transactions)} транзакций из Excel")
        return transactions

    except pd.errors.EmptyDataError:
        logger.error("Excel-файл пуст")
    except Exception as error:
        logger.exception(f"Ошибка загрузки Excel: {str(error)}")
    return []
