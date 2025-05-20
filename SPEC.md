# SIGMA 시스템 모듈 사양서

본 문서는 SIGMA 자동매매 시스템 개선을 위해 도입되는 모듈 구조와 설정 방식을 정의합니다.

## 환경 설정 예시
- `.env.example` 파일을 참고하여 실제 `.env` 파일을 작성합니다.

## 데이터베이스 모듈 (`sigma/db/database.py`)
- `python-dotenv`를 사용해 `.env` 파일을 로드합니다.
- 환경 변수 `DATABASE_URL`을 읽어 데이터베이스에 연결합니다.
- `get_db()` 함수는 세션을 생성하여 사용 후 종료하도록 제너레이터 형태로 제공합니다.
- `init_db.py` 스크립트로 테이블을 초기 생성할 수 있습니다.

## 핵심 로직 (`sigma/core`)
- `bot.py`: 트레이딩 봇의 실행 흐름을 담당합니다.
- `strategies.py`: 기본 전략 클래스와 예시 전략을 포함합니다.
- `execution.py`: 주문 실행 로직을 담당하는 `OrderExecutor` 클래스를 제공합니다.

## 웹 인터페이스 (`sigma/web`)
- `dashboard.py`: FastAPI 기반 대시보드를 제공합니다.

## 유틸리티 (`sigma/utils`)
- `logger.py`: `loguru` 라이브러리를 사용한 로깅 기능을 제공합니다.

## 스케줄러 (`sigma/core/scheduler.py`)
- APScheduler를 사용해 트레이딩 봇 실행 작업을 주기적으로 등록합니다.
- `start_bot_scheduler()` 함수는 봇 인스턴스와 실행 간격을 받아 스케줄러를 구동합니다.

## 슬랙 알림 모듈 (`sigma/utils/slack_notifier.py`)
- `slack_sdk` 기반으로 슬랙 채널에 메시지를 전송하는 기능을 제공합니다.
- 환경 변수 `SLACK_TOKEN`과 `SLACK_CHANNEL`을 사용해 인증 정보를 로드합니다.

## 데이터 수집 모듈 (`sigma/data/collector.py`)
- 외부 API에서 시세 데이터를 가져오는 역할을 합니다.
- 초기 구현에서는 더미 데이터를 반환하며, `fetch_market_data()` 메서드를 제공합니다.

## 데이터 모델 (`sigma/data/models.py`)
- SQLAlchemy ORM을 사용하여 `MarketData` 테이블 구조를 정의합니다.
- 가격과 타임스탬프 정보를 저장하는 기본 예시 모델을 포함합니다.

## 동작 방식 요약
1. 애플리케이션 시작 시 `.env` 파일을 통해 환경 변수를 불러옵니다.
2. 데이터베이스 모듈에서 `DATABASE_URL`을 사용해 세션을 생성합니다.
3. `TradingBot`은 전략에서 받은 신호를 `OrderExecutor`를 통해 처리합니다.
4. 모든 모듈에서 `logger`를 사용
5. `start_bot_scheduler()`로 봇을 주기 실행하고, 필요 시 `SlackNotifier`로 알림을 전송합니다
## 설정 파일
- `.env.example`: 데이터베이스와 슬랙 인증 정보를 예시로 제공하는 환경 변수 파일입니다.
- `.pre-commit-config.yaml`: 커밋 시 `black`, `flake8`, `pytest`를 자동 실행하도록 설정합니다.
- `.github/workflows/ci.yml`: GitHub Actions에서 린트와 테스트를 수행하는 CI 구성을 정의합니다.