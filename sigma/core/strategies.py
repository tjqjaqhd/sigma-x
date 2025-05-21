class BaseStrategy:
    def generate_signals(self, market_data: dict):
        raise NotImplementedError


class DummyStrategy(BaseStrategy):
    def generate_signals(self, market_data: dict):
        # 간단한 더미 신호 생성 예시
        for _ in range(5):
            yield "BUY"
            yield "SELL"
