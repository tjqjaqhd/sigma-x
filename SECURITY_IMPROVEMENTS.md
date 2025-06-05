# 보안 개선 사항

## 즉시 적용 필요

### 1. 환경변수 기반 설정
```bash
# .env 파일 생성
SIGMA_SECRET_KEY=your-super-secret-key-here-at-least-32-chars
SIGMA_ADMIN_PASSWORD=strong-admin-password
SIGMA_TRADER_PASSWORD=strong-trader-password
```

### 2. 비밀번호 해싱
```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

### 3. 토큰 만료 시간 단축
```python
token_expire_seconds = 300  # 5분으로 단축
```

## 권장 보안 헤더
```python
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response
```
