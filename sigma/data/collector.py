from sigma.utils.logger import logger


class DataCollector:
    """시장 데이터를 가져오는 클래스."""

    def fetch_market_data(self) -> dict:
 ncqct1 - 코덱스 / md 
        """시장 데이터를 반환합니다 (더미 데이터)."""
        logger.info("시장 데이터 수집")
        return {"price": 0.0}

        """시장 가격 데이터를 반환합니다."""
        # TODO: 실제 데이터 수집 로직을 구현합니다.
        logger.info("Fetching market data")
        return {"price": 100.0}
 main
