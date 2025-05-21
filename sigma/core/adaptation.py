class RegimeDetector:
    """단순 시장 국면 탐지기."""

    def detect(self, prices: list[float]) -> str:
        if len(prices) < 2:
            return "unknown"
        return "bull" if prices[-1] > prices[0] else "bear"


class ParamAdjuster:
    """전략 파라미터를 DB에 반영합니다."""

    def __init__(self, session_factory):
        self.SessionLocal = session_factory

    def update_parameter(self, name: str, value: str) -> None:
        session = self.SessionLocal()
        try:
            from sigma.data.models import StrategyParam

            param = session.get(StrategyParam, name)
            if param:
                param.value = value
            else:
                param = StrategyParam(name=name, value=value)
                session.add(param)
            session.commit()
        finally:
            session.close()


class QualityAssessment:
    """간단한 성과 평가 도구."""

    def evaluate(self, returns: list[float]) -> float:
        if not returns:
            return 0.0
        return sum(returns) / len(returns)


class FeedbackMechanism:
    """평가 결과를 기록하는 메커니즘."""

    def __init__(self) -> None:
        self.records: list[float] = []

    def record(self, metric: float) -> None:
        self.records.append(metric)
