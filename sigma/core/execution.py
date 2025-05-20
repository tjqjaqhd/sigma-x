from sigma.utils.logger import logger


class OrderExecutor:
    """Execute real or simulated orders."""

    def __init__(self, is_simulation: bool = True):
        self.is_simulation = is_simulation

    def execute(self, signal: str) -> None:
        if self.is_simulation:
            logger.info(f"[SIM] execute {signal}")
        else:
            # TODO: 실제 주문 로직을 구현합니다.
            logger.info(f"execute {signal}")
