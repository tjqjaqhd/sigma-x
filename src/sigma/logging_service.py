"""애플리케이션 로깅 서비스.

`docs/4_development/module_specs/common/LoggingService_Spec.md` 사양을 따른다.
"""

from __future__ import annotations

import logging
from logging import Logger
from typing import Optional


class LoggingService:
    """파일 및 콘솔 핸들러를 구성해 로거를 제공한다."""

    def __init__(self, level: str = "INFO", log_path: str = "sigma.log") -> None:
        self.level = level
        self.log_path = log_path
        self._logger = logging.getLogger()
        self.configure()

    def configure(self) -> None:
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        if not self._logger.handlers:
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            self._logger.addHandler(console)

            file_handler = logging.FileHandler(self.log_path)
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)

        self.set_level(self.level)

    def get_logger(self, name: Optional[str] = None) -> Logger:
        return logging.getLogger(name)

    def set_level(self, level: str) -> None:
        self._logger.setLevel(level.upper())

    def rotate(self, new_path: str) -> None:
        """로그 파일을 새 위치로 교체한다."""
        for handler in list(self._logger.handlers):
            if isinstance(handler, logging.FileHandler):
                self._logger.removeHandler(handler)
                handler.close()
        file_handler = logging.FileHandler(new_path)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )
        self._logger.addHandler(file_handler)
        self.log_path = new_path


def setup_logger(level: str = "INFO", log_path: str = "sigma.log") -> Logger:
    """편의 함수: 기본 로거를 설정하고 반환한다."""

    service = LoggingService(level=level, log_path=log_path)
    return service.get_logger()
