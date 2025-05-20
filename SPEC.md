# SIGMA 시스템 모듈 사양서

본 문서는 SIGMA 자동매매 시스템 개선을 위해 도입되는 모듈 구조와 설정 방식을 정의합니다.

## 데이터베이스 모듈 (`sigma/db/database.py`)
- `python-dotenv`를 사용해 `.env` 파일을 로드합니다.
- 환경 변수 `DATABASE_URL`을 읽어 데이터베이스에 연결합니다.
- `get_db()` 함수는 세션을 생성하여 사용 후 종료하도록 제너레이터 형태로 제공합니다.

## 핵심 로직 (`sigma/core`)
- `bot.py`: 트레이딩 봇의 실행 흐름을 담당합니다.
- `strategies.py`: 기본 전략 클래스와 예시 전략을 포함합니다.
- `execution.py`: 주문 실행 로직을 담당하는 `OrderExecutor` 클래스를 제공합니다.

## 웹 인터페이스 (`sigma/web`)
- `dashboard.py`: FastAPI 기반 대시보드를 제공합니다.

## 유틸리티 (`sigma/utils`)
- `logger.py`: `loguru` 라이브러리를 사용한 로깅 기능을 제공합니다.

## 동작 방식 요약
1. 애플리케이션 시작 시 `.env` 파일을 통해 환경 변수를 불러옵니다.
2. 데이터베이스 모듈에서 `DATABASE_URL`을 사용해 세션을 생성합니다.
3. `TradingBot`은 전략에서 받은 신호를 `OrderExecutor`를 통해 처리합니다.
4. 모든 모듈에서 `logger`를 사용하여 로그를 남깁니다.
