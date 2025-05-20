class BaseStrategy:
    def generate_signals(self):
        raise NotImplementedError


class DummyStrategy(BaseStrategy):
    def generate_signals(self):
        # 간단한 더미 신호 생성 예시
        for _ in range(5):
            yield "BUY"
            yield "SELL"
