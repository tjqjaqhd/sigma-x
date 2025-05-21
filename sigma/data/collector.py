from sigma.utils.logger import logger


class DataCollector:
    """Fetch market data from external sources."""

    def fetch_market_data(self) -> dict:
        """임시로 고정된 가격 데이터를 반환합니다."""
        logger.info("Fetching market data")
        return {"price": 100.0}
