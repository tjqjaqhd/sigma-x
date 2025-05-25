# 컴포넌트 설명

## 컨테이너: main - SIGMA-X 가동 환경

| 이름 | 타입 | 이미지 | 설명 |
| ---- | ---- | ------ | ---- |
| data_collector | service | docker.io/sigma/data_collector:latest | 비동기 WebSocket 연결로 시세 데이터를 수신한 뒤 RabbitMQ 큐에 넣습니다. 예시:<br>```python
collector = DataCollector()
await collector.run()
``` |
| trade_executor | service | docker.io/sigma/trade_executor:latest | RabbitMQ 큐에서 데이터를 가져와 이동평균 교차 전략을 실행하고 주문 결과를 Redis에 저장합니다. 예시:<br>```python
executor = TradeExecutor()
await executor.run()
``` |
| api_server | service | docker.io/sigma/api_server:latest | FastAPI 기반 REST/WS 인터페이스를 제공하여 시스템 상태 확인과 주문 조회, 실시간 데이터 구독 기능을 지원합니다. 예시:<br>```python
server = APIServer()
server.run()
``` |
| redis | database | docker.io/library/redis:7 | 애플리케이션용 Redis 인터페이스. 키-값 저장소와의 연결을 관리하며 데이터 읽기와 쓰기를 담당합니다. 예시:<br>```python
store = Redis()
store.run()
``` |
