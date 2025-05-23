"""추가 초기화 단계 모듈.

캐시 초기화 이후 실행되어 알림 서비스 토큰 검증 등 부수 작업을 수행한다. 사양은
``docs/4_development/module_specs/common/AdditionalSetup_Spec.md`` 를 따른다.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, Optional


class AdditionalSetup:
    def __init__(self, tmp_dir: str = "/tmp/sigma", logger: Optional[logging.Logger] = None) -> None:
        self.tmp_dir = tmp_dir
        self.logger = logger or logging.getLogger(__name__)

    def verify_tokens(self, config: Dict[str, Any]) -> bool:
        slack = config.get("slack_token")
        telegram = config.get("telegram_token")
        if not slack or not telegram:
            self.logger.error("알림 토큰 누락")
            return False
        return True

    def run(self, config: Dict[str, Any]) -> bool:
        if not self.verify_tokens(config):
            return False
        os.makedirs(self.tmp_dir, exist_ok=True)
        self.logger.debug("임시 디렉터리 생성: %s", self.tmp_dir)
        return True

