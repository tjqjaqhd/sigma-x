# SIGMA-X

SIGMA-X는 단일 VPS 환경에서 동작하도록 설계된 자동매매 시스템입니다. 실전 거래(LIVE), 실시간 시뮬레이션(SIM), 과거 백테스트(BACKTEST) 세 가지 모드를 지원하며 비동기 이벤트 처리와 모듈화된 구조를 채택했습니다. 상세한 아키텍처는 `docs/1_architecture` 폴더를 참고하세요.

## 의존성 설치
```bash
pip install -r requirements.txt
```

## 사용 방법
현재 기본 코드베이스는 템플릿 형태로 제공되며, 각 모듈은 사용자의 전략에 맞게 확장할 수 있습니다. 구체적인 사용 예시는 추후 문서를 통해 제공될 예정입니다.

## 빌드 및 테스트
별도의 빌드 단계는 없으며 다음 명령으로 테스트를 실행할 수 있습니다.
```bash
pytest
```

## 시스템 명세
`specs/sigma_system.yaml` 파일은 컨테이너와 컴포넌트, 그리고 데이터 흐름을 YAML 형식으로 기술합니다.
자세한 구조 설명은 `docs/sigma_yaml_structure.md` 문서를 참고하세요.

## 다이어그램 생성
`scripts/generate_diagrams.py` 스크립트를 실행하면 YAML 명세를 바탕으로 Mermaid 문법의 다이어그램 파일이 `docs/sigma_system_diagram.mmd`에 저장됩니다.

```bash
/usr/bin/python3 scripts/generate_diagrams.py
```

