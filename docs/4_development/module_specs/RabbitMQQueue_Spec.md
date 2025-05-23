# SIGMA 모듈 사양서

이 문서는 SIGMA 프로젝트의 각 모듈을 명확히 기록하기 위한 문서입니다. 모든 항목은 누락 없이 작성하며, 해당 사항이 없을 경우 **해당 없음**으로 표기합니다.

## 1. 모듈 개요
* 모듈명: RabbitMQQueue
* 작성자: TBD
* 작성일: 2025-05-23
* 최종 검토자: TBD
* 최종 수정일: 2025-05-23

비동기 작업 처리를 위한 메시지 큐 역할을 한다. 전략 최적화 작업이나 리포트 생성
등 시간이 오래 걸리는 태스크를 Queue로 분리한다.

## 2. 구조 개요
* 포함된 클래스/함수: `RabbitMQQueue`, `publish_task`, `consume_task`
* 주요 메서드: `send()`, `listen()`
* 외부 API 제공 여부: 없음
* 소스 파일 위치: `sigma/rabbitmq_queue.py`

## 3. 인터페이스 명세
### 3.1 입력
* 입력 유형: 태스크 메시지
* 형식 및 구조: JSON `{task, payload}`
* 제약 조건: 큐 길이 제한, durable 큐 사용
* 예시: `{"task":"optimize","payload":{...}}`

### 3.2 출력
* 출력 유형: 작업 수행 결과
* 형식 및 구조: `{task, status}`
* 예시: `{"task":"optimize","status":"queued"}`
* 반환 조건: 메시지 큐 전송 성공 시

### 3.3 API 엔드포인트(해당 시)
* 해당 없음

## 4. 내부 처리 로직
* 처리 흐름 요약: 태스크 생성 → RabbitMQ publish → Worker에서 consume
* 순서도/플로우차트: Scheduler flow에서 strategySelector와 연동
* 알고리즘 요약: AMQP 프로토콜 사용, 메시지 ack 기반 신뢰성 보장

## 5. 예외 처리
* 주요 예외 유형: 연결 끊김, 큐 포화
* 발생 조건: 네트워크 장애, 큐 길이 초과
* 대응 방식: 재연결 시도, 로컬 저장 후 재전송
* 로깅/알림: logging_service와 NotificationService 활용

## 6. 연관 모듈 및 외부 시스템
* 상위 호출자: StrategySelector, PerformanceReporter
* 하위 호출 대상: RabbitMQ 서버
* 연계되는 DB/캐시/메시지큐: RabbitMQ
* 타 모듈 간 의존 관계: OptimizationModule에서 작업 결과 수신

## 7. 리소스 및 성능
### 7.1 리소스 소비
* CPU 예상 사용량: 경량
* 메모리 예상 사용량: 30MB 이하
* 병렬성 또는 멀티스레딩 여부: 비동기 소비자 지원

### 7.2 성능 기준
* 처리량 기준: 초당 수백 메시지 처리
* 응답 시간: 큐 등록 10ms 내외
* 지연 허용 한계: 1초 이하
* 초기화 시간: 0.5초 이하

## 8. 설정 및 의존성
* 사용하는 DB 테이블 및 필드: 없음
* 설정값 및 기본값: `RABBITMQ_URL`, `QUEUE_NAME`
* 외부 환경 변수: `RABBITMQ_URL`
* 사용하는 서드파티/외부 API: RabbitMQ

## 9. 테스트 및 검증
* 단위 테스트 항목: publish/consume 동작
* 예외 테스트 항목: 연결 끊김 후 재시도
* 통합 테스트 체크리스트: StrategySelector와 연동한 태스크 큐 확인
* 테스트 커버리지 목표: 80% 이상

## 10. 제약사항 및 향후 계획
* 현재 한계: 단일 브로커 장애 시 중단
* 기술적 부채: 복수 노드 클러스터 미구현
* 향후 개선/확장 예정 사항: 멀티 노드 RabbitMQ 지원, 우선순위 큐 도입
* 폐지 예정 요소: 없음
