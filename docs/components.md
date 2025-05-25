# 컴포넌트 설명

## 컨테이너: main - SIGMA-X 가동 환경

| 이름 | 타입 | 이미지 | 설명 |
| --- | --- | --- | --- |
| data_collector | service | docker.io/sigma/data_collector:latest | 비동기 WebSocket 연결을 통해 시세 데이터를 수신하고 Redis 채널로 발행합니다.  예시: <br> ````python
collector = DataCollector()
await collector.run()
```` |
| trade_executor | service | docker.io/sigma/trade_executor:latest | Redis 채널을 구독해 이동평균 교차 전략을 실행하고 주문 결과를 저장합니다.  예시: <br> ````python
executor = TradeExecutor()
await executor.run()
```` |
| redis | database | docker.io/library/redis:7 | 애플리케이션용 Redis 인터페이스.  키-값 저장소인 Redis와의 연결을 관리하며 데이터 읽기와 쓰기를 담당합니다.  예시: <br> ````python<br>store = Redis()<br>store.run()<br>```` |
