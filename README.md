# SIGMA-X

SIGMA-X는 단일 VPS 환경에서 동작하도록 설계된 자동매매 시스템입니다. 실전 거래(LIVE), 실시간 시뮬레이션(SIM), 과거 백테스트(BACKTEST) 세 가지 모드를 지원하며 비동기 이벤트 처리와 모듈화된 구조를 채택했습니다. 상세한 아키텍처는 `docs/1_architecture` 폴더를 참고하세요.

## 의존성 설치
```bash
pip install -r requirements.txt
```

## 사용 방법
`DataCollector`는 수집한 데이터를 RabbitMQ 큐에 전달하고 `TradeExecutor`는 해당 큐를 소비하여 주문을 실행합니다. 아래와 같이 실행해 볼 수 있습니다.

```python
import asyncio
from src.data_collector import DataCollector
from src.trade_executor import TradeExecutor


async def main():
    collector = DataCollector()
    executor = TradeExecutor()
    await asyncio.gather(
        collector.run(limit=5),
        executor.run(limit=5),
    )


asyncio.run(main())
```

모듈은 사용자의 전략에 맞게 자유롭게 확장할 수 있습니다.

## 코드 스타일
본 프로젝트는 `black`과 `flake8`을 사용해 코드 품질을 유지하며,
라인 길이 제한은 120자로 설정되어 있습니다.

## 빌드 및 테스트
별도의 빌드 단계는 없으며 다음 명령으로 테스트를 실행할 수 있습니다.
```bash
pytest
```

## 시스템 명세
`specs/sigma_system.yaml` 파일은 컨테이너와 컴포넌트, 그리고 데이터 흐름을 YAML 형식으로 기술합니다.
자세한 구조 설명은 `docs/sigma_yaml_structure.md` 문서를 참고하세요.

## 다이어그램 생성
`scripts/generate_diagrams.py`를 실행하면 YAML 명세를 바탕으로 `docs/sigma_system_diagram.mmd` 파일이 생성됩니다.
`--split` 옵션을 주면 각 컨테이너별로 `<이름>_diagram.mmd` 파일이 별도로 저장됩니다.
`docs/scripts/gen_diagrams.sh` 스크립트는 mermaid-cli(mmdc)와 graphviz(dot)를 이용해
`docs` 디렉터리의 모든 `.mmd`, `.dot` 파일을 일괄적으로 SVG로 변환합니다.
CI 환경에서도 자동으로 실행되므로, 로컬에서도 아래와 같이 실행해 최신 다이어그램을 확인할 수 있습니다.

필요 패키지 설치 예시:

```bash
sudo npm install -g @mermaid-js/mermaid-cli
sudo apt-get install -y graphviz
```

실행 방법:

```bash
bash docs/scripts/gen_diagrams.sh
```

## 스캐폴드 생성
`scripts/scaffold.py` 스크립트는 `specs/sigma_system.yaml` 파일을 읽어
`src/`와 `tests/` 디렉터리에 기본 모듈과 `pytest` 테스트 템플릿을 만듭니다.
간단한 동작 예시는 `specs/example.yaml` 파일을 활용해 확인할 수 있습니다.

```bash
/usr/bin/python3 scripts/scaffold.py
```

## 문서 생성
`scripts/generate_docs.py` 스크립트를 실행하면 YAML 명세와 코드 정보를 이용해
`docs/` 폴더의 Markdown 문서를 갱신합니다. 이후 `mkdocs build` 명령을 실행하면
정적 사이트가 `site/` 디렉터리에 생성됩니다.

```bash
/usr/bin/python3 scripts/generate_docs.py
mkdocs build
```

## CI 자동 실행
`specs/` 디렉터리의 YAML 파일을 수정하면 GitHub Actions가 자동으로 세 가지 스크립트
(`generate_diagrams.py`, `scaffold.py`, `generate_docs.py`)을 실행합니다. 실행 결과
생성된 파일이 커밋에 반영되어 있지 않으면 워크플로우가 실패하므로, YAML 변경 시 해당
파일들을 함께 커밋해야 합니다. 이후 모든 테스트가 실행되어 통과해야 합니다.

