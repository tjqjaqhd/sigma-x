import logging
from logging.handlers import RotatingFileHandler


def init_logger(level: int = logging.INFO, log_file: str = "sigma.log") -> logging.Logger:
    """로거를 초기화하고 반환합니다."""
    handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
    logging.basicConfig(level=level, handlers=[handler, logging.StreamHandler()])
    return logging.getLogger("sigma")


logger = init_logger()

__all__ = ["logger", "init_logger"]
