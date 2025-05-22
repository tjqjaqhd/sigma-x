# core.execution 모듈 사양

## 1. 모듈 개요

* 모듈명: core.execution
* 작성자: AI 자동화
* 작성일: 2024-06-XX
* 최종 검토자: AI 자동화
* 최종 수정일: 2024-06-XX

**설명:**
주문 실행(OrderExecutor)과 주문 이벤트 비동기 처리(OrderWorker)를 담당하는 모듈. 시뮬레이션/실거래 구분, 주문 신호 처리, DB 기록 등 자동매매 시스템의 핵심 주문 처리 로직을 제공한다.

## 2. 구조 개요

* 포함된 클래스:
  - OrderExecutor: 주문 실행(실거래/모의)
  - OrderEvent: 주문 신호 데이터 구조체
  - OrderWorker: RabbitMQ(aio_pika) 기반 주문 소비 및 DB 기록
* 주요 함수/메서드 목록:
  - OrderExecutor.__init__(is_simulation): 실거래/시뮬레이션 여부(통합 플래그) 설정
  - OrderExecutor.execute(signal): 주문 신호 실행(실거래/시뮬레이션 분기)
  - OrderWorker.__init__(): SystemConfig에서 RabbitMQ/큐 정보 로드
  - OrderWorker.start(): aio_pika 기반 비동기 소비 시작
  - OrderWorker.stop(): 소비 중단
  - OrderWorker._on_message(): 주문 이벤트 소비 및 orders 테이블 기록
* 외부 API 제공 여부: 해당 없음

## 3. 인터페이스 명세

### 3.1. 입력 (Input)
* 입력 유형: str(주문 신호)
* 형식 및 구조: signal: str
* 제약 조건: signal은 "BUY"/"SELL" 등
* 예시: "BUY"

### 3.2. 출력 (Output)
* 출력 유형: None(로그/DB 기록)
* 형식 및 구조: None
* 반환 조건: 주문 실행/DB 기록 시

### 3.3. API 엔드포인트 (해당 시)
* URL: 해당 없음
* Method: 해당 없음
* 인증: 해당 없음
* 설명: 해당 없음
* 요청/응답 예시: 해당 없음

## 4. 내부 처리 로직
* 처리 흐름 요약:
  1. OrderExecutor.execute: is_simulation 플래그에 따라 실거래/시뮬레이션 코드 경로를 통합 처리
     - 시뮬레이션: 체결가=요청가, 체결시간=now로 Order(status=EXECUTED) 기록
     - 실거래: 실제 거래소 API 호출(추후 구현)
  2. OrderWorker.start: aio_pika 기반 RabbitMQ 큐 비동기 소비 시작
  3. OrderWorker._on_message: RabbitMQ 큐에서 주문 이벤트를 꺼내 orders 테이블에만 기록
  4. OrderWorker.stop: 소비 중단
* 순서도/플로우차트: 해당 없음
* 알고리즘 요약: 비동기 큐 기반 주문 이벤트 소비 및 DB 기록

## 5. 예외 처리
* 주요 예외 유형: 해당 없음(내부적으로 DB 연결/커밋 실패 등 가능)
* 발생 조건: DB 연결/커밋 실패, 큐 비동기 오류 등
* 대응 방식: finally로 세션 종료, 예외 발생 시 무시
* 로깅/알림: logger.info로 주문/이벤트 기록

## 6. 연관 모듈 및 외부 시스템
* 상위 호출자: core/bot, system/plugin_loader 등
* 하위 호출 대상: db/database, logger
* 연계되는 DB/캐시/메시지큐: orders 테이블, RabbitMQ
* 타 모듈 간 의존 관계: data/models, db/database, utils/logger

## 7. 리소스 및 성능
### 7.1. 리소스 소비
* CPU 예상 사용량: 매우 낮음(비동기 큐/DB 기록)
* 메모리 예상 사용량: 매우 낮음
* 병렬성 또는 멀티스레딩 여부: asyncio 기반 비동기 처리
### 7.2. 성능 기준
* 처리량 기준 (TPS/건수): 주문 이벤트 발생 빈도에 따라 다름
* 응답 시간: 매우 짧음(비동기)
* 지연 허용 한계: 해당 없음
* 초기화 시간: 매우 짧음

## 8. 설정 및 의존성
* 사용하는 DB 테이블 및 필드: orders(signal, status, timestamp)
* 설정값 및 기본값: is_simulation=True(기본값, Simulation Mode)
* 외부 환경 변수: 해당 없음
* 사용하는 서드파티/외부 API: 해당 없음

## 9. 테스트 및 검증
* 단위 테스트 항목: execute, start, stop, _on_message 정상 동작
* 예외 테스트 항목: DB 연결/커밋 실패, 큐 오류 등
* 통합 테스트 체크리스트: 주문 신호 처리, DB 기록 정상 동작
* 테스트 커버리지 목표: 90% 이상

## 10. 제약사항 및 향후 계획
* 현재 한계: 실거래소 연동 미흡, 주문 이벤트 구조 단순
* 기술적 부채: 실거래 로직 미구현, 예외처리 미흡
* 향후 개선/확장 예정 사항: 실거래 연동, 주문 이벤트 구조 확장, 예외처리/로깅 강화
* 폐지 예정 요소: 해당 없음

| 객체 | 설명 |
|------|------|
| `OrderExecutor` | 실제 주문 또는 모의 주문을 수행, execute(signal) 제공 |
| `OrderEvent` | 주문 신호 데이터 구조체(dataclass) |
| `OrderWorker` | aio_pika 기반 비동기 RabbitMQ 주문 이벤트 소비 및 orders 테이블 기록 |

## 11. 시뮬레이션/실거래 모드

* OrderExecutor, TradingBot 등 모든 주요 경로는 is_simulation 플래그로 실거래/시뮬레이션을 통합 관리한다.
* CLI에서는 --mode=sim, API에서는 ?mode=sim 파라미터로 시뮬레이션 모드 진입이 가능하다.
* 시뮬레이션 모드(Simulation Mode)는 is_simulation 플래그로 분기한다. SimRunner 용어는 사용하지 않는다.
* 시뮬레이션 모드에서는 체결가=요청가, 체결시간=now로 가상 체결만 기록된다.
