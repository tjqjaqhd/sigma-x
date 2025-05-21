# 환경설정 관리

## DB 기반 설정

- 모든 시스템 설정은 DB(system_config 테이블)에서 관리합니다.
- .env 파일은 오직 DATABASE_URL 한 줄만 허용합니다.
- 기타 API 키, 토큰 등은 SystemConfig.get(key)로 접근해야 하며, .env에서 직접 로드하지 않습니다. 