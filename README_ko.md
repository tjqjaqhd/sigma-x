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

## 의존성 설치

개발 환경에서는 `requirements.txt`와 `requirements-dev.txt` 두 파일을 사용합니다.
다음 명령어로 모든 의존성을 설치할 수 있습니다.

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```


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
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## 봇 실행 방법
```bash
python run_bot.py
```

## 주요 변경 사항

- 모든 설정은 DB의 `system_config` 테이블에서 로드됩니다.
- `initialize()` 호출 시 DB 테이블이 자동으로 생성되며 `/metrics` 경로가 노출됩니다.

## PDF 문서 변환

`Sigma-X 자동매매 시스템 아키텍처 분석.pdf` 파일의 내용을 텍스트로 활용하려면
다음 스크립트를 실행합니다.

```bash
python scripts/pdf_to_md.py 'Sigma-X 자동매매 시스템 아키텍처 분석.pdf' docs/architecture_summary.md
```

`docs/architecture_summary.md` 파일이 생성되면 내용을 검토 후 서식을 정리해 사용합니다.
