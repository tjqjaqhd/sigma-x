# SIGMA 아키텍처 v1.2

본 문서는 SIGMA 자동매매 시스템의 v1.2 설계를 설명합니다. 개인 VPS 한 대에서 LIVE, SIM, BACKTEST 세 모드를 동일 경로로 처리하는 것이 목표입니다.

```mermaid
flowchart LR
    subgraph DataSource
        WS[Real-time WebSocket]
        HD[HistoricalDataLoader]
    end
    WS -- tick --> R( Redis `market.tick` )
    HD -- replay tick --> R
    R --> TB[TradingBot]
    TB --> SM(StrategyManager)
    SM --> RM(RiskManager)
    RM -- approved --> EX{MODE?}
    EX -- LIVE --> OE[OrderExecutor]
    EX -- SIM/BACKTEST --> SE[SimulatorExecutor]

    OE -- fill --> R_Fill[Redis `order.fill`]
    SE -- sim fill --> R_Fill

    TB -. metrics .-> MT(MetricsTracker)
    MT --> Prom(Prometheus) --> Graf[Grafana]
    Prom -. alert .-> AM(Alertmanager) -.> NS(NotificationService)

    TB --> API[DashboardAPI]
```

## 구성 모듈

| ID | 모듈 | 모드 | 책임 |
| -- | ---- | ---- | --- |
| 1 | MarketDataWebSocket | ALL | 실시간 시세 수집 |
| 2 | HistoricalDataLoader | BACKTEST | 과거 틱 재생 |
| 3 | TradingBot | ALL | 전략 호출 및 주문 파이프라인 |
| 4 | StrategyManager | ALL | 전략 실행 및 주문 초안 반환 |
| 5 | RiskManager | ALL | 주문 검증 |
| 6 | OrderExecutor | LIVE | 실계좌 주문 처리 |
| 7 | SimulatorExecutor | SIM/BACKTEST | 가상 체결 및 잔고 갱신 |
| 8 | MetricsTracker | ALL | 지표 수집 및 Push |
| 9 | NotificationService | ALL | 경보 전달 |
| 10 | DashboardAPI | ALL | 실시간 대시보드 제공 |

## 비기능 요구사항 요약

| 항목 | 목표치 | 비고 |
| --- | --- | --- |
| 지연 | 평균 ≤ 250ms, P99 ≤ 600ms | VPS 단일 호스트 기준 |
| RPO/RTO | 5분 / 30분 | Postgres WAL, Redis AOF |
| 가용성 | 99.5%/월 | 컨테이너 자동 재시작 |
| 보안 | NAVER KMS, 30일 키 회전 | GitHub Actions OIDC |

세부 구현 및 설정은 각 모듈 사양서를 참고하시기 바랍니다.
