from src.sigma.utils.logger import logger


class RiskManager:
    """단순 리스크 관리 모듈."""

    def evaluate(self, signal: str) -> bool:
        """신호의 허용 여부를 판정합니다."""
        if signal not in {"BUY", "SELL"}:
            logger.warning("알 수 없는 신호: %s", signal)
            return False
        return True


class AnomalyDetector:
    """간단한 이상치 탐지기."""

    def detect(self, price: float) -> bool:
        return price <= 0


class NewsHandler:
    """뉴스 기반 이벤트 처리기."""

    def process(self, news: str) -> None:
        logger.info("뉴스 처리: %s", news)
