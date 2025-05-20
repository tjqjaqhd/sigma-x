# Sigma 모듈 사양서

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

자세한 규격은 추후 개발 진행에 맞추어 확장합니다.
