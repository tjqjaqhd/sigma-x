class BaseStrategy:
    def generate_signals(self, data: dict):
        """시장 데이터를 입력받아 매매 신호를 생성합니다."""
        raise NotImplementedError


class DummyStrategy(BaseStrategy):
    def generate_signals(self, data: dict):
        """가격이 0보다 크면 매수 후 매도 신호를 생성합니다."""
        price = data.get("price", 0)
        for _ in range(5):
            if price > 0:
                yield "BUY"
                yield "SELL"
