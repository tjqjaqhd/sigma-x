# 컴포넌트 설명

## 컨테이너: main - SIGMA-X 가동 환경

| 이름 | 타입 | 이미지 | 설명 |
| --- | --- | --- | --- |
| data_collector | service | docker.io/sigma/data_collector:latest | 시세 데이터를 수집하는 모듈.  외부 거래소나 데이터 소스에서 시세 정보를 받아 Redis 채널로 전달합니다.  예시:     >>> collector = DataCollector()     >>> await collector.run() |
| trade_executor | service | docker.io/sigma/trade_executor:latest | 거래를 실행하고 주문을 처리합니다. |
| redis | database | docker.io/library/redis:7 | - |

## 컨테이너: scheduler - 전략 교체 및 성과 리포트 스케줄러

| 이름 | 타입 | 이미지 | 설명 |
| --- | --- | --- | --- |
| sigma_scheduler | service | docker.io/sigma/sigma_scheduler:latest | StrategySelector를 실행하는 백그라운드 스케줄러. |
