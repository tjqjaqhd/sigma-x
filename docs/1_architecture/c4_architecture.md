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

```mermaid
C4Container
title SIGMA-X Container

Person(trader, "Trader", "Uses the trading system")
Person(admin, "Administrator", "Manages the system")

System_Boundary(sigma, "SIGMA-X") {
    Container(db, "Database (ID 1)", "PostgreSQL", "Stores trading data")
    Container(redis, "Redis (ID 2)", "Redis", "Handles pub/sub messaging")
    Container(mq, "Task Queue (ID 3)", "RabbitMQ", "Background job queue")
    Container(analytics, "Analytics (ID 4)", "Python", "Backtesting and analysis")
    Container(api, "API (ID 5)", "FastAPI", "Handles REST/WS")
    Container(bot, "Bot (ID 6)", "Python", "Executes strategies")
}

Rel(trader, api, "Trade & view")
Rel(admin, api, "Manage system")
Rel(api, redis, "Publishes")
Rel(api, bot, "Sends jobs")
Rel(bot, db, "RW trades")
Rel(bot, redis, "Publish result")
Rel(analytics, db, "Reads data")
Rel(analytics, mq, "Sends job")
Rel(mq, analytics, "Returns result")
linkStyle 0,1,2,3,4,5 stroke:#000,stroke-width:3px;
linkStyle 6,7,8 stroke-dasharray: 5 5;
```

## 3. API 컴포넌트 다이어그램 (C3)

```mermaid
C4Component
title SIGMA-X API Components

Container_Boundary(api, "API") {
    Component(rest, "REST (ID 1)", "Handles HTTP REST")
    Component(ws, "WS (ID 2)", "WebSocket handling")
    Component(auth, "Auth (ID 3)", "Authentication layer")
    Component(health, "Health (ID 4)", "Health monitoring")
}

Person(trader, "Trader", "Uses the trading system")
ContainerDb(redis, "Redis", "Handles pub/sub messaging")

Rel(trader, rest, "Makes requests")
Rel(rest, auth, "Auth check")
Rel(rest, ws, "WebSocket start")
Rel(rest, health, "Health check")
Rel(ws, redis, "Subscribes")
linkStyle 0,1,2,3,4 stroke:#000,stroke-width:3px;
```

## 4. Bot 컴포넌트 다이어그램 (C4)

```mermaid
C4Component
title SIGMA-X Bot Components

Container_Boundary(bot, "Bot") {
    Component(strat, "Strategy (ID 1)", "Runs strategies")
    Component(risk, "Risk (ID 2)", "Validates risk")
    Component(exec, "Exec (ID 3)", "Executes orders")
    Component(sim, "Sim (ID 4)", "Simulates trades")
}

ContainerDb(db, "Database", "Stores trading data")
ContainerDb(redis, "Redis", "Handles pub/sub messaging")

Rel(strat, risk, "Validate")
Rel(risk, exec, "If ok")
Rel(sim, strat, "Sim input")
Rel(sim, db, "Save results")
linkStyle 0,1 stroke:#000,stroke-width:3px;
linkStyle 2,3 stroke-dasharray: 5 5;
```

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
