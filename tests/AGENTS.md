```markdown
# AGENT for tests

## 목적
`src` 모듈을 검증하는 단위·통합 테스트 모음입니다.

## 테스트 규칙
- **pytest 단독 실행**으로 전체 테스트 통과해야 함  
- 외부 네트워크·시스템 자원 접근 금지  
- 테스트간 상태 오염 방지를 위해 픽스처로 자원 관리

## 테스트 스타일
- 공통 픽스처는 `tests/conftest.py` 에서 관리  
- 비동기 테스트는 `pytest.mark.asyncio`  
- 커버리지 목표 80 % 이상 (`pytest --cov`)

## 예시 도구
```bash
# 전체 테스트 실행
pytest -q
# 커버리지
pytest --cov=src --cov-report=term-missing
-변경사항이 있으면 알맞게 고치세요