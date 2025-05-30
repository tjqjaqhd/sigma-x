# `sigma_system.yaml` 구조 설명

이 파일은 SIGMA-X 시스템의 컨테이너, 컴포넌트 그리고 데이터 흐름을 정의합니다.
YAML 형식은 다음과 같습니다.

```yaml
containers:
  - name: <컨테이너 이름>
    description: <설명>
    components:
      - name: <컴포넌트 이름>
        type: <service|database 등>
        image: <도커 이미지 태그>
    flows:
      - from: <출발 컴포넌트>
        to: <도착 컴포넌트>
        channel: <통신 방식>
        description: <데이터 전달 내용>
```

각 항목의 의미는 아래와 같습니다.

- **containers**: 시스템을 구성하는 컨테이너 단위 목록입니다.
- **components**: 컨테이너 내에서 동작하는 주요 모듈이나 서비스입니다.
- **flows**: 컴포넌트 간 데이터 이동 경로와 방식입니다.

예시는 `specs/sigma_system.yaml`에서 확인할 수 있습니다.
`scripts/generate_diagrams.py`를 실행하면 이 YAML 파일로부터 Mermaid 다이어그램(`docs/sigma_system_diagram.mmd`)을 생성할 수 있습니다. `--split` 옵션을 사용하면 컨테이너별 다이어그램도 함께 생성됩니다.
추가로 `specs/example.yaml`에는 스캐폴드 동작을 확인할 수 있는 간단한 예제가 포함되어 있습니다.
