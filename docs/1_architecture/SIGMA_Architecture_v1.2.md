# SIGMA Architecture v1.2

## 1. Purpose & Scope

개인 VPS 한 대(4 vCPU / 16 GB)에서

* **실전 거래(LIVE)**
* **실시간 시뮬레이션(SIM)**
* **과거 백테스트(BACKTEST)**
  세 모드가 동일한 코드-경로로 동작하도록 설계한다.

---

## 2. Design Principles

1. 이벤트 기반 비동기(Redis Pub/Sub)
2. 전략·리스크·실행 **단일 책임 모듈**
3. “MVP → 확장” 단계적 복잡도 추가
4. **관찰성 기본 탑재** : Prometheus·Grafana·Alertmanager
5. Docker Compose 단일 호스트 → 필요 시 모듈별 컨테이너 분리

---

## 3. High-Level Diagram (Mermaid)

​flowchart TB

  %% Interfaces Layer
  subgraph Interfaces
    direction TB
    main["run_bot.py:main"]
    backtestCLI["backtest.py CLI"]
    wsReceive["WebSocket.receive_prices"]
    wsSubscribe["Redis.subscribe_price_update"]
    fastApi["FastAPI.initApp"]
    wsEndpoint["/ws endpoint"]
    reactDashboard["ReactDashboard.useWebSocket"]
    restApi["REST /api/orders,/api/pnl"]
  end

  %% Core Layer
  subgraph Core
    direction TB
    tradingBot["TradingBot"]
    strategyManager["StrategyManager"]
    riskManager["RiskManager"]
    orderExecutor["OrderExecutor"]
    simulatorExecutor["SimulatorExecutor"]
    strategySelector["StrategySelector"]
    optimizationModule["OptimizationModule"]
    trendScanner["TrendScanner"]
    performanceReporter["PerformanceReporter"]
    mlModule["MLModule"]
    strategyTester["StrategyTester"]
    newsHandler["NewsHandler"]
    anomalyDetector["AnomalyDetector"]
    dataCleaner["DataCleaner"]
    commentaryModule["CommentaryModule"]
    systemStatus["SystemStatus"]
  end

  %% Common Layer
  subgraph Common
    direction TB
    configLoader["config_loader.py"]
    dbSession["db/session.py"]
    dbModels["db/models.py"]
    logger["logger.py"]
    pluginLoader["plugin_loader.py"]
    metrics["metrics.py"]
    userPrefs["user_prefs.py"]
    healthCheck["health_check.py"]
    cache["cache.py"]
    additionalSetup["additional_setup.py"]
    notificationService["notification_service.py"]
    apiService["api_service.py"]
    eventLoop["event_loop.py"]
    sessionManager["session_manager.py"]
    loggingService["logging_service.py"]
    redisPub["Redis Pub/Sub"]
    rabbitMQ["RabbitMQ Queue"]
    postgreSQL["PostgreSQL"]
    paymentProcessor["PaymentProcessor"]
    reportRepo["ReportRepository"]
  end

  %% Initialization flow
  main --> configLoader
  configLoader --> dbSession
  dbSession --> dbModels
  dbModels --> logger
  logger --> pluginLoader
  pluginLoader --> metrics
  metrics --> userPrefs
  userPrefs --> healthCheck
  healthCheck --> cache
  cache --> additionalSetup
  additionalSetup --> notificationService
  notificationService --> apiService
  apiService --> eventLoop
  eventLoop --> sessionManager
  sessionManager --> loggingService

  %% RealTimeLoop flow
  wsReceive --> redisPub
  redisPub --> tradingBot
  tradingBot --> strategyManager
  strategyManager --> riskManager
  riskManager --> orderExecutor
  riskManager --> simulatorExecutor
  orderExecutor --> redisPub
  simulatorExecutor --> redisPub

  tradingBot --> loggingService
  tradingBot --> metrics
  strategyManager --> pluginLoader
  strategyManager --> configLoader
  riskManager --> postgreSQL
  orderExecutor --> paymentProcessor
  orderExecutor --> postgreSQL
  simulatorExecutor --> postgreSQL
  tradingBot --> notificationService

  %% Scheduler flow
  strategySelector --> strategyManager
  strategySelector --> optimizationModule
  optimizationModule --> strategyManager
  dataCleaner --> postgreSQL
  healthCheck --> notificationService
  healthCheck --> metrics
  trendScanner --> redisPub
  trendScanner --> postgreSQL
  performanceReporter --> postgreSQL
  performanceReporter --> reportRepo
  mlModule --> strategyManager
  strategySelector --> rabbitMQ

  %% Simulation flow
  backtestCLI --> strategyManager
  strategyManager --> simulatorExecutor
  simulatorExecutor --> postgreSQL
  simulatorExecutor --> strategyTester
  strategyTester --> strategyManager
  strategyManager --> commentaryModule
  strategyManager --> reportRepo

  %% Dashboard flow
  fastApi --> wsEndpoint
  wsEndpoint --> wsSubscribe
  wsSubscribe --> reactDashboard
  fastApi --> strategyManager
  fastApi --> loggingService
  fastApi --> restApi
  restApi --> orderExecutor
  restApi --> systemStatus
  systemStatus --> apiService
  systemStatus --> loggingService
  systemStatus --> metrics

