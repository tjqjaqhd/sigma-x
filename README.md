# SIGMA-X 프로젝트

SIGMA-X는 단일 VPS에서 동작하는 자동 매매 시스템입니다. 실전(LIVE), 시뮬레이션(SIM), 백테스트(BACKTEST) 모드가 동일한 코드 경로로 실행되도록 설계되었습니다.

## 설치 방법
```bash
pip install -r requirements.txt
```

## 실행 예시
```bash
python src/sigma/interfaces/run_bot.py --mode live
```

## 프로젝트 구조
- `src/sigma/common/` : 공통 유틸리티, 로깅, 설정, 플러그인, 세션 등
- `src/sigma/core/` : 전략, 리스크, 실행, 최적화, 상태 등 핵심 로직
- `src/sigma/interfaces/` : API, WebSocket, CLI, 대시보드 등 외부 인터페이스
- `src/sigma/infrastructure/` : DB, Redis, RabbitMQ 등 인프라 연동
- `src/sigma/legacy/` : 과거 데이터 로더 등 레거시 모듈
- `docs/4_development/module_specs/` : 모든 모듈별 사양서(코드와 1:1 동기화)
- `tests/` : 각 모듈별 최소 단위 테스트, 샘플 데이터
- `scripts/` : 네이밍 자동 검증 등 스크립트

## 테스트 및 자동화
- 모든 모듈별 최소 단위 테스트: `pytest tests/`
- 코드 스타일/린트: `black src tests`, `flake8 src tests`
- 네이밍/사양서 동기화 자동 검증: `python scripts/check_naming.py`
- pre-commit, GitHub Actions CI로 PR/Push 시 자동 검증

## 네이밍/구조 규칙
- 모듈/클래스: CamelCase, 파일/함수: snake_case
- 코드/사양서/문서/테스트/자동화 1:1 동기화 필수
- logger.py 사용 금지, logging_service.py만 사용

## 문서
- 아키텍처/플로우/모듈 사양: `docs/1_architecture/`, `docs/4_development/module_specs/`
- REST API/대시보드/실행/백테스트 등 상세 문서 포함

## 검증 및 품질 관리
- 모든 변경사항은 문서(사양서/README/아키텍처 등)에도 즉시 반영
- scripts/check_naming.py, pytest, flake8, black 등 자동 검증 필수
- main 브랜치 기준, PR+문서 동반 커밋만 허용

자세한 아키텍처 설명과 모듈 사양서는 `docs/` 디렉터리를 참고하세요.
