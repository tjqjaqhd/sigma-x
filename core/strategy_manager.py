class StrategyManager:
    """전략 객체를 관리하고 교체하는 역할."""

    def __init__(self):
        self.current_strategy = None

    def set_strategy(self, strategy):
        """전략 설정."""
        self.current_strategy = strategy

    def get_strategy(self):
        """현재 전략 반환."""
        return self.current_strategy