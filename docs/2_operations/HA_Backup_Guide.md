# 고가용성 및 백업 가이드

시스템 장애에 대비하여 Redis AOF와 Postgres WAL을 활용한 5분 주기 백업을 권장합니다. 복구 시 Docker Compose로 컨테이너를 재시작하면 됩니다.
