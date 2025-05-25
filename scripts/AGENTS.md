```markdown
# AGENT for scripts

## 목적
스펙 → 코드/다이어그램/문서 자동화 유틸 모음입니다.  
반복 작업을 CLI 한 줄로 처리해 생산성을 높입니다.

## 테스트 규칙
- 모든 스크립트는 **오프라인**에서 완전히 동작해야 함  
- 의존 도구(mmdc, graphviz 등) 미설치 시 **친절한 오류 메시지** 출력  
- 이미 존재하는 파일은 덮어쓰지 않도록 설계(데이터 손실 방지)

## 테스트 스타일
- `pytest` → 각 스크립트 `--help` 가 0 종료코드 반환  
- `subprocess.run([...], check=True)` 로 자체 호출해 smoke-test  
- 출력 파일 hash 비교로 재현성 확인

## 예시 도구
```python
def test_scaffold_help():
    import subprocess, sys
    r = subprocess.run([sys.executable, "scripts/scaffold.py", "--help"])
    assert r.returncode == 0
-변경사항이 있으면 알맞게 고치세요
