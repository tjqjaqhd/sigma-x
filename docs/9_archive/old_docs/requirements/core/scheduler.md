# core.scheduler 모듈 사양

## 1. 모듈 개요

* 모듈명: core.scheduler
* 작성자: AI 자동화
* 작성일: 2024-06-XX
* 최종 검토자: AI 자동화
* 최종 수정일: 2024-06-XX

**설명:**
봇 및 기타 작업을 주기적으로 실행하기 위한 스케줄러 모듈. APScheduler가 설치되어 있으면 BackgroundScheduler를, 없으면 SimpleScheduler(내장 스레드 기반)를 사용하여 주기적 작업을 실행한다.

## 2. 구조 개요

* 포함된 클래스:
  - SimpleScheduler: 스레드 기반 간단 스케줄러
* 주요 함수/메서드 목록:
  - add_job(func, interval_seconds): 주기적 작업 등록
  - start(): 스케줄러 시작
  - shutdown(): 스케줄러 종료
  - _run(): 내부 스레드 루프
  - start_bot_scheduler(bot, interval_seconds): APScheduler/내장 스케줄러 자동 선택 및 실행
* 외부 API 제공 여부: 해당 없음

## 3. 인터페이스 명세

### 3.1. 입력 (Input)
* 입력 유형: callable(작업 함수), int(주기), TradingBot 인스턴스
* 형식 및 구조: func: callable, interval_seconds: int, bot: TradingBot
* 제약 조건: func은 인자 없는 함수, interval_seconds > 0
* 예시: bot.run, 60

### 3.2. 출력 (Output)
* 출력 유형: None, scheduler 인스턴스
* 형식 및 구조: None, SimpleScheduler/BackgroundScheduler 객체
* 예시: 반환값 없음 또는 스케줄러 객체
* 반환 조건: 스케줄러 시작/종료 시

### 3.3. API 엔드포인트 (해당 시)
* URL: 해당 없음
* Method: 해당 없음
* 인증: 해당 없음
* 설명: 해당 없음
* 요청/응답 예시: 해당 없음

## 4. 내부 처리 로직
* 처리 흐름 요약:
  1. add_job으로 작업과 주기 등록
  2. start()로 스레드/스케줄러 시작
  3. _run()에서 주기적으로 작업 실행
  4. shutdown()으로 안전하게 종료
  5. start_bot_scheduler는 APScheduler/내장 스케줄러 자동 선택
* 순서도/플로우차트: 해당 없음
* 알고리즘 요약: 스레드/스케줄러 기반 주기적 작업 실행

## 5. 예외 처리
* 주요 예외 유형: AssertionError(작업 미등록 시)
* 발생 조건: add_job 없이 start 시
* 대응 방식: assert로 강제
* 로깅/알림: 해당 없음

## 6. 연관 모듈 및 외부 시스템
* 상위 호출자: core/bot, __main__.py 등
* 하위 호출 대상: TradingBot, APScheduler(외부)
* 연계되는 DB/캐시/메시지큐: 해당 없음
* 타 모듈 간 의존 관계: core/bot

## 7. 리소스 및 성능
### 7.1. 리소스 소비
* CPU 예상 사용량: 매우 낮음(주기적 대기)
* 메모리 예상 사용량: 매우 낮음
* 병렬성 또는 멀티스레딩 여부: 스레드 기반, APScheduler 지원
### 7.2. 성능 기준
* 처리량 기준 (TPS/건수): 주기적 작업 빈도에 따라 다름
* 응답 시간: 실시간성 아님
* 지연 허용 한계: 해당 없음
* 초기화 시간: 매우 짧음

## 8. 설정 및 의존성
* 사용하는 DB 테이블 및 필드: 해당 없음
* 설정값 및 기본값: interval_seconds(기본 60)
* 외부 환경 변수: 해당 없음
* 사용하는 서드파티/외부 API: APScheduler(선택적)

## 9. 테스트 및 검증
* 단위 테스트 항목: add_job, start, shutdown 정상 동작
* 예외 테스트 항목: add_job 없이 start 시 AssertionError
* 통합 테스트 체크리스트: TradingBot과 연동, 주기적 실행 정상 동작
* 테스트 커버리지 목표: 90% 이상

## 10. 제약사항 및 향후 계획
* 현재 한계: 분산/클러스터 스케줄링 미지원
* 기술적 부채: APScheduler 미설치 시 기능 제한
* 향후 개선/확장 예정 사항: 분산 스케줄러, 작업 모니터링, 동적 작업 추가/삭제
* 폐지 예정 요소: 해당 없음

| 객체/함수 | 설명 |
|-----------|------|
| `SimpleScheduler` | 쓰레드를 이용해 주기적으로 작업을 실행하는 간단한 스케줄러 |
| `start_bot_scheduler(bot, interval_seconds)` | 봇을 일정 간격으로 실행하기 위한 헬퍼 함수 |
