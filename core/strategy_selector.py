class StrategySelector:
    """전략 선택 로직을 담당."""

    def __init__(self, strategies):
        self.strategies = strategies

    def select_strategy(self, market_conditions):
        """시장 조건에 따라 전략 선택."""
        for strategy in self.strategies:
            if strategy.is_suitable(market_conditions):
                return strategy
        return None