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
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: example
    ports:
      - "5432:5432"
  api:
    build: .
    command: python -m src.api_server
    environment:
      SIGMA_REDIS_URL: redis://redis:6379
      SIGMA_DB_URL: postgresql://postgres:example@db:5432/postgres
    ports:
      - "8000:8000"
  scheduler:
    build: .
    command: python -m src.sigma_scheduler
    environment:
      MODE: live
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
  alertmanager:
    image: prom/alertmanager
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
    ports:
      - "9093:9093"
```

프로젝트 루트에 위 파일을 저장한 뒤 다음 명령으로 서비스를 실행합니다.

```bash
docker compose up -d
```

Prometheus와 Grafana는 각각 `http://localhost:9090`, `http://localhost:3000`에서
접근할 수 있습니다. Alertmanager는 `http://localhost:9093` 포트를 사용합니다.

로컬 환경에서 실행하려면 단순히 다음과 같이 실행할 수 있습니다.

```bash
python -m src.api_server
```

전체 구성은 아래 다이어그램을 참고하세요.

![메인 다이어그램](main_diagram.svg)