---

## 4. Component Catalog

| ID | Module                   | Mode(s)      | 책임                               |
| -- | ------------------------ | ------------ | -------------------------------- |
| 1  | **MarketDataWebSocket**  | ALL          | 업비트·바이낸스 실시간 시세 수집               |
| 2  | **HistoricalDataLoader** | BACKTEST     | 과거 틱·캔들 → `market.tick` 재생       |
| 3  | **TradingBot**           | ALL          | 틱 처리·전략 호출·주문 파이프라인 오케스트레이션      |
| 4  | **StrategyManager**      | ALL          | 플러그인 전략 실행·주문 초안 반환              |
| 5  | **RiskManager**          | ALL          | 주문 검증(증거금·한도·중복)                 |
| 6  | **OrderExecutor**        | LIVE         | REST/WS API로 실계좌 주문·체결 수신        |
| 7  | **SimulatorExecutor**    | SIM/BACKTEST | 가상 체결·잔고 업데이트                    |
| 8  | **MetricsTracker**       | ALL          | 지표(P\&L, 레이턴시) Prometheus push   |
| 9  | **NotificationService**  | ALL          | Alertmanager 경보 → Slack/Telegram |
| 10 | **DashboardAPI**         | ALL          | FastAPI + WS, 포지션·실적 실시간 제공      |

---

## 5. Data Flow & Sequence (high-level)

1. **DataSource**
   LIVE → WebSocket, BACKTEST → HistoricalDataLoader
2. `market.tick` → Redis → **TradingBot**
3. Strategy → Risk → Executor (LIVE or SIM)
4. `order.fill` 이벤트 → TradingBot 잔고 갱신
5. MetricsTracker·Dashboard 출력 → Grafana 대시보드
6. Alert 임계치 초과 → Slack 알림

---

## 6. Non-Functional Requirements

| 항목            | 목표치                       | 비고                     |
| ------------- | ------------------------- | ---------------------- |
| **지연**        | 평균 ≤ 250 ms, P99 ≤ 600 ms | VPS 단일 호스트 왕복          |
| **RPO / RTO** | 5 분 / 30 분                | Postgres WAL·Redis AOF |
| **가용성**       | 99.5 % /월                 | 컨테이너 재시작 자동            |
| **보안**        | NAVER KMS 관리 키, 30 일 회전   | GitHub Actions OIDC    |

---

## 7. Deployment Topology

| 계층                | 컨테이너                                    | 비고                     |
| ----------------- | --------------------------------------- | ---------------------- |
| **App**           | `sigma-app` (모듈 run-via CLI arg)        | MODE=live/sim/backtest |
| **Data**          | `redis`, `postgres`, `rabbitmq`         | Named volume `db-data` |
| **Observability** | `prometheus`, `grafana`, `alertmanager` | dev · prod 공통          |
| **Dev-only**      | `sim_replay` (HD 전용), `sim_grafana`     | dev compose override   |

---

## 8. Glossary

| 용어       | 설명                           |
| -------- | ---------------------------- |
| **Tick** | 100 ms 단위 호가·체결 스냅샷          |
| **Fill** | 주문 체결 이벤트(계좌·수량·가격)          |
| **MODE** | live / sim / backtest 환경 스위치 |

---

## 9. Version History

| 버전       | 날짜         | 주요 변경                                                   |
| -------- | ---------- | ------------------------------------------------------- |
| v1.0     | 2025-05-21 | Baseline (거래 5 모듈)                                      |
| v1.1     | 2025-05-22 | Metrics·Notification·Dashboard 추가                       |
| **v1.2** | 2025-05-22 | SimulatorExecutor · HistoricalDataLoader 통합, 다이어그램/표 갱신 |

---
