# SIGMA 모듈 사양서

이 문서는 SIGMA 프로젝트의 각 모듈을 명확히 기록하기 위한 문서입니다. 모든 항목은 누락 없이 작성하며, 해당 사항이 없을 경우 **해당 없음**으로 표기합니다.

## 1. 모듈 개요
* 모듈명: WebSocket_Endpoint
* 작성자: TBD
* 작성일: 2025-05-23
* 최종 검토자: TBD
* 최종 수정일: 2025-05-23

FastAPI에서 `/ws` 경로로 노출되는 실시간 스트림 엔드포인트를 담당한다. 클라이언
트와의 WebSocket 세션을 유지하며 Redis Pub/Sub으로부터 받은 가격 정보와 시스템
알림을 브라우저로 전달한다.

## 2. 구조 개요
* 포함된 클래스/함수: `WebSocketEndpoint`, `broadcast_message`
* 주요 메서드: `on_connect`, `on_receive`, `on_disconnect`
* 외부 API 제공 여부: WebSocket
* 소스 파일 위치: `sigma/interfaces/ws_endpoint.py`

## 3. 인터페이스 명세
### 3.1 입력
* 입력 유형: WebSocket 메시지
* 형식 및 구조: JSON `{type, payload}`
* 제약 조건: 인증 토큰이 헤더에 포함되어야 함

### 3.2 출력
* 출력 유형: 실시간 JSON 메시지
* 형식 및 구조: `{event, data}`
* 반환 조건: 연결이 유지되는 동안 지속 전송

## 4. 내부 처리 로직
1. 클라이언트 연결 시 세션 등록 및 인증
2. Redis `price_update` 채널 구독
3. 수신된 메시지를 클라이언트에 전달
4. 연결 종료 시 세션 정리

## 5. 예외 처리
* 인증 실패 → 연결 거부
* Redis 오류 → 재시도 후 실패 시 연결 종료

## 6. 연관 모듈 및 외부 시스템
* 상위 호출자: FastAPI_InitApp에서 라우터로 등록
* 하위 호출 대상: RedisPubSub
* 연계되는 DB/캐시/메시지큐: Redis
* 타 모듈 간 의존 관계: metrics.py, logging_service

## 7. 리소스 및 성능
### 7.1 리소스 소비
* CPU 예상 사용량: 세션 수에 비례
* 메모리 예상 사용량: 클라이언트당 1MB 내외

### 7.2 성능 기준
* 지연 허용: 200ms 이하 실시간 전송
* 동시 접속자: 100명 기준 테스트

## 8. 설정 및 의존성
* 환경 변수: `WS_TOKEN_SECRET`
* 의존성: `fastapi`, `redis-py`

## 9. 테스트 및 검증
* 단위 테스트 항목: 메시지 브로드캐스트 로직
* 통합 테스트 체크리스트: 실제 WebSocket 클라이언트 연결
* 테스트 커버리지 목표: 80% 이상

## 10. 제약사항 및 향후 계획
* 향후 계획: 다중 서버 환경에서 Redis Stream 사용 검토
