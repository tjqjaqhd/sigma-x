# 컴포넌트 설명

## 컨테이너: main - SIGMA-X 가동 환경

| 이름 | 타입 | 이미지 | 설명 |
| --- | --- | --- | --- |
| data_collector | service | docker.io/sigma/data_collector:latest | 시세 데이터를 수집하는 모듈.  외부 거래소나 데이터 소스에서 시세 정보를 받아 다른 컴포넌트로 전달합니다.  예시: <br> ````python<br>collector = DataCollector()<br>collector.run()<br>```` |
| trade_executor | service | docker.io/sigma/trade_executor:latest | 매매 로직을 실행하는 컴포넌트.  수집된 시세 데이터를 바탕으로 주문을 생성하고, 필요한 경우 결과를 저장합니다.  예시: <br> ````python<br>executor = TradeExecutor()<br>executor.run()<br>```` |
| redis | database | docker.io/library/redis:7 | 애플리케이션용 Redis 인터페이스.  키-값 저장소인 Redis와의 연결을 관리하며 데이터 읽기와 쓰기를 담당합니다.  예시: <br> ````python<br>store = Redis()<br>store.run()<br>```` |
