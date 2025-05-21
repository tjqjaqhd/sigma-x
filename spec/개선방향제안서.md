## Sigma-X 시스템 개선 방안 문서

### 1. 환경설정 구조 개선

* `.env` 기반 설정 제거
* DB 테이블 `system_config` 도입: key-value 구조
* `config_loader`는 DB로부터만 설정 수신
* 초기 접속용 DB URL만 `.env`로 유지
* Slack, 전략, 사용자 선호 등 모든 설정 항목 DB화

### 2. 초기화 단계 완성

* `initialize()` 내에 `init_db()` 추가해 ORM 테이블 자동 생성
* FastAPI 서버 실행 코드 삽입 (`uvicorn.run` 또는 백그라운드 스레드)
* SlackNotifier, Redis, DB 상태 검사 포함한 `health_check` 구현
* Prometheus 지표 수집기 등록 및 `/metrics` 엔드포인트 노출

### 3. 실시간 트레이딩 구조 전환

* WebSocket 또는 REST 기반 시세 수집기 구현
* Redis Pub/Sub 구조 도입: 시세 broadcast 구조화
* TradingBot은 Redis 구독자로 전환
* 신호 발생 시 RabbitMQ로 주문 전송 -> OrderWorker에서 실행
* OrderExecutor는 실체 API 또는 모의체결 분리 전략 적용

### 4. 전략 적응 구조 도입

* `RegimeDetector`: 시장 국면 탐지 로직 구현
* `ParamAdjuster`: 전략 파라미터 DB에 동적 반영
* `QualityAssessment`: 전략 성과 평가, 기준 미달시 경고
* `FeedbackMechanism`: 장기 학습용 로그 및 전략 비교 저장

### 5. 스케줄러 확장

* APScheduler로 전환하여 다양한 주기 작업 등록

  * 일일 전략 선택 및 튜닝
  * 주간 성과 보고서 생성
  * 로그 회전 및 오래된 데이터 삭제
  * 사용자 활성도 및 설정 갱신

### 6. 데이터 및 상태 저장 구조 정비

* `market_data`, `orders`, `positions`, `strategy_param`, `alerts` 테이블 설계
* 모든 이벤트 결과는 DB에 저장 (체결, 신호, 오류 등)
* 시계열 데이터는 TimescaleDB 등 확장 고려

### 7. API 서버 기능 확대

* FastAPI에 REST + WebSocket 엔드포인트 다수 추가

  * 전략 제어 (`/bot/start`, `/bot/stop`, `/strategy/update` 등)
  * 실시간 시세 조회, 과거 성과 조회
  * 알림 기록, 사용자 설정 관리
* 인증(JWT/OAuth2) 적용

### 8. NotificationService 통합

* SlackNotifier 등 알림 채널은 NotificationService 아래 통합
* `notify(level, message)` 방식 인터페이스 제공
* 설정값에 따라 Slack/Email 등 분기
* 시스템 전역에서 NotificationService 호출 방식 일원화

### 9. 로깅 및 모니터링

* `RotatingFileHandler`로 로그 회전 구현
* 메트릭 지표 수집 및 Prometheus 연동
* 헬스체크 주기화: 30초 단위, Slack 알림 연동
* 주요 이벤트 로깅 시 DB 기록 병행

### 10. 테스트 및 예외 처리 강화

* try-except 구조 보강: 모든 외부 연동, 전략 실행, 주문 처리
* 실패 시 rollback, 알림 전송, 리트라이 구조 도입
* 단위 테스트 모듈 생성: config, bot, executor, API 등
* 커버리지 측정 도구 도입 (pytest-cov 등)
