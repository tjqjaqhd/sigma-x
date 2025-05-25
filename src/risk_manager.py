class RiskManager:
    """간단한 포지션 기반 리스크 관리기."""

    def __init__(self, max_position: int = 100) -> None:
        self.position = 0
        self.max_position = max_position

    def check(self, signal: str) -> bool:
        if signal == "BUY" and self.position >= self.max_position:
            return False
        if signal == "SELL" and self.position <= 0:
            return False
        return True

    def apply(self, signal: str) -> None:
        if signal == "BUY":
            self.position += 1
        elif signal == "SELL":
            self.position -= 1
