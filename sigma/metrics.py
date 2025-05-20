from sigma.utils.logger import logger


class Metrics:
    def __init__(self) -> None:
        self.data = {}

    def inc(self, key: str) -> None:
        self.data[key] = self.data.get(key, 0) + 1


def init_metrics() -> Metrics:
    """메트릭 수집 객체를 초기화합니다."""
    logger.info("메트릭 시스템 초기화")
    return Metrics()
