"""MLModule: 머신러닝 보조 지표 계산 모듈.

사양: docs/4_development/module_specs/core/MLModule_Spec.md
사전 학습된 모델을 로드해 전략 신호 보조값을 제공한다.
"""

from __future__ import annotations

import os
import pickle
from typing import Any, Dict

import numpy as np
import pandas as pd
from sigma.common.logging_service import get_logger


class MLModule:
    """경량 머신러닝 추론기를 제공한다."""

    def __init__(self, model_path: str = "model.pkl", logger=None) -> None:
        self.model_path = model_path
        self.logger = logger or get_logger(__name__)
        self.model: Dict[str, Any] | None = None

    def load_model(self) -> None:
        """디스크에서 모델을 읽어 들인다."""
        if not os.path.exists(self.model_path):
            self.logger.error("모델 파일을 찾을 수 없음: %s", self.model_path)
            self.model = None
            return

        with open(self.model_path, "rb") as fp:
            self.model = pickle.load(fp)
        self.logger.info("모델 로드 완료: %s", self.model_path)

    def run_inference(self, df: pd.DataFrame) -> Dict[str, float]:
        """마지막 행 데이터를 사용해 신호 값을 계산한다."""
        if self.model is None:
            self.logger.warning("모델이 로드되지 않아 기본값 반환")
            return {"signal": 0.0}

        try:
            features = df.values[-1]
            weights = np.asarray(self.model.get("weights"))
            bias = float(self.model.get("bias", 0.0))
            score = float(np.dot(features, weights) + bias)
            signal = float(1 / (1 + np.exp(-score)))
            return {"signal": signal}
        except Exception as exc:  # pragma: no cover - 예외 로깅
            self.logger.exception("모델 추론 실패: %s", exc)
            return {"signal": 0.0}


def predict_signal(module: MLModule, df: pd.DataFrame) -> Dict[str, float]:
    """단독 함수 형태로 신호 값을 계산한다."""

    return module.run_inference(df)
