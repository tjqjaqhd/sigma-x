# Sigma 서버 개요

이 문서는 Naver Cloud Platform에서 동작 중인 sigma VPS 서버의 기본 정보를 요약합니다. 또한 PR(풀 리퀘스트)이 제대로 동작하지 않을 때 확인해야 할 사항들을 정리합니다. 프로젝트에 포함된 모듈은 SIGMA 자동매매 시스템 구현 요구사항을 간단히 만족하도록 구성되어 있습니다.

## 모듈 개요

프로젝트는 다음과 같은 초기화 모듈을 포함합니다.

- `config_loader.py`: 환경변수와 데이터베이스 설정 로드
- `plugin_loader.py`: 외부 플러그인 로드
- `metrics.py`: 간단한 메트릭 시스템 초기화
- `user_prefs.py`: 사용자 선호 설정 로드
- `health_check.py`: 헬스 체크 수행
- `cache.py`: 캐시 초기화
- `notification_service.py`: 알림 서비스 초기화
- `api_service.py`: FastAPI 기반 API 서버 생성
- `event_loop.py`: 이벤트 루프 시작
- 그 밖에도 세션 관리 및 로깅 설정 등이 포함됩니다.

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

### 봇 실행
```bash
python run_bot.py
```

### 코드 스타일 검사
```bash
flake8
black --check .
```
