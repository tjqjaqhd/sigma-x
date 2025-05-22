# Sigma 시스템 환경변수 명세 (SystemConfig)

본 문서는 sigma 시스템에서 DB(system_config 테이블)로 관리하는 필수 환경변수를 안내한다.

| 변수명         | 용도                | 예시                                      | 설명                       |
|---------------|---------------------|-------------------------------------------|----------------------------|
| RABBIT_URL    | RabbitMQ 접속 URL   | amqp://guest:guest@localhost:5672/        | 주문 파이프라인 메시지큐   |
| ORDERS_QUEUE  | 주문 큐 이름        | orders                                    | RabbitMQ 주문 큐 이름      |
| REDIS_URL     | Redis 접속 URL      | redis://localhost:6379/0                  | 실시간 데이터 Pub/Sub      |
| SLACK_TOKEN   | Slack API 토큰      | xoxb-...                                  | 알림(Notification) 채널    |
| ...           | ...                 | ...                                       | ...                        |

- 모든 환경변수는 DB(system_config)에 직접 등록/수정
- .env에는 DATABASE_URL만 작성, 나머지는 DB에서 관리
- 신규 환경변수 추가 시 반드시 본 문서와 DB 모두 동기화

> 상세 등록/수정 방법은 [설치 가이드](install_guide.md) 참고 