# 모듈 사양서 디렉터리 구조

SIGMA 아키텍처의 레이어별로 모듈 사양서를 구분했습니다.

- `interfaces/` : 외부와 직접 상호작용하는 CLI, WebSocket, REST API 등
- `core/` : 거래 로직과 전략 관리 등 핵심 모듈
- `common/` : 설정, 로깅 등 공통 유틸리티
- `infrastructure/` : 데이터베이스, 메시지 브로커 같은 인프라 모듈
- `legacy/` : 현재 아키텍처에서 제외되었지만 참고용으로 유지되는 모듈

각 파일은 `Module_Spec_Template.md` 형식을 따릅니다.

### 최근 업데이트 (2025-05-26)

다음 모듈들이 구현되어 사양서와 코드가 동기화되었습니다.

- `Logger`
- `MetricsTracker`
- `NotificationService`
- `ApiService`
- `Cache`
- `SessionManager`
- `RedisPubSub`
- `RabbitMQQueue`
- `PaymentProcessor`
- `MLModule`
- `PluginLoader`
- `PerformanceReporter`
- `CommentaryModule`
- `NewsHandler`
- `HistoricalLoader`
- `FastAPI_InitApp`
- `RunBot_Main`
- `Redis_SubscribePriceUpdate`
- `WebSocket_Endpoint`
- `AdditionalSetup`
- `ConfigLoader`
- `EventLoop`
- `SystemStatus`
- `DashboardAPI`
- `HealthCheck`
- `UserPrefs`
- `DataCleaner`
- `Backtest_CLI`
- `StrategyTester`
- `DBModels`
- `DBSession`
- `PostgreSQL`
- `LoggingService`
- `ReportRepository`
- `AnomalyDetector`
- `MarketDataWebSocket`
- `StrategyManager`
- `OrderExecutor`
- `TrendScanner`

[DEPRECATED] `logger.py`는 더 이상 사용하지 않으며 `logging_service.py`로 대체되었습니다.
