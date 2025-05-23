# SIGMA 모듈 사양서

이 문서는 SIGMA 프로젝트의 각 모듈을 명확히 기록하기 위한 문서입니다. 모든 항목은 누락 없이 작성하며, 해당 사항이 없을 경우 **해당 없음**으로 표기합니다.

## 1. 모듈 개요
* 모듈명: RiskManager
* 작성자: TBD
* 작성일: 2025-05-22
* 최종 검토자: TBD
* 최종 수정일: 2025-05-22

주문 초안을 검증하여 증거금 부족, 주문 한도 초과, 중복 주문 등을 체크한다. 검증 통과 시 Executor로 전달하며, 실패 시 알림과 로그를 남긴다.

## 2. 구조 개요
* 포함된 클래스/함수: `RiskManager`, `check_margin`, `check_limits`
* 주요 메서드: `validate_order()`, `record_rejection()`
* 외부 API 제공 여부: 없음
* 소스 파일 위치: `sigma/risk_manager.py`

## 3. 인터페이스 명세
### 3.1 입력
* 입력 유형: 주문 초안 dict
* 형식 및 구조: `{symbol, side, size, price}`
* 제약 조건: 가격·수량 음수 불가, 잔고 체크 필요
* 예시: `{"symbol":"BTC/KRW","side":"buy","size":0.01,"price":101}`

### 3.2 출력
* 출력 유형: 검증 결과 dict 또는 예외
* 형식 및 구조: `{valid: bool, reason?: str}`
* 예시: `{"valid":false,"reason":"Insufficient balance"}`
* 반환 조건: valid=true인 경우 Executor로 전달

### 3.3 API 엔드포인트(해당 시)
* 해당 없음

## 4. 내부 처리 로직
* 처리 흐름 요약: 주문 파라미터 확인 → 잔고·리스크 한도 조회 → 결과 반환
* 순서도/플로우차트: RealTimeLoop의 Risk 단계 참조
* 알고리즘 요약: 계좌 정보는 Postgres에서 조회, 결과 캐싱

## 5. 예외 처리
* 주요 예외 유형: DB 연결 실패, 값 오류
* 발생 조건: Postgres 다운, 입력 데이터 누락
* 대응 방식: 재시도 후 실패 시 주문 거부
* 로깅/알림: `logger.py` 기록, NotificationService에 전송

## 6. 연관 모듈 및 외부 시스템
* 상위 호출자: StrategyManager 또는 TradingBot
* 하위 호출 대상: OrderExecutor, SimulatorExecutor
* 연계되는 DB/캐시/메시지큐: Postgres, Redis 캐시
* 타 모듈 간 의존 관계: metrics.py와 연동하여 리젝 통계 수집

## 7. 리소스 및 성능
### 7.1 리소스 소비
* CPU 예상 사용량: 0.3 vCPU 이하
* 메모리 예상 사용량: 200MB 이하
* 병렬성 또는 멀티스레딩 여부: asyncio 사용

### 7.2 성능 기준
* 처리량 기준: 초당 수천 건 주문 검증
* 응답 시간: 평균 50ms 이하
* 지연 허용 한계: 250ms
* 초기화 시간: 1초 이하

## 8. 설정 및 의존성
* 사용하는 DB 테이블 및 필드: `accounts`, `risk_limits`
* 설정값 및 기본값: 최대 주문 수량, 레버리지 한도
* 외부 환경 변수: `POSTGRES_DSN`
* 사용하는 서드파티/외부 API: 해당 없음

## 9. 테스트 및 검증
* 단위 테스트 항목: 각 검증 함수, 경계 조건
* 예외 테스트 항목: 잔고 부족, 한도 초과
* 통합 테스트 체크리스트: StrategyManager → RiskManager → Executor 흐름
* 테스트 커버리지 목표: 80% 이상

## 10. 제약사항 및 향후 계획
* 현재 한계: 단일 계좌 기준 로직만 구현
* 기술적 부채: 리스크 규칙 추가 시 코드 복잡도 증가
* 향후 개선/확장 예정 사항: 다계좌 지원, 고급 리스크 모델
* 폐지 예정 요소: 없음
