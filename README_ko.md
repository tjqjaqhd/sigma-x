# Sigma 서버 개요

이 문서는 Naver Cloud Platform에서 동작 중인 sigma VPS 서버의 기본 정보를 요약합니다. 또한 PR(풀 리퀘스트)이 제대로 동작하지 않을 때 확인해야 할 사항들을 정리합니다.

## 서버 정보

- 플랫폼: Naver Cloud Platform (VPC 환경)
- 서버 이름: sigma (ID: 105080454)
- 공인 IP: 223.130.139.218
- 비공인 IP: 10.0.1.6
- 이미지: Ubuntu 24.04 LTS (ubuntu-24.04-base)
- 서버 사양: s4-g3 (vCPU 4개 / 메모리 16GB)
- 스토리지: 100GB SSD(`/dev/vda`)
- 하이퍼바이저: KVM
- 서버 상태: 운영 중
- 생성일시: 2025-05-12 16:32 (KST)
- 구동일시: 2025-05-19 19:57 (KST)
- VPC 이름: sigma-vpc
- Subnet: public-subnet1 (KR-1)




## 테스트와 린트 사용 방법

### 테스트 실행
```bash
pytest
```

### 코드 스타일 검사
```bash
flake8
black --check .
```

## 의존성 설치
두 파일을 모두 설치해야 합니다:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## 봇 실행
초기화 모듈을 모두 호출하는 `run_bot.py` 스크립트를 제공합니다.

```bash
python run_bot.py
```

이 스크립트는 환경 변수 로드부터 알림, API 서버 초기화까지
플로우차트에 명시된 과정을 순차적으로 실행한 후 스케줄러를 시작합니다.
