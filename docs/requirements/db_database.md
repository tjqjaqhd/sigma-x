# db.database 모듈 사양

| 객체/함수 | 설명 |
|-----------|------|
| `SessionLocal` | SQLAlchemy 세션을 생성하는 팩토리 |
| `Base` | 모델 베이스 클래스 |
| `get_db()` | 세션을 생성하고 종료하는 제너레이터 함수 |
