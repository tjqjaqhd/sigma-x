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
  - OrderWorker: 주문 이벤트 비동기 소비 및 DB 기록
* 주요 함수/메서드 목록:
  - OrderExecutor.__init__(is_simulation): 시뮬레이션 여부 설정
  - OrderExecutor.execute(signal): 주문 신호 실행(로그/실거래)
  - OrderWorker.__init__(queue): 주문 큐 바인딩
  - OrderWorker.start(): 비동기 소비 시작
  - OrderWorker.stop(): 소비 중단
  - OrderWorker._consume(): 주문 이벤트 소비 및 DB 기록(비동기)
* 외부 API 제공 여부: 해당 없음

## 3. 인터페이스 명세

### 3.1. 입력 (Input)
* 입력 유형: str(주문 신호), asyncio.Queue(OrderEvent)
* 형식 및 구조: signal: str, queue: asyncio.Queue[OrderEvent]
* 제약 조건: signal은 "BUY"/"SELL" 등, queue는 asyncio 기반
* 예시: "BUY", queue

### 3.2. 출력 (Output)
* 출력 유형: None(로그/DB 기록)
* 형식 및 구조: None
* 예시: 해당 없음
* 반환 조건: 주문 실행/DB 기록 시

### 3.3. API 엔드포인트 (해당 시)
* URL: 해당 없음
* Method: 해당 없음
* 인증: 해당 없음
* 설명: 해당 없음
* 요청/응답 예시: 해당 없음

## 4. 내부 처리 로직
* 처리 흐름 요약:
  1. OrderExecutor.execute: 시뮬레이션 여부에 따라 주문 신호 로그 또는 실거래 처리
  2. OrderWorker.start: asyncio.create_task로 _consume 비동기 실행
  3. OrderWorker._consume: 큐에서 OrderEvent를 꺼내 DB(Alert)에 기록
  4. OrderWorker.stop: 비동기 태스크 중단
* 순서도/플로우차트: 해당 없음
* 알고리즘 요약: 비동기 큐 기반 주문 이벤트 소비 및 DB 기록

## 5. 예외 처리
* 주요 예외 유형: 해당 없음(내부적으로 DB 연결/커밋 실패 등 가능)
* 발생 조건: DB 연결/커밋 실패, 큐 비동기 오류 등
* 대응 방식: finally로 세션 종료, 예외 발생 시 무시
* 로깅/알림: logger.info로 주문/이벤트 기록

## 6. 연관 모듈 및 외부 시스템
* 상위 호출자: core/bot, system/plugin_loader 등
* 하위 호출 대상: src.sigma.data.models.Alert, db/database, logger
* 연계되는 DB/캐시/메시지큐: alert 테이블
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
* 사용하는 DB 테이블 및 필드: alert(level, message)
* 설정값 및 기본값: is_simulation=True(기본값)
* 외부 환경 변수: 해당 없음
* 사용하는 서드파티/외부 API: 해당 없음

## 9. 테스트 및 검증
* 단위 테스트 항목: execute, start, stop, _consume 정상 동작
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
| `OrderWorker` | asyncio.Queue 기반 주문 이벤트 소비 및 DB 기록 |
