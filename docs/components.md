# 컴포넌트 설명

## 컨테이너: main - SIGMA-X 가동 환경

| 이름 | 타입 | 이미지 | 설명 |
| --- | --- | --- | --- |
| data_collector | service | docker.io/sigma/data_collector:latest | - |
| trade_executor | service | docker.io/sigma/trade_executor:latest | - |
| redis | database | docker.io/library/redis:7 | - |
