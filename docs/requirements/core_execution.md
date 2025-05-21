# core.execution 모듈 사양

| 객체 | 설명 |
|------|------|
| `OrderExecutor` | 실제 주문 또는 모의 주문을 수행합니다. `execute(signal)` 메서드를 제공하며 시뮬레이션 여부에 따라 로그를 남깁니다. |
| `OrderWorker` | RabbitMQ 대신 asyncio.Queue를 사용하여 주문 이벤트를 소비하고 DB에 기록하는 비동기 워커 |
