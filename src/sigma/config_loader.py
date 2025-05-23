"""애플리케이션 설정 로더.

YAML 파일과 환경 변수 값을 병합하여 설정 딕셔너리를 제공한다. 자세한 사양은
``docs/4_development/module_specs/common/ConfigLoader_Spec.md`` 를 참고한다.
"""

from __future__ import annotations

import os
import logging
from typing import Any, Dict

import yaml
from sigma.common.logging_service import get_logger


class ConfigLoader:
    """설정 파일을 로드하고 캐싱한다."""

    def __init__(
        self,
        default_path: str = "config.yaml",
        env_prefix: str = "SIGMA_",
        logger: logging.Logger | None = None,
    ) -> None:
        self.default_path = default_path
        self.env_prefix = env_prefix
        self.logger = logger or get_logger(__name__)
        self.config: Dict[str, Any] = {}

    def load_yaml(self, path: str) -> Dict[str, Any]:
        with open(path, "r") as fp:
            return yaml.safe_load(fp) or {}

    def _merge_env(self, data: Dict[str, Any]) -> Dict[str, Any]:
        for key, value in os.environ.items():
            if key.startswith(self.env_prefix):
                data[key[len(self.env_prefix) :].lower()] = value
        return data

    def load(self, path: str | None = None) -> Dict[str, Any]:
        path = path or self.default_path
        try:
            data = self.load_yaml(path)
        except FileNotFoundError:
            self.logger.warning("설정 파일을 찾을 수 없음: %s", path)
            data = {}
        self.config = self._merge_env(data)
        return self.config

    def reload(self) -> Dict[str, Any]:
        return self.load(self.default_path)

    def get(self, key: str, default: Any | None = None) -> Any:
        return self.config.get(key, default)
