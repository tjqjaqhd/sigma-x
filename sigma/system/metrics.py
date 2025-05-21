"""메트릭 초기화."""

from prometheus_client import Counter, start_http_server

from sigma.utils.logger import logger

REQUEST_COUNT = Counter("sigma_request_total", "총 요청 수")


def init_metrics(port: int = 8001) -> None:
    """Prometheus 메트릭 수집기를 초기화합니다."""
    start_http_server(port)
    logger.info("메트릭 시스템 초기화")
