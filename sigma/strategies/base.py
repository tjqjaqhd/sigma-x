import pandas as pd


class BaseStrategy:
    """전략 기본 클래스"""

    def generate_signal(self, data: pd.DataFrame) -> str | None:
        raise NotImplementedError
