import logging


def init_logger(level: int = logging.INFO) -> logging.Logger:
    """로거를 초기화하고 반환합니다."""
    logging.basicConfig(level=level)
    return logging.getLogger("sigma")


logger = init_logger()

__all__ = ["logger", "init_logger"]
