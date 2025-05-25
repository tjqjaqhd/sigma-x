# 환경 설정 가이드

Docker Compose를 이용해 SIGMA-X 서비스를 구성하는 방법을 설명합니다.

## docker-compose.yml 예시
```yaml
version: "3"
services:
  redis:
    image: redis:7
    ports:
      - "6379:6379"
  api:
    build: .
    command: python -m src.api_server
    environment:
      SIGMA_REDIS_URL: redis://redis:6379
    ports:
      - "8000:8000"
```

프로젝트 루트에 위 파일을 저장한 뒤 다음 명령으로 서비스를 실행합니다.

```bash
docker compose up -d
```

로컬 환경에서 실행하려면 단순히 다음과 같이 실행할 수 있습니다.

```bash
python -m src.api_server
```

전체 구성은 아래 다이어그램을 참고하세요.

![메인 다이어그램](main_diagram.svg)
