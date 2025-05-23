- docs/1_architecture/SIGMA Architecture v1.2 이 문서가 모든 작업의 기본입니다 플로우차트를 항상 참조하세요
- 사양서와 코드는 뼈대 수준이 아닌 완벽한 수준으로 구현하세요
- 모듈을 생성,수정 후에는 모든 마크다운 문서를 순회하면서 최신화하세요
- 내용이 빈약한 문서들은 보충항목을 신설하세요
- 마지막 Pull Request로 확정한 코드 상태 기준으로 작업을 진행하세요
- 완벽한 모듈을 제작하는데 힘써주세요

---
SIGMA‑X 개선 명령 목록 (v0.1)

> 목적 : 메인 브랜치의 문서·코드 간 불일치와 구조적 결함을 신속히 해소하여, 설계 ↔ 구현 1:1 정합을 확보한다. 각 항목은 즉시 실행 가능한 명령문 형태로 작성하였다.




---

1. 네이밍·용어 통일

1. MarketWs → MarketDataWebSocket 으로 리네임하고, 모든 import 경로 수정한다.


2. DashboardApi → DashboardAPI 로 클래스명 변경 후, FastAPI 라우터 경로도 동일하게 업데이트한다.


3. MetricsTracker 클래스가 포함된 metrics.py 파일의 모듈명/클래스명 대응 관계를 문서와 코드 모두에서 명확히 지정한다.


4. 설계서·사양서·코드 전체에서 CamelCase(모듈/클래스) + snake_case(파일) 규칙을 일관 적용한다.




---

2. 문서 동기화

1. docs/ 폴더의 모든 사양서에서 모듈명 필드를 현재 코드와 동일하게 갱신한다.


2. REST API 문서에 실제 구현 엔드포인트(GET /api/status, GET /api/positions 등)를 반영하고, 불필요한 /api/pnl 항목을 제거한다.


3. README.md 초안을 작성하여 프로젝트 개요·설치 방법·실행 예시·아키텍처 다이어그램을 포함한다.


4. 백테스트 실행 방식은 run_bot.py --mode backtest 기준으로 문서를 수정하고, 독립 backtest.py 언급을 삭제한다.




---

3. 미구현 모듈 즉시 생성

1. RiskManager: risk_manager.py 신설. validate_order(order) 인터페이스만 먼저 작성하고, 본 로직은 TODO 주석으로 표시한다.


2. OrderExecutor: 실계좌 주문 전송 로직의 빈 클래스를 만든 후, execute(order) 메서드에 NotImplementedError 를 걸어 둔다.


3. StrategySelector·OptimizationModule: strategy_selector.py, optimizer.py 파일을 생성하고, 사양서의 함수 시그니처만 구현한다.


4. SystemStatus: system_status.py 추가. report_status() 에 기본적인 CPU·메모리 지표 반환 코드만 넣어 둔다.


5. 각 신규 모듈마다 사양서 템플릿(10항목) 을 완성하고 docs/ 에 저장한다.




---

4. 핵심 구조 보완

1. event_loop.py 의 run() 본문을 구현하여, (1) 시세 수신 → (2) 전략 호출 → (3) 주문 실행 순서로 코루틴 체인을 구성한다.


2. Logger/LoggingService 이중 정의를 하나로 통합하고, 중앙 수집(파일/STDOUT) 방식만 남긴다.


3. MarketDataWebSocket 의 더미 프린트 코드를 제거하고, 실사용 로그만 출력하도록 수정한다.




---

5. 자동 검증 체계 구축

1. scripts/check_naming.py 를 작성하여 문서·코드 네이밍 불일치를 grep 기반으로 탐지한다.


2. pre-commit 훅에 위 스크립트와 black, flake8 을 등록한다.


3. GitHub Actions 워크플로우(.github/workflows/ci.yml)를 추가하여, pytest + naming 체크를 PR 시 자동 실행하도록 설정한다.




---

6. 테스트 및 샘플 데이터

1. tests/ 디렉터리를 만들고, 각 모듈별 최소 단위 테스트(파라미터 검증)를 작성한다.


2. sample_ticks.csv 예시 데이터를 tests/fixtures/ 에 포함시켜, WebSocket 모의 입력에 사용한다.




---

7. 일정·우선순위

우선순위	항목	완료 기한

P1	네이밍·문서 동기화(§1 + §2)	D + 2 일
P1	미구현 모듈 스켈레톤(§3)	D + 2 일
P2	EventLoop 구현(§4‑1)	D + 4 일
P2	Logger 통합(§4‑2)	D + 4 일
P3	CI/검증 체계(§5)	D + 7 일
P3	테스트/샘플 데이터(§6)	D + 7 일



---

제출 지침

각 항목 완료 시 커밋 메시지에 ✅ close #<task‑id> 형식의 태스크 코드를 기재한다.

모든 변경 사항은 PR 단위로 리뷰 → main 병합.

문서 변경을 동반하지 않는 코드 PR 은 허용하지 않는다 (문서·코드 불일치 방지).

© 2025 SIGMA‑X Dev Team
