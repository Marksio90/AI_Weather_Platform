import logging
import os
from typing import Optional


# mapowanie string → poziom logowania
_LEVELS = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}


def _get_log_level_from_env(default: str = "INFO") -> int:
    level_name = os.getenv("APP_LOG_LEVEL", default).upper()
    return _LEVELS.get(level_name, logging.INFO)


def setup_logging(name: Optional[str] = None) -> logging.Logger:
    """
    Inicjalizuje logowanie w aplikacji.

    - czyta poziom z APP_LOG_LEVEL (INFO/DEBUG/WARNING/ERROR),
    - nie dodaje drugiego handlera jeśli już jest,
    - zwraca logger (możesz od razu użyć: log = setup_logging(__name__))

    Użycie:
        log = setup_logging(__name__)
        log.info("start")
    """
    level = _get_log_level_from_env()
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # jeżeli nie ma jeszcze handlerów (np. pierwszy start), to dodajemy konsolę
    if not root_logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)

    # jeżeli chcemy loggera dla konkretnego modułu:
    if name:
        logger = logging.getLogger(name)
        logger.setLevel(level)
        return logger

    return root_logger
