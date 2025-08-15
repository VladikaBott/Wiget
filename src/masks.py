from logger import setup_logger

logger = setup_logger("masks", "masks")


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты."""
    try:
        cleaned_number = card_number.replace(" ", "")
        if len(cleaned_number) != 16:
            error_msg = f"Некорректная длина номера: {len(cleaned_number)}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        masked = f"{cleaned_number[:4]} {cleaned_number[4:6]}** **** {cleaned_number[-4:]}"
        logger.info(f"Успешно замаскирована карта: {masked}")
        return masked

    except Exception as e:
        logger.exception(f"Ошибка маскирования карты: {str(e)}")
        raise


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счёта."""
    try:
        cleaned_number = account_number.replace(" ", "")
        if len(cleaned_number) < 4:
            error_msg = f"Слишком короткий номер: {len(cleaned_number)}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        masked = f"**{cleaned_number[-4:]}"
        logger.info(f"Успешно замаскирован счёт: {masked}")
        return masked

    except Exception as e:
        logger.exception(f"Ошибка маскирования счёта: {str(e)}")
        raise
