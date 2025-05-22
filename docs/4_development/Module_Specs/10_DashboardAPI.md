# DashboardAPI 모듈 사양

## 1. 모듈 개요
* 모듈명: DashboardAPI
* 작성자: SIGMA 팀
* 작성일: 2025-05-22
* 최종 검토자: SIGMA 팀
* 최종 수정일: 2025-05-22

FastAPI 기반의 실시간 대시보드 및 WebSocket 서버를 제공한다. 포지션, PnL, 시스템 상태를 외부에서 조회할 수 있다.

## 2. 구조 개요
* 포함된 클래스/함수:
  - FastAPI `app`
  - REST 엔드포인트(`/positions`, `/pnl` 등)
  - WebSocket 엔드포인트(`/ws`)
* 주요 메서드:
  - `init_api(port)`: 서버 실행
* 외부 API 제공 여부: REST & WebSocket
* 소스 파일 위치: `sigma/web/dashboard.py`

## 3. 인터페이스 명세
### 3.1 입력
* 입력 유형: HTTP/WS 요청
* 형식 및 구조: JSON 또는 텍스트
* 제약 조건: 일부 엔드포인트는 인증 필요
* 예시: `GET /positions`

### 3.2 출력
* 출력 유형: JSON 응답 또는 실시간 메시지
* 형식 및 구조: `[{"symbol":"BTC","qty":0.1}]`
* 예시: `[{"symbol":"BTC","qty":0.1}]`
* 반환 조건: 요청 처리 후

### 3.3 API 엔드포인트
* URL: `/positions`, `/pnl`, `/ws`
* Method: GET/POST/WS
* 인증: API_TOKEN 헤더
* 설명: 대시보드 데이터 제공
* 요청/응답 예시: `{"pnl":1000}`

## 4. 내부 처리 로직
* 처리 흐름 요약:
  1. FastAPI 앱을 생성하고 엔드포인트를 등록한다.
  2. WebSocket 연결 시 Redis `market.tick`을 구독해 실시간 데이터를 전송한다.
* 순서도/플로우차트: 해당 없음
* 알고리즘 요약: FastAPI 표준 라우팅 + Redis Pub/Sub

## 5. 예외 처리
* 주요 예외 유형: 인증 실패, 연결 오류
* 발생 조건: 잘못된 토큰, 네트워크 장애
* 대응 방식: HTTPException 반환
* 로깅/알림: 오류 로그 후 필요 시 `NotificationService` 호출

## 6. 연관 모듈 및 외부 시스템
* 상위 호출자: 운영 대시보드
* 하위 호출 대상: Redis, DB
* 연계되는 DB/캐시/메시지큐: PostgreSQL, Redis
* 타 모듈 간 의존 관계: MetricsTracker

## 7. 리소스 및 성능
### 7.1 리소스 소비
* CPU 예상 사용량: 낮음(HTTP 처리)
* 메모리 예상 사용량: 낮음
* 병렬성 또는 멀티스레딩 여부: uvicorn/asyncio

### 7.2 성능 기준
* 처리량 기준: 초당 수십~수백 요청
* 응답 시간: 100ms 이내 목표
* 지연 허용 한계: 500ms
* 초기화 시간: 수 초

## 8. 설정 및 의존성
* 사용하는 DB 테이블 및 필드: orders, positions 등
* 설정값 및 기본값: `API_TOKEN`, `PORT`
* 외부 환경 변수: 동일
* 사용하는 서드파티/외부 API: `fastapi`, `uvicorn`, `redis`

## 9. 테스트 및 검증
* 단위 테스트 항목: 각 엔드포인트 동작, 인증 체크
* 예외 테스트 항목: 토큰 미제공, WebSocket 오류
* 통합 테스트 체크리스트: 전체 시스템과 연동된 대시보드 사용
* 테스트 커버리지 목표: 90%

## 10. 제약사항 및 향후 계획
* 현재 한계: 기본 조회 기능 위주, 고급 UI 미구현
* 기술적 부채: 인증 로직 단순화
* 향후 개선/확장 예정 사항: 실시간 차트, 사용자별 권한 관리
* 폐지 예정 요소: 해당 없음
