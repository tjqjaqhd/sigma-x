class BaseStrategy:
    def generate_signals(self, market_data: dict):
        """시장 데이터를 받아 매매 신호를 생성합니다."""
        raise NotImplementedError


class DummyStrategy(BaseStrategy):
    def generate_signals(self, market_data: dict):
        """더미 데이터를 이용해 BUY/SELL 신호를 번갈아 반환합니다."""
        for _ in range(5):
            yield "BUY"
            yield "SELL"
