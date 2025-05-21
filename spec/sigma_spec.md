# Sigma 모듈 사양서
이 문서는 `sigma` 하위 모듈을 간단하게 설명하는 목차입니다. 각 파일에 대한 상세 내용은 동일한 이름의 문서에서 찾을 수 있습니다.

| 모듈 경로 | 관련 문서 |
|-----------|-----------|
| `sigma/core/bot.py` | [core_bot.md](core_bot.md) |
| `sigma/core/strategies.py` | [core_strategies.md](core_strategies.md) |
| `sigma/core/execution.py` | [core_execution.md](core_execution.md) |
| `sigma/core/scheduler.py` | [core_scheduler.md](core_scheduler.md) |
| `sigma/data/collector.py` | [data_collector.md](data_collector.md) |
| `sigma/data/models.py` | [data_models.md](data_models.md) |
| `sigma/db/database.py` | [db_database.md](db_database.md) |
| `sigma/utils/logger.py` | [utils_logger.md](utils_logger.md) |
| `sigma/web/dashboard.py` | [web_dashboard.md](web_dashboard.md) |
| `sigma/system/plugin_loader.py` | [plugin_loader.md] (plugin_loader.md)ㅣ
| `sigma/system/metrics.py` | [metrics.md] (metrics.md) |
| `sigma/system/user_prefs.py` | [user_prefs.md](user_prefs.md) |
| `sigma/system/health_check.py` | [health_check.md](health_check.md) |
| `sigma/system/cache.py` | [cache.md](cache.md) |
| `sigma/system/additional_setup.py` | [additional_setup.md](additional_setup.md) |
| `sigma/system/notification_service.py` | [notification_service.md](notification_service.md) |
| `sigma/system/api_service.py` | [api_service.md](api_service.md) |
| `sigma/system/event_loop.py` | [event_loop.md](event_loop.md) |
| `sigma/system/session_manager.py` | [session_manager.md](session_manager.md) |
| `sigma/system/logging_service.py` | [로깅_서비스
이 문서는 `sigma` 패키지 내부 모듈과 기능을 간략히 정리한 초안입니다. 코드 변경 시 이곳의 내용도 함께 업데이트해야 합니다.

| 모듈 경로 | 주요 클래스/함수 | 설명 |
|-----------|----------------|-----|
| `sigma/core/bot.py` | `TradingBot` | 전략 신호를 받아 주문을 실행하는 기본 봇 클래스 |
| `sigma/core/strategies.py` | `BaseStrategy`, `DummyStrategy` | 전략 인터페이스와 샘플 전략 구현 |
| `sigma/core/execution.py` | `OrderExecutor` | 실제 또는 모의 주문을 실행하는 모듈 |
| `sigma/core/scheduler.py` | `start_bot_scheduler` | 봇을 주기적으로 실행하기 위한 스케줄러 |
| `sigma/data/collector.py` | `DataCollector` | 외부 시장 데이터를 수집하는 클래스 |
| `sigma/data/models.py` | `MarketData` | 시장 데이터 저장을 위한 SQLAlchemy 모델 |
| `sigma/db/database.py` | `get_db` 등 | 데이터베이스 세션과 엔진 설정 |
| `sigma/utils/logger.py` | `logger` | 프로젝트 전역 로거 설정 |
| `sigma/web/dashboard.py` | FastAPI `app` | 간단한 웹 대시보드 엔드포인트 |

정밀한 기술은 추후 개발을 진행하기 위해 확장됩니다. 
