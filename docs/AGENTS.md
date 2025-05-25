# AGENT for docs

## 목적
프로젝트 설계·운용 문서를 MkDocs 기반으로 관리하는 공간입니다.  
아키텍처, 컴포넌트 설명, 사용자 가이드를 **오프라인에서도** 열람할 수 있게 합니다.

## 테스트 규칙
- 문서 빌드·미리보기 시 **외부 네트워크 금지**  
- 다이어그램은 `mmdc`, `dot` 같은 로컬 CLI로 생성  
- 이미지·리소스는 `docs/assets` 내부에만 저장  
- 문서 스크립트(`generate_docs.py`, `gen_diagrams.sh`) 실행 후 **빌드 오류 0** 확인

## 테스트 스타일
- `mkdocs build` 로 정적 사이트 생성 여부 확인  
- 다이어그램 스크립트는 `pytest` 대신 **쉘 스크립트** 단위 테스트(`assert $(ls *.svg | wc -l) -gt 0`)  
- 링크 검사: `mkdocs serve -q` 후 링크 체크 스크립트 실행

## 예시 도구
```bash
# 다이어그램 일괄 변환
bash docs/scripts/gen_diagrams.sh
# 문서 빌드
mkdocs build --strict
-변경사항이 있으면 알맞게 고치세요