from __future__ import annotations

from prometheus_client import Counter, Summary, Gauge, generate_latest

# 처리된 틱 수
ticks_processed_total = Counter(
    "ticks_processed_total",
    "수집기가 처리한 전체 틱 수",
)

# 주문 처리 지연 시간
order_processing_delay_seconds = Summary(
    "order_processing_delay_seconds",
    "주문 처리 지연 시간(초)",
)

# 최근 수익률
recent_profit = Gauge(
    "recent_profit",
    "최근 계산된 수익률",
)


def record_tick() -> None:
    """틱 처리량을 1 증가."""
    ticks_processed_total.inc()


def record_order_delay(delay: float) -> None:
    """주문 지연 시간 기록."""
    order_processing_delay_seconds.observe(delay)


def set_recent_profit(value: float) -> None:
    """최근 수익률 설정."""
    recent_profit.set(value)


def metrics_text() -> str:
    """현재 메트릭 데이터를 텍스트 포맷으로 반환."""
    return generate_latest().decode()
