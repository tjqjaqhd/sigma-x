# Sigma 문서 개요

이 디렉터리는 프로젝트 전반의 문서를 모아두는 공간입니다. `docs/guides/README.md`에는 서버 및 환경 설정, 의존성 설치 방법, 테스트 실행법이 정리되어 있습니다.

## 문서 구조

- `docs/` : 프로젝트 사용 방법과 운영 가이드를 담습니다.
- `docs/requirements/` : 각 파이썬 모듈과 1:1로 매핑되는 상세 사양서를 작성합니다.


## 기본 사용법

1. `src/run_bot.py`를 실행하면 `sigma.system.initialize()`가 호출되어 필수 서비스가 순차적으로 초기화됩니다.
2. 이후 `TradingBot`이 동작하며 `RegimeDetector`가 시장 국면을 판단하고 `ParamAdjuster`가 전략 파라미터를 DB에 갱신합니다.
3. `NotificationService.notify()` 호출 시 메시지가 DB의 `alert` 테이블에 저장되고 Slack으로 전송됩니다.

`system_config` 테이블에 등록된 설정 값이 초기화 단계에서 자동으로 로드됩니다. `/metrics` 엔드포인트로 Prometheus 지표를 수집할 수 있습니다.

프로젝트를 처음 접하는 사용자는 이 문서를 읽은 뒤 필요한 추가 정보를 이곳에서 확인하세요.


