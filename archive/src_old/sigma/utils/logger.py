import logging
from logging.handlers import RotatingFileHandler


def init_logger(level: int = logging.INFO) -> logging.Logger:
    """로거를 초기화하고 반환합니다."""
    logger = logging.getLogger("sigma")
    logger.setLevel(level)
    handler = RotatingFileHandler("sigma.log", maxBytes=1000000, backupCount=3)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = init_logger()

__all__ = ["logger", "init_logger"]
