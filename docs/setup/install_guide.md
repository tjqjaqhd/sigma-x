# Sigma 시스템 설치 가이드

본 문서는 sigma 시스템의 설치 및 환경설정 절차를 안내한다.

## 1. 사전 준비
- Python 3.12 이상
- PostgreSQL, Redis, RabbitMQ 등 외부 서비스
- 가상환경(venv) 권장

## 2. 환경설정
- .env 파일에는 DATABASE_URL 한 줄만 작성
- 나머지 모든 설정은 DB(SystemConfig) 테이블에서 관리
- 예시:
  ```
  DATABASE_URL=postgresql://user:password@localhost:5432/sigma
  ```

## 3. 의존성 설치
```bash
pip install -r requirements.txt
```

## 4. DB 초기화
```bash
alembic upgrade head
```

## 5. SystemConfig 환경변수 등록
- DB(system_config 테이블)에 필수 환경변수(RABBIT_URL, ORDERS_QUEUE 등) 등록
- 등록 방법은 [env_vars.md](env_vars.md) 참고

## 6. 서비스 실행
- 실시간 데이터 수집, 주문 파이프라인, 알림 등은 모두 DB 기반 설정을 사용
- 운영/테스트 환경 분리, 로그/임시파일 커밋 금지

> 추가 문의 및 상세 설정은 [가이드라인](../guides/README.md) 참고 