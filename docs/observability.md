# 관찰성 기능

SIGMA-X는 Prometheus, Grafana, Alertmanager를 이용해 시스템 상태를 모니터링합니다.

- **Prometheus**: `/metrics` 엔드포인트에서 노출되는 메트릭을 주기적으로 수집합니다.
- **Grafana**: Prometheus를 데이터 소스로 사용해 대시보드를 구성합니다.
- **Alertmanager**: 임계치 초과 시 Slack으로 알림을 전송합니다.

메트릭 예시는 다음과 같습니다.

- `ticks_processed_total`: 처리된 틱 수
- `order_processing_delay_seconds`: 주문 처리 지연 시간
- `recent_profit`: 최근 수익률
