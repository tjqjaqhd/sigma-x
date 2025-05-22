# system.api_service 모듈 사양

## 1. 모듈 개요

* 모듈명: system.api_service
* 작성자: AI 자동화
* 작성일: 2024-06-XX
* 최종 검토자: AI 자동화
* 최종 수정일: 2024-06-XX

**설명:**
FastAPI 기반 REST API 및 Prometheus 메트릭 엔드포인트를 제공하는 모듈. 봇 제어, 성과/포지션 조회, 인증, 메트릭 수집 등 운영 대시보드와 외부 연동을 담당한다.

## 2. 구조 개요

* 포함된 객체/함수:
  - app: FastAPI 인스턴스
  - init_api: API 서버 초기화(백그라운드 실행)
  - 각 엔드포인트(metrics, bot/start, bot/stop, performance, positions)
* 주요 함수/메서드 목록:
  - init_api(): uvicorn.run으로 FastAPI 서버 실행
  - metrics(): Prometheus 메트릭 반환
  - bot_start()/bot_stop(): 봇 제어
  - performance(): PnL 등 성과 반환
  - positions(): 포지션 리스트 반환
* 외부 API 제공 여부: REST API, Prometheus

## 3. 인터페이스 명세

### 3.1. 입력 (Input)
* 입력 유형: HTTP 요청, 인증 토큰
* 형식 및 구조: HTTP 헤더, POST/GET
* 제약 조건: 인증 필요(일부 엔드포인트)
* 예시: Authorization: Bearer <token>

### 3.2. 출력 (Output)
* 출력 유형: JSON, Prometheus 텍스트
* 형식 및 구조: {"status": "started"}, {"pnl": 0}, [] 등
* 예시: {"status": "started"}, {"pnl": 0}, []
* 반환 조건: 요청 성공/실패 시

### 3.3. API 엔드포인트
* URL:
  - /metrics (GET): Prometheus 메트릭
  - /bot/start (POST): 봇 시작
  - /bot/stop (POST): 봇 중지
  - /performance (GET): 성과 조회
  - /positions (GET): 포지션 조회
* Method: GET, POST
* 인증: API_TOKEN 필요(일부 엔드포인트)
* 설명: 운영 대시보드 및 외부 연동용 API
* 요청/응답 예시: {"status": "started"}, {"pnl": 0}, []

## 4. 내부 처리 로직
* 처리 흐름 요약:
  1. app 인스턴스 생성, 엔드포인트 등록
  2. 인증 헤더 검사(auth_header)
  3. 각 엔드포인트에서 요청 처리 및 응답 반환
  4. init_api에서 uvicorn.run으로 서버 백그라운드 실행
* 순서도/플로우차트: 해당 없음
* 알고리즘 요약: FastAPI 표준 라우팅 및 인증

## 5. 예외 처리
* 주요 예외 유형: HTTPException(401)
* 발생 조건: 인증 실패, 잘못된 요청 등
* 대응 방식: HTTP 401 반환
* 로깅/알림: logger.info로 서버 초기화 로그 기록

## 6. 연관 모듈 및 외부 시스템
* 상위 호출자: system 초기화 등
* 하위 호출 대상: uvicorn, fastapi, prometheus_client, utils/logger
* 연계되는 DB/캐시/메시지큐: 해당 없음
* 타 모듈 간 의존 관계: fastapi, prometheus_client, utils/logger

## 7. 리소스 및 성능
### 7.1. 리소스 소비
* CPU 예상 사용량: 낮음(HTTP 서버)
* 메모리 예상 사용량: 낮음
* 병렬성 또는 멀티스레딩 여부: uvicorn/Thread 기반
### 7.2. 성능 기준
* 처리량 기준 (TPS/건수): 요청 빈도에 따라 다름
* 응답 시간: 매우 짧음
* 지연 허용 한계: 해당 없음
* 초기화 시간: 매우 짧음

## 8. 설정 및 의존성
* 사용하는 DB 테이블 및 필드: 해당 없음
* 설정값 및 기본값: API_TOKEN, PORT(환경변수)
* 외부 환경 변수: API_TOKEN, PORT, RUN_SERVER
* 사용하는 서드파티/외부 API: fastapi, uvicorn, prometheus_client

## 9. 테스트 및 검증
* 단위 테스트 항목: 각 엔드포인트 정상 동작, 인증 실패
* 예외 테스트 항목: 인증 실패, 잘못된 요청 등
* 통합 테스트 체크리스트: 전체 시스템 초기화와 연동, 대시보드 연동
* 테스트 커버리지 목표: 90% 이상

## 10. 제약사항 및 향후 계획
* 현재 한계: 단순 라우팅, 실제 봇/포지션 연동 미흡
* 기술적 부채: 인증/로깅/상태 관리 단순
* 향후 개선/확장 예정 사항: 실시간 데이터 연동, 엔드포인트 확장, 인증 강화
* 폐지 예정 요소: 해당 없음

| 객체/함수 | 설명 |
|-----------|------|
| `app` | FastAPI 인스턴스 |
| `init_api()` | FastAPI 서버 백그라운드 실행 |
| `/metrics` | Prometheus 메트릭 엔드포인트 |
| `/bot/start` | 봇 시작 API |
| `/bot/stop` | 봇 중지 API |
| `/performance` | 성과 조회 API |
| `/positions` | 포지션 조회 API | 