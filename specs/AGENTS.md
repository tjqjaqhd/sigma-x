```markdown
# AGENT for specs

## 목적
시스템 전체 구조를 YAML로 정의하는 **단일 진실 공급원(SSoT)** 입니다.  
여기서 코드·다이어그램·문서를 자동 생성합니다.

## 테스트 규칙
- YAML 포맷 오류가 없어야 하며 외부 URL·시크릿 포함 금지  
- 스펙 수정 후 `scripts/scaffold.py` 실행 → 새 코드 생성 확인  
- CI 전 단계에서 `python -m py_compile` 로 **구문 검사**

## 테스트 스타일
- `pytest` 로 `yaml.safe_load` 성공 여부만 빠르게 검증  
- 스펙으로 생성된 모듈 존재 여부(`Path("src")/f"{name}.py".exists()`) 확인  
- 다이어그램 노드 수 = YAML 컴포넌트 수 테스트

## 예시 도구
```python
def test_yaml_valid():
    import yaml, pathlib
    for f in pathlib.Path("specs").glob("*.yaml"):
        yaml.safe_load(f.read_text())
-변경사항이 있으면 알맞게 고치세요