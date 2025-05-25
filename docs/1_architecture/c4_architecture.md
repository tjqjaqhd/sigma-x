# SIGMA-X C4 아키텍처 다이어그램

## 1. 시스템 컨텍스트 다이어그램 (C1)

```mermaid
C4Context
title SIGMA-X System Context

Person(trader, "Trader (ID 1)", "Uses the trading system")
Person(admin, "Administrator (ID 2)", "Manages the system")

System(sigma, "SIGMA-X (ID 3)", "An automated trading system")

Rel(trader, sigma, "Trade & view")
Rel(admin, sigma, "Manage system")
linkStyle 0,1 stroke:#000,stroke-width:3px;
```

## 2. 컨테이너 다이어그램 (C2)

컨테이너 간 상호작용을 그린 다이어그램은
[`c2_container.mmd`](c2_container.mmd) 파일에서 확인할 수 있습니다.

## 3. API 컴포넌트 다이어그램 (C3)

API 내부 구조를 보여 주는 다이어그램은
[`c3_api.mmd`](c3_api.mmd) 파일에서 확인할 수 있습니다.

## 4. Bot 컴포넌트 다이어그램 (C4)

Bot 서비스 구성은 [`c4_bot.mmd`](c4_bot.mmd) 파일에서 확인할 수 있습니다.

## 다이어그램 설명

### 1. 시스템 컨텍스트 다이어그램 (C1)
- 전체 시스템의 맥락을 보여주는 최상위 다이어그램
- Trader와 Administrator 사용자와 SIGMA-X 시스템 간의 관계를 표현
- 시스템의 주요 목적과 사용자 상호작용을 보여줌

### 2. 컨테이너 다이어그램 (C2)
- 시스템의 주요 구성 요소들을 보여주는 다이어그램
- 6개의 주요 컨테이너:
  - Database (PostgreSQL)
  - Redis (Pub/Sub)
  - Task Queue (RabbitMQ)
  - Analytics (Python)
  - API (FastAPI)
    - `/health`, `/trade`, `/ws` 엔드포인트 제공
  - Bot (Python)
- 컨테이너 간의 상호작용과 데이터 흐름을 표현

### 3. API 컴포넌트 다이어그램 (C3)
- API 서비스의 내부 구조를 보여주는 다이어그램
- 4개의 주요 컴포넌트:
  - REST (HTTP 처리)
  - WS (WebSocket 처리)
  - Auth (인증)
  - Health (상태 모니터링)
- 컴포넌트 간의 상호작용과 외부 시스템과의 관계를 표현

### 4. Bot 컴포넌트 다이어그램 (C4)
- Bot 서비스의 내부 구조를 보여주는 다이어그램
- 4개의 주요 컴포넌트:
  - Strategy (전략 실행)
  - Risk (리스크 관리)
  - Exec (주문 실행)
  - Sim (시뮬레이션)
- 컴포넌트 간의 상호작용과 데이터 흐름을 표현

## 참고사항
- 이 다이어그램들은 C4 모델 표준을 따름
- Mermaid 문법을 사용하여 작성됨
- https://mermaid.live 에서 실시간으로 확인 가능
