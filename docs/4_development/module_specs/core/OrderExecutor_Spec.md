# SIGMA 모듈 사양서

이 문서는 SIGMA 프로젝트의 각 모듈을 명확히 기록하기 위한 문서입니다. 모든 항목은 누락 없이 작성하며, 해당 사항이 없을 경우 **해당 없음**으로 표기합니다.

## 1. 모듈 개요
* 모듈명: OrderExecutor
* 작성자: Codex
* 작성일: 2025-05-22
* 최종 검토자: Codex
* 최종 수정일: 2025-05-22

실계좌 주문을 거래소 REST/WS API로 전송하고 체결 결과를 수신한다. 체결 정보는 Redis `order.fill` 채널로 퍼블리시하며 Postgres에 기록한다.

## 2. 구조 개요
* 포함된 클래스/함수: `OrderExecutor`, `send_order`, `handle_fill`
* 주요 메서드: `execute()`, `listen_fills()`
* 외부 API 제공 여부: 없음
* 소스 파일 위치: `sigma/core/order_executor.py`

## 3. 인터페이스 명세
### 3.1 입력
* 입력 유형: 검증된 주문 dict
* 형식 및 구조: `{symbol, side, size, price}`
* 제약 조건: API 제한 준수, 서명 필요
* 예시: `{"symbol":"BTC/KRW","side":"buy","size":0.01,"price":101}`

### 3.2 출력
* 출력 유형: 체결 이벤트
* 형식 및 구조: `{order_id, filled_size, price, ts}`
* 예시: `{"order_id":"123","filled_size":0.01,"price":101,"ts":1620000001}`
* 반환 조건: 체결 시점마다 Redis 퍼블리시

### 3.3 API 엔드포인트(해당 시)
* 해당 없음

## 4. 내부 처리 로직
* 처리 흐름 요약: 주문 서명 → REST/WS 전송 → 체결 대기 → 결과 저장 및 퍼블리시
* 순서도/플로우차트: RealTimeLoop의 Execution 단계 참조
* 알고리즘 요약: 비동기 HTTP 요청, 체결 대기용 웹소켓 유지

## 5. 예외 처리
* 주요 예외 유형: API 실패, 네트워크 오류
* 발생 조건: HTTP 4xx/5xx, 연결 끊김
* 대응 방식: 재시도, 실패 시 주문 취소 알림
* 로깅/알림: 상세 로그 기록, NotificationService 호출

## 6. 연관 모듈 및 외부 시스템
* 상위 호출자: RiskManager
* 하위 호출 대상: 외부 거래소 API, Redis
* 연계되는 DB/캐시/메시지큐: Postgres, Redis
* 타 모듈 간 의존 관계: metrics.py와 체결 통계 공유

## 7. 리소스 및 성능
### 7.1 리소스 소비
* CPU 예상 사용량: 0.5 vCPU 이하
* 메모리 예상 사용량: 250MB 이하
* 병렬성 또는 멀티스레딩 여부: asyncio 사용

### 7.2 성능 기준
* 처리량 기준: 초당 수백 건 주문 전송 가능
* 응답 시간: 평균 150ms 이하
* 지연 허용 한계: 500ms
* 초기화 시간: 2초 이하

## 8. 설정 및 의존성
* 사용하는 DB 테이블 및 필드: `order_history`
* 설정값 및 기본값: API 키, 시크릿, 타임아웃
* 외부 환경 변수: `EXCHANGE_KEY`, `EXCHANGE_SECRET`
* 사용하는 서드파티/외부 API: 업비트, 바이낸스 REST/WS

## 9. 테스트 및 검증
* 단위 테스트 항목: 주문 서명, API 요청 포맷
* 예외 테스트 항목: 네트워크 실패, 체결 지연
* 통합 테스트 체크리스트: RiskManager → OrderExecutor → fill 퍼블리시 흐름
* 테스트 커버리지 목표: 80% 이상

## 10. 제약사항 및 향후 계획
* 현재 한계: 단일 거래소 API에 종속
* 기술적 부채: 로깅과 모니터링 코드 중복
* 향후 개선/확장 예정 사항: 거래소 다중 지원, 주문 속도 최적화
* 폐지 예정 요소: 없음
