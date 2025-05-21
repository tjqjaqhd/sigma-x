from sigma.utils.logger import logger


class DataCollector:
    """시장 데이터를 가져오는 클래스."""

    def fetch_market_data(self) -> dict:
        """시장 데이터를 반환합니다 (더미 데이터)."""
        logger.info("시장 데이터 수집")
        return {"price": 0.0}
