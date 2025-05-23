"""로깅 설정 모듈.

`Logger` 클래스와 전역 설정 함수 ``setup_logger`` 를 제공한다. 사양은
``docs/4_development/module_specs/common/Logger_Spec.md`` 를 참조한다.
"""

from __future__ import annotations

import logging
from typing import Optional


def setup_logger(
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    json_format: bool = False,
) -> logging.Logger:
    """루트 로거를 초기화한다."""

    root = logging.getLogger()
    root.setLevel(level)

    if json_format:
        fmt = (
            '{"time":"%(asctime)s","level":"%(levelname)s",'
            '"name":"%(name)s","msg":"%(message)s"}'
        )
    else:
        fmt = "%(asctime)s %(levelname)s %(name)s: %(message)s"
    formatter = logging.Formatter(fmt)

    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    root.handlers = [stream]

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)

    return root


class Logger:
    """로거 인스턴스를 래핑해 이름별 로거를 제공한다."""

    def __init__(self, name: str = "sigma") -> None:
        self._logger = logging.getLogger(name)

    def get_logger(self) -> logging.Logger:
        """내부 로거 객체를 반환한다."""

        return self._logger

