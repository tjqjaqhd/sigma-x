# Sigma 문서 개요

이 디렉터리는 프로젝트 전반의 문서를 모아두는 공간입니다. `README_ko.md`에는 서버 및 환경 설정, 의존성 설치 방법, 테스트 실행법이 정리되어 있습니다.

## 문서 구조

- `docs/` : 프로젝트 사용 방법과 운영 가이드를 담습니다.
- `spec/` : 각 파이썬 모듈과 1:1로 매핑되는 상세 사양서를 작성합니다.

프로젝트를 처음 접하는 사용자는 `README_ko.md`를 읽은 뒤 필요한 추가 정보를 이곳에서 확인하세요.

## 기본 사용법

1. 의존성 설치
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

2. 데이터베이스 초기화
   ```bash
   python -m sigma.db.init_db
   ```

3. 봇 실행
   ```bash
   python run_bot.py
   ```

4. 테스트 및 커버리지 확인
   ```bash
   pytest --cov=sigma -q
   ```

위 명령으로 커버리지 90% 이상을 유지하는지 확인할 수 있습니다.

