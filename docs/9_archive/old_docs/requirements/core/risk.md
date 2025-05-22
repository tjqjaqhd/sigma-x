# core.risk 모듈 사양

## 1. 모듈 개요

* 모듈명: core.risk
* 작성자: AI 자동화
* 작성일: 2024-06-XX
* 최종 검토자: AI 자동화
* 최종 수정일: 2024-06-XX

**설명:**
매매 신호의 유효성 평가(RiskManager), 가격 이상치 감지(AnomalyDetector), 뉴스 이벤트 로깅(NewsHandler) 등 리스크 관리 및 이벤트 감지 기능을 제공하는 모듈.

## 2. 구조 개요

* 포함된 클래스:
  - RiskManager: 신호 유효성 평가
  - AnomalyDetector: 가격 이상치 감지
  - NewsHandler: 뉴스 이벤트 로깅
* 주요 함수/메서드 목록:
  - RiskManager.evaluate(signal): 신호 유효성 판정
  - AnomalyDetector.detect(price): 가격 이상치 감지
  - NewsHandler.process(news): 뉴스 이벤트 로깅
* 외부 API 제공 여부: 해당 없음

## 3. 인터페이스 명세

### 3.1. 입력 (Input)
* 입력 유형: str(신호), float(가격), str(뉴스)
* 형식 및 구조: "BUY"/"SELL", price: float, news: str
* 제약 조건: 신호는 "BUY"/"SELL"만 허용
* 예시: "BUY", 100.0, "FOMC 발표"

### 3.2. 출력 (Output)
* 출력 유형: bool, None
* 형식 및 구조: True/False(유효성/이상치), None(로깅)
* 예시: True, False, None
* 반환 조건: 평가/감지/로깅 결과 반환

### 3.3. API 엔드포인트 (해당 시)
* URL: 해당 없음
* Method: 해당 없음
* 인증: 해당 없음
* 설명: 해당 없음
* 요청/응답 예시: 해당 없음

## 4. 내부 처리 로직
* 처리 흐름 요약:
  1. RiskManager.evaluate: 신호가 "BUY"/"SELL"인지 판정, 아니면 logger.warning
  2. AnomalyDetector.detect: 가격이 0 이하인지 감지
  3. NewsHandler.process: 뉴스 문자열을 logger.info로 기록
* 순서도/플로우차트: 해당 없음
* 알고리즘 요약: 단순 조건문 기반 평가/감지/로깅

## 5. 예외 처리
* 주요 예외 유형: 해당 없음(내부적으로 logger.warning/info 등 활용)
* 발생 조건: 신호 비정상, 가격 음수/0, 뉴스 문자열 등
* 대응 방식: logger.warning/info로 기록
* 로깅/알림: logger.warning/info 등 활용

## 6. 연관 모듈 및 외부 시스템
* 상위 호출자: core/bot, system/plugin_loader 등
* 하위 호출 대상: utils/logger
* 연계되는 DB/캐시/메시지큐: 해당 없음
* 타 모듈 간 의존 관계: core/bot 등

## 7. 리소스 및 성능
### 7.1. 리소스 소비
* CPU 예상 사용량: 매우 낮음
* 메모리 예상 사용량: 매우 낮음
* 병렬성 또는 멀티스레딩 여부: 해당 없음
### 7.2. 성능 기준
* 처리량 기준 (TPS/건수): 실시간 신호/이벤트 발생 빈도에 따라 다름
* 응답 시간: 매우 짧음
* 지연 허용 한계: 해당 없음
* 초기화 시간: 매우 짧음

## 8. 설정 및 의존성
* 사용하는 DB 테이블 및 필드: 해당 없음
* 설정값 및 기본값: 해당 없음
* 외부 환경 변수: 해당 없음
* 사용하는 서드파티/외부 API: 해당 없음

## 9. 테스트 및 검증
* 단위 테스트 항목: evaluate, detect, process 정상 동작
* 예외 테스트 항목: 신호/가격/뉴스 비정상 입력
* 통합 테스트 체크리스트: core/bot 등과 연동
* 테스트 커버리지 목표: 90% 이상

## 10. 제약사항 및 향후 계획
* 현재 한계: 고도화된 리스크/이상치/뉴스 분석 미흡
* 기술적 부채: 단순 조건문 기반, logger 의존
* 향후 개선/확장 예정 사항: ML 기반 리스크/이상치 탐지, 외부 뉴스 API 연동
* 폐지 예정 요소: 해당 없음

| 객체 | 설명 |
|------|------|
| `RiskManager` | 매매 신호의 유효성을 판별, logger.warning 활용 |
| `AnomalyDetector` | 가격 이상치를 감지 |
| `NewsHandler` | 뉴스 이벤트를 logger.info로 기록 |