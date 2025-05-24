# SIGMA 모듈 사양서

이 문서는 SIGMA 프로젝트의 각 모듈을 명확히 기록하기 위한 문서입니다. 모든 항목은 누락 없이 작성하며, 해당 사항이 없을 경우 **해당 없음**으로 표기합니다.

## 1. 모듈 개요
* 모듈명: DashboardAPI
* 작성자: Codex
* 작성일: 2025-05-22
* 최종 검토자: TBD
* 최종 수정일: 2025-05-22

FastAPI 기반의 REST 및 WebSocket 서버로 포지션, 실적, 시스템 상태를 실시간으로 제공한다. React 대시보드에서 구독하여 시각화한다.

## 2. 구조 개요
* 포함된 클래스/함수: `create_app`, `ws_endpoint`, `rest_endpoints`
* 주요 메서드: `get_positions()`, `get_pnl()`, `ws_handler()`
* 외부 API 제공 여부: REST/WS
* 소스 파일 위치: `sigma/dashboard_api.py`

## 3. 인터페이스 명세
### 3.1 입력
* 입력 유형: HTTP 요청, WebSocket 메시지
* 형식 및 구조: JSON 또는 URL 파라미터
* 제약 조건: 인증 토큰 필요
* 예시: `GET /api/pnl?symbol=BTC`

### 3.2 출력
* 출력 유형: JSON 응답 또는 WebSocket 스트림
* 형식 및 구조: `{pnl: 1000}` 등
* 예시: `{"pnl":1000}`
* 반환 조건: 요청 성공 시 200 OK

### 3.3 API 엔드포인트(해당 시)
* URL: `/api/*`, `/ws`
* Method: GET/POST, WebSocket
* 인증: Bearer Token
* 설명: 포지션·실적 조회 및 실시간 스트림 제공
* 요청/응답 예시: `curl -H "Authorization: Bearer TOKEN" /api/positions`

## 4. 내부 처리 로직
* 처리 흐름 요약: 요청 수신 → 인증 → 데이터 조회 → 응답 반환
* 순서도/플로우차트: Dashboard flow 참조
* 알고리즘 요약: FastAPI 라우터, Redis 구독을 통한 실시간 업데이트

## 5. 예외 처리
* 주요 예외 유형: 인증 실패, 데이터 조회 오류
* 발생 조건: 잘못된 토큰, Redis 연결 끊김
* 대응 방식: 401/500 오류 반환 및 로그
* 로깅/알림: `logging_service.py` 사용 (`logger.py`는 deprecated), 심각 오류 시 NotificationService 호출

## 6. 연관 모듈 및 외부 시스템
* 상위 호출자: 사용자의 웹 브라우저
* 하위 호출 대상: Redis, Postgres
* 연계되는 DB/캐시/메시지큐: Redis, Postgres
* 타 모듈 간 의존 관계: metrics.py와 데이터 공유

## 7. 리소스 및 성능
### 7.1 리소스 소비
* CPU 예상 사용량: 0.5 vCPU 이하
* 메모리 예상 사용량: 300MB 이하
* 병렬성 또는 멀티스레딩 여부: uvicorn 멀티스레드 가능

### 7.2 성능 기준
* 처리량 기준: 초당 수십 요청 처리
* 응답 시간: 평균 100ms 이하
* 지연 허용 한계: WebSocket 1초 이내 업데이트
* 초기화 시간: 2초 이하

## 8. 설정 및 의존성
* 사용하는 DB 테이블 및 필드: `positions`, `pnl_history`
* 설정값 및 기본값: API 토큰, Redis URL
* 외부 환경 변수: `API_TOKEN`, `REDIS_URL`, `POSTGRES_DSN`
* 사용하는 서드파티/외부 API: FastAPI, Uvicorn

## 9. 테스트 및 검증
* 단위 테스트 항목: 각 엔드포인트 응답, 인증 로직
* 예외 테스트 항목: 잘못된 요청, 권한 없음
* 통합 테스트 체크리스트: TradingBot 및 metrics.py와 데이터 연동
* 테스트 커버리지 목표: 80% 이상

## 10. 제약사항 및 향후 계획
* 현재 한계: 단일 서버에서만 서비스
* 기술적 부채: 인증 로직 단순화
* 향후 개선/확장 예정 사항: 사용자 권한 레벨, 대시보드 기능 추가
* 폐지 예정 요소: 없음
