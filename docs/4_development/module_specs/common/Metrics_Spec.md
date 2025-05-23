# SIGMA 모듈 사양서

이 문서는 SIGMA 프로젝트의 각 모듈을 명확히 기록하기 위한 문서입니다. 모든 항목은 누락 없이 작성하며, 해당 사항이 없을 경우 **해당 없음**으로 표기합니다.

## 1. 모듈 개요
* 모듈명: metrics.py
* 작성자: TBD
* 작성일: 2025-05-22
* 최종 검토자: TBD
* 최종 수정일: 2025-05-22

시스템 전반의 지표(P&L, 주문 지연, 시스템 상태)를 수집하여 Prometheus Pushgateway로 전송한다. Grafana 대시보드에서 모니터링이 가능하도록 지표 포맷을 맞춘다.

## 2. 구조 개요
* 포함된 클래스/함수: `MetricsTracker`, `collect_pnl`, `collect_latency`
* 주요 메서드: `push_metrics()`, `start()`
* 외부 API 제공 여부: 없음
* 소스 파일 위치: `sigma/metrics.py`

## 3. 인터페이스 명세
### 3.1 입력
* 입력 유형: 시스템 이벤트, 체결 정보
* 형식 및 구조: `{event_type, value, ts}`
* 제약 조건: 이벤트 발생 시 비동기 호출
* 예시: `{"event_type":"fill","value":101,"ts":1620000001}`

### 3.2 출력
* 출력 유형: Prometheus metric push
* 형식 및 구조: HTTP POST body
* 예시: `profit_total 1000`
* 반환 조건: Pushgateway 응답 확인 후 완료

### 3.3 API 엔드포인트(해당 시)
* 해당 없음

## 4. 내부 처리 로직
* 처리 흐름 요약: 이벤트 수집 → 메트릭 변환 → Pushgateway 전송
* 순서도/플로우차트: Observability 흐름 참조
* 알고리즘 요약: 비동기 버퍼링, 주기적 푸시

## 5. 예외 처리
* 주요 예외 유형: Pushgateway 접속 실패
* 발생 조건: 네트워크 장애, HTTP 오류
* 대응 방식: 재시도 및 로컬 버퍼 저장
* 로깅/알림: 실패 횟수 누적 시 NotificationService 호출

## 6. 연관 모듈 및 외부 시스템
* 상위 호출자: TradingBot, Executor 등 모든 모듈
* 하위 호출 대상: Prometheus Pushgateway
* 연계되는 DB/캐시/메시지큐: 없음
* 타 모듈 간 의존 관계: DashboardAPI와 지표 공유

## 7. 리소스 및 성능
### 7.1 리소스 소비
* CPU 예상 사용량: 0.2 vCPU 이하
* 메모리 예상 사용량: 100MB 이하
* 병렬성 또는 멀티스레딩 여부: asyncio 사용

### 7.2 성능 기준
* 처리량 기준: 초당 수백 이벤트 집계
* 응답 시간: 평균 50ms 이하
* 지연 허용 한계: 200ms
* 초기화 시간: 1초 이하

## 8. 설정 및 의존성
* 사용하는 DB 테이블 및 필드: 해당 없음
* 설정값 및 기본값: Pushgateway URL, 푸시 주기
* 외부 환경 변수: `PUSHGATEWAY_URL`
* 사용하는 서드파티/외부 API: Prometheus Pushgateway

## 9. 테스트 및 검증
* 단위 테스트 항목: 메트릭 포맷 변환, 푸시 로직
* 예외 테스트 항목: 네트워크 장애 시 재시도
* 통합 테스트 체크리스트: Grafana에서 지표 확인
* 테스트 커버리지 목표: 80% 이상

## 10. 제약사항 및 향후 계획
* 현재 한계: Pushgateway 단일 엔드포인트 의존
* 기술적 부채: 지표 종류가 제한적
* 향후 개선/확장 예정 사항: 커스텀 지표 추가, 알림 임계치 세분화
* 폐지 예정 요소: 없음
