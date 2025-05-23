# SIGMA-X 프로젝트

SIGMA-X는 단일 VPS에서 동작하는 자동 매매 시스템입니다. 실전(LIVE), 시뮬레이션(SIM), 백테스트(BACKTEST) 모드가 동일한 코드 경로로 실행되도록 설계되었습니다.

## 설치 방법
```bash
pip install -r requirements.txt
```

## 실행 예시
```bash
python src/sigma/run_bot.py --mode live
```

자세한 아키텍처 설명과 모듈 사양서는 `docs/` 디렉터리를 참고하세요.
