# Sigma-X 자동매매 시스템

Sigma-X는 실시간 자동매매, 전략 플러그인, 시뮬레이션/백테스트, API/대시보드 기능을 갖춘 모듈형 트레이딩 서버입니다.

## 필수 사용법

- 의존성 설치
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```
- 테스트 실행: `pytest`
- 코드 스타일 검사: `flake8`, `black --check .`
- 봇 실행: `python src/run_bot.py`

자세한 개발/운영/구성 안내는 `docs/` 디렉토리와 [모듈 사양서](docs/requirements/sigma_spec.md)를 참고하세요.
