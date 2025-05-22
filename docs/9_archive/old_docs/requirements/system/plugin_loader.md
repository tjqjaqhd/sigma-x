# system.plugin_loader 모듈 사양

## 1. 모듈 개요

* 모듈명: system.plugin_loader
* 작성자: AI 자동화
* 작성일: 2024-06-XX
* 최종 검토자: AI 자동화
* 최종 수정일: 2024-06-XX

**설명:**
플러그인 디렉토리 내 PluginBase 상속 플러그인을 동적으로 로드, 등록, 실행하는 모듈. 플러그인 기반 전략 확장, 동적 로딩, 실행, 로깅을 담당한다.

## 2. 구조 개요

* 포함된 클래스:
  - 해당 없음(외부 PluginBase 사용)
* 주요 함수/메서드 목록:
  - load_plugins(directory): 플러그인 동적 로드 및 등록
  - run_all_plugins(*args, **kwargs): 등록된 플러그인 일괄 실행
* 외부 API 제공 여부: 해당 없음

**설명:**
- load_plugins: 지정 디렉토리 내 PluginBase 상속 플러그인 동적 로드, on_load 실행, 로깅
- run_all_plugins: 등록된 플러그인 run 메서드 일괄 실행, 로깅

## 3. 인터페이스 명세

### 3.1. 입력 (Input)
* 입력 유형: str(directory), *args, **kwargs
* 형식 및 구조: directory(str, 기본값 'sigma/plugins'), 플러그인 run 인자
* 제약 조건: directory는 실제 플러그인 경로여야 함
* 예시: 'sigma/plugins'

### 3.2. 출력 (Output)
* 출력 유형: None
* 형식 및 구조: None
* 예시: 해당 없음
* 반환 조건: 플러그인 로드/실행 완료 시

### 3.3. API 엔드포인트 (해당 시)
* URL: 해당 없음
* Method: 해당 없음
* 인증: 해당 없음
* 설명: 해당 없음
* 요청/응답 예시: 해당 없음

## 4. 내부 처리 로직
* 처리 흐름 요약:
  1. load_plugins: 디렉토리 내 py 파일 탐색, PluginBase 상속 클래스 동적 로드, on_load 실행, plugins 리스트 등록, 로깅
  2. run_all_plugins: plugins 리스트 순회, 각 플러그인 run 실행, 로깅
* 순서도/플로우차트: 해당 없음
* 알고리즘 요약: importlib, inspect로 동적 클래스 탐색 및 실행

## 5. 예외 처리
* 주요 예외 유형: Exception(플러그인 로드/실행 실패)
* 발생 조건: 플러그인 import/실행 오류 등
* 대응 방식: logger.exception으로 예외 상세 기록
* 로깅/알림: logger.info, logger.warning, logger.exception 등 활용

## 6. 연관 모듈 및 외부 시스템
* 상위 호출자: system 초기화 등
* 하위 호출 대상: utils/logger, plugins/plugin_base
* 연계되는 DB/캐시/메시지큐: 해당 없음
* 타 모듈 간 의존 관계: utils/logger, plugins/plugin_base

## 7. 리소스 및 성능
### 7.1. 리소스 소비
* CPU 예상 사용량: 매우 낮음(동적 import, 함수 실행)
* 메모리 예상 사용량: 매우 낮음
* 병렬성 또는 멀티스레딩 여부: 해당 없음
### 7.2. 성능 기준
* 처리량 기준 (TPS/건수): 플러그인 수에 비례
* 응답 시간: 매우 짧음
* 지연 허용 한계: 해당 없음
* 초기화 시간: 매우 짧음

## 8. 설정 및 의존성
* 사용하는 DB 테이블 및 필드: 해당 없음
* 설정값 및 기본값: directory='sigma/plugins'
* 외부 환경 변수: 해당 없음
* 사용하는 서드파티/외부 API: importlib, inspect

## 9. 테스트 및 검증
* 단위 테스트 항목: load_plugins 정상 동작, run_all_plugins 실행
* 예외 테스트 항목: 플러그인 import/실행 실패 등
* 통합 테스트 체크리스트: 전체 시스템 초기화와 연동, 플러그인 정상 로드/실행
* 테스트 커버리지 목표: 90% 이상

## 10. 제약사항 및 향후 계획
* 현재 한계: 플러그인 구조 단순, 예외처리 단순
* 기술적 부채: 동적 import/실행 예외처리 미흡
* 향후 개선/확장 예정 사항: 플러그인 상태 관리, 동적 언로드, 플러그인 메타데이터 관리
* 폐지 예정 요소: 해당 없음

| 함수 | 설명 |
|------|------|
| `load_plugins()` | 플러그인 디렉토리 내 PluginBase 상속 플러그인 동적 로드 및 등록 |
| `run_all_plugins()` | 등록된 플러그인 일괄 실행 | 