# SIGMA 모듈 사양서

이 문서는 SIGMA 프로젝트의 각 모듈을 명확히 기록하기 위한 문서입니다. 모든 항목은 누락 없이 작성하며, 해당 사항이 없을 경우 **해당 없음**으로 표기합니다.

## 1. 모듈 개요
* 모듈명: TradingBot
* 작성자: TBD
* 작성일: 2025-05-22
* 최종 검토자: TBD
* 최종 수정일: 2025-05-22

업비트·바이낸스 등 거래소의 실시간 틱 데이터를 받아 전략을 실행하고 주문 파이프라인을 오케스트레이션한다. 주문 체결 후 포지션과 잔고를 갱신하며 지표 및 알림 모듈과 연동한다.

## 2. 구조 개요
* 포함된 클래스/함수: `TradingBot`, `handle_tick`, `update_position`
* 주요 메서드: `start()`, `process_tick()`, `dispatch_order()`
* 외부 API 제공 여부: 없음
* 소스 파일 위치: `sigma/tradingbot.py`

## 3. 인터페이스 명세
### 3.1 입력
* 입력 유형: Redis 채널 `market.tick` 메시지
* 형식 및 구조: JSON `{symbol, bid, ask, ts}`
* 제약 조건: 100 ms 단위, 시계열 순서 보장
* 예시: `{"symbol":"BTC/KRW","bid":100,"ask":101,"ts":1620000000}`

### 3.2 출력
* 출력 유형: 주문 초안 이벤트
* 형식 및 구조: Python dict `{symbol, side, size, price}`
* 예시: `{"symbol":"BTC/KRW","side":"buy","size":0.01,"price":101}`
* 반환 조건: 비동기 큐 전송

### 3.3 API 엔드포인트(해당 시)
* 해당 없음

## 4. 내부 처리 로직
* 처리 흐름 요약: 틱 수신 → StrategyManager 호출 → RiskManager 검증 → Executor 전송 → 포지션 갱신
* 순서도/플로우차트: 아키텍처 문서의 RealTimeLoop 참조
* 알고리즘 요약: asyncio 기반 이벤트 루프, 각 단계 비동기 호출

## 5. 예외 처리
* 주요 예외 유형: 네트워크 지연, 데이터 포맷 오류
* 발생 조건: Redis 연결 끊김, JSON 파싱 실패 등
* 대응 방식: 재시도 로직, 오류 로그 후 해당 틱 무시
* 로깅/알림: `logger.py` 사용, 심각 오류 시 NotificationService 호출

## 6. 연관 모듈 및 외부 시스템
* 상위 호출자: MarketDataWebSocket, HistoricalDataLoader
* 하위 호출 대상: StrategyManager, RiskManager, MetricsTracker, NotificationService
* 연계되는 DB/캐시/메시지큐: Redis, Postgres
* 타 모듈 간 의존 관계: OrderExecutor 또는 SimulatorExecutor와 직접 연결

## 7. 리소스 및 성능
### 7.1 리소스 소비
* CPU 예상 사용량: 0.5 vCPU 이하
* 메모리 예상 사용량: 256MB 이하
* 병렬성 또는 멀티스레딩 여부: asyncio 단일 스레드

### 7.2 성능 기준
* 처리량 기준: 초당 10,000 틱까지 처리
* 응답 시간: 평균 100ms 이하
* 지연 허용 한계: 최대 600ms
* 초기화 시간: 1초 미만

## 8. 설정 및 의존성
* 사용하는 DB 테이블 및 필드: `positions`, `orders`
* 설정값 및 기본값: `MAX_POSITION`, `RISK_LIMIT`
* 외부 환경 변수: `MODE`, `REDIS_URL`, `POSTGRES_DSN`
* 사용하는 서드파티/외부 API: 없음

## 9. 테스트 및 검증
* 단위 테스트 항목: 틱 처리 로직, 주문 생성 로직
* 예외 테스트 항목: Redis 오류, 잘못된 입력 처리
* 통합 테스트 체크리스트: StrategyManager 및 Executor 연동
* 테스트 커버리지 목표: 80% 이상

## 10. 제약사항 및 향후 계획
* 현재 한계: 단일 서버 기반으로 확장성 제한
* 기술적 부채: 전략 플러그인 검증 절차 미흡
* 향후 개선/확장 예정 사항: 멀티 서버 지원, 전략 A/B 테스트 도구
* 폐지 예정 요소: 없음
