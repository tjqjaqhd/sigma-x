# core.adaptation 모듈 사양

## 1. 모듈 개요

* 모듈명: core.adaptation
* 작성자: AI 자동화
* 작성일: 2024-06-XX
* 최종 검토자: AI 자동화
* 최종 수정일: 2024-06-XX

**설명:**
시장 국면 탐지(RegimeDetector), 전략 파라미터 DB 반영(ParamAdjuster), 성과 평가(QualityAssessment), 피드백 기록(FeedbackMechanism) 등 전략 적응 및 자동화 기능을 제공하는 모듈.

## 2. 구조 개요

* 포함된 클래스:
  - RegimeDetector: 시장 국면(상승/하락/미확정) 탐지
  - ParamAdjuster: 전략 파라미터 DB 반영 및 실시간 감시
  - QualityAssessment: 전략 성과 평가
  - FeedbackMechanism: 평가 결과 기록
* 주요 함수/메서드 목록:
  - RegimeDetector.detect(prices): 가격 리스트로 국면 판정
  - ParamAdjuster.watch(callback): DB 파라미터 변경 감시 및 콜백 호출
  - ParamAdjuster.update_parameter(name, value): 파라미터 DB 반영
  - QualityAssessment.evaluate(returns): 수익률 리스트 평가
  - FeedbackMechanism.record(metric): 평가 결과 기록
* 외부 API 제공 여부: 해당 없음

## 3. 인터페이스 명세

### 3.1. 입력 (Input)
* 입력 유형: list[float](가격/수익률), str(파라미터명/값), 콜백 함수
* 형식 및 구조: prices: list[float], returns: list[float], name: str, value: str, callback: callable
* 제약 조건: prices/returns는 비어있을 수 있음
* 예시: [100.0, 105.0], [0.01, -0.02], "param1", "value1"

### 3.2. 출력 (Output)
* 출력 유형: str(국면), float(평가값), None(콜백/DB 반영/기록)
* 형식 및 구조: "bull"/"bear"/"unknown", float, None
* 예시: "bull", 0.015, None
* 반환 조건: 판정/평가/DB 반영/기록 시

### 3.3. API 엔드포인트 (해당 시)
* URL: 해당 없음
* Method: 해당 없음
* 인증: 해당 없음
* 설명: 해당 없음
* 요청/응답 예시: 해당 없음

## 4. 내부 처리 로직
* 처리 흐름 요약:
  1. RegimeDetector.detect: 가격 리스트로 국면 판정("bull"/"bear"/"unknown")
  2. ParamAdjuster.watch: DB 파라미터 변경 감지 시 콜백 호출(비동기 루프)
  3. ParamAdjuster.update_parameter: 파라미터 DB에 반영
  4. QualityAssessment.evaluate: 수익률 평균 계산
  5. FeedbackMechanism.record: 평가값 리스트에 기록
* 순서도/플로우차트: 해당 없음
* 알고리즘 요약: 단순 조건문/DB 조회/평균 계산/리스트 기록

## 5. 예외 처리
* 주요 예외 유형: 해당 없음(내부적으로 DB 연결/조회 실패 등 가능)
* 발생 조건: DB 연결 실패, 파라미터 미존재 등
* 대응 방식: finally로 세션 종료, 예외 발생 시 무시
* 로깅/알림: 해당 없음

## 6. 연관 모듈 및 외부 시스템
* 상위 호출자: core/bot, system/plugin_loader 등
* 하위 호출 대상: src.sigma.data.models.StrategyParam, DB 세션
* 연계되는 DB/캐시/메시지큐: strategy_param 테이블
* 타 모듈 간 의존 관계: data/models, db/database

## 7. 리소스 및 성능
### 7.1. 리소스 소비
* CPU 예상 사용량: 매우 낮음(간단 연산/DB 조회)
* 메모리 예상 사용량: 매우 낮음
* 병렬성 또는 멀티스레딩 여부: watch는 asyncio 기반 비동기 루프
### 7.2. 성능 기준
* 처리량 기준 (TPS/건수): DB 감시 주기(1초), 평가/기록 빈도에 따라 다름
* 응답 시간: 실시간성 아님(1초 주기)
* 지연 허용 한계: 해당 없음
* 초기화 시간: 매우 짧음

## 8. 설정 및 의존성
* 사용하는 DB 테이블 및 필드: strategy_param(name, value)
* 설정값 및 기본값: 해당 없음
* 외부 환경 변수: 해당 없음
* 사용하는 서드파티/외부 API: 해당 없음

## 9. 테스트 및 검증
* 단위 테스트 항목: detect, evaluate, record, update_parameter 정상 동작
* 예외 테스트 항목: 빈 리스트, DB 연결 실패 등
* 통합 테스트 체크리스트: DB 연동, 파라미터 실시간 반영, 평가/기록 정상 동작
* 테스트 커버리지 목표: 90% 이상

## 10. 제약사항 및 향후 계획
* 현재 한계: 고도화된 국면 탐지/파라미터 최적화/피드백 미흡
* 기술적 부채: 단순 조건문/평균 기반, DB 감시 polling 방식
* 향후 개선/확장 예정 사항: ML 기반 국면 탐지, 파라미터 자동 최적화, 피드백 자동화
* 폐지 예정 요소: 해당 없음

| 객체 | 설명 |
|------|------|
| `RegimeDetector` | 가격 리스트로 시장 국면(상승/하락/미확정) 판정 |
| `ParamAdjuster` | 전략 파라미터를 DB에 반영하고 실시간 감시 |
| `QualityAssessment` | 수익률 리스트로 전략 성과 평가 |
| `FeedbackMechanism` | 평가 결과를 리스트에 기록 | 