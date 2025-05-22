# data.collector 모듈 사양

## 1. 모듈 개요

* 모듈명: data.collector
* 작성자: AI 자동화
* 작성일: 2024-06-XX
* 최종 검토자: AI 자동화
* 최종 수정일: 2024-06-XX

**설명:**
WebSocket 클라이언트로 외부 실시간 데이터를 수집하고, Redis Pub/Sub을 통해 시스템 전체에 실시간 배포하는 데이터 수집기 모듈. 모든 접속 정보는 SystemConfig에서만 로드.

## 2. 구조 개요

* 포함된 클래스:
  - DataCollector: WebSocket→Redis Pub/Sub 실시간 데이터 수집기
* 주요 함수/메서드 목록:
  - stream_prices(): WebSocket에서 실시간 데이터 수신, Redis로 publish
* 외부 API 제공 여부: 해당 없음

## 3. 인터페이스 명세

### 3.1. 입력 (Input)
* 입력 유형: 없음(내부적으로 WebSocket, Redis 접속)
* 형식 및 구조: 해당 없음
* 제약 조건: SystemConfig에 WS_ENDPOINT, REDIS_URL 필요
* 예시: 해당 없음

### 3.2. 출력 (Output)
* 출력 유형: None(내부적으로 Redis publish)
* 형식 및 구조: 해당 없음
* 예시: 해당 없음
* 반환 조건: 실시간 데이터 수신 시

## 4. 내부 처리 로직
* 처리 흐름 요약:
  1. SystemConfig에서 WebSocket/Redis 접속 정보 로드
  2. WebSocket 연결 후 실시간 데이터 수신
  3. 수신 즉시 Redis Pub/Sub 채널로 publish
* 순서도/플로우차트: 해당 없음
* 알고리즘 요약: WebSocket→Redis Pub/Sub 실시간 데이터 배포

## 5. 예외 처리
* 주요 예외 유형: 연결 실패, 데이터 수신 오류 등
* 발생 조건: WebSocket/Redis 연결 실패 등
* 대응 방식: logger로 기록, 예외 발생 시 재시도/종료
* 로깅/알림: logger 활용

## 6. 연관 모듈 및 외부 시스템
* 상위 호출자: core/bot 등
* 하위 호출 대상: SystemConfig, logger
* 연계되는 DB/캐시/메시지큐: Redis
* 타 모듈 간 의존 관계: core/bot, SystemConfig

## 7. 리소스 및 성능
### 7.1. 리소스 소비
* CPU 예상 사용량: 매우 낮음(비동기)
* 메모리 예상 사용량: 매우 낮음
* 병렬성 또는 멀티스레딩 여부: asyncio 기반 비동기
### 7.2. 성능 기준
* 처리량 기준 (TPS/건수): WebSocket/Redis 처리량에 따름
* 응답 시간: 매우 짧음(실시간)
* 지연 허용 한계: 해당 없음
* 초기화 시간: 매우 짧음

## 8. 설정 및 의존성
* 사용하는 DB 테이블 및 필드: SystemConfig(WS_ENDPOINT, REDIS_URL)
* 설정값 및 기본값: SystemConfig에서만 로드
* 외부 환경 변수: 해당 없음
* 사용하는 서드파티/외부 API: websockets, redis

## 9. 테스트 및 검증
* 단위 테스트 항목: stream_prices 정상 동작
* 예외 테스트 항목: WebSocket/Redis 연결 실패 등
* 통합 테스트 체크리스트: 실시간 데이터 수집 및 배포 정상 동작
* 테스트 커버리지 목표: 90% 이상

## 10. 제약사항 및 향후 계획
* 현재 한계: 외부 데이터 포맷 고정, 예외처리 단순
* 기술적 부채: 재연결/복구 미흡
* 향후 개선/확장 예정 사항: 다양한 거래소 지원, 재연결/복구 강화
* 폐지 예정 요소: 해당 없음

| 객체 | 설명 |
|------|------|
| `DataCollector` | WebSocket→Redis Pub/Sub 실시간 데이터 수집기 |
| `stream_prices()` | 실시간 데이터 수신 및 Redis publish |
