# SIGMA-X 아키텍처 v1.4

## 1. 목적 및 범위

SIGMA-X는 단일 VPS(4 vCPU / 16 GB)에서 동작하는 자동매매 시스템으로, 다음 세 가지 모드를 지원합니다:

* **실전 거래(LIVE)**: 실제 계좌를 통한 자동매매
* **실시간 시뮬레이션(SIM)**: 가상 계좌를 통한 실시간 시뮬레이션
* **과거 백테스트(BACKTEST)**: 과거 데이터를 이용한 전략 검증

## 2. 설계 원칙

1. **이벤트 기반 비동기 처리**
   - Redis Pub/Sub을 통한 실시간 이벤트 처리
   - (선택 사항) RabbitMQ 대신 현재는 Redis Pub/Sub으로 일원화

2. **단일 책임 모듈**
   - 전략 실행 (Strategy)
   - 리스크 관리 (Risk)
   - 주문 실행 (Execution)
   - 시뮬레이션 (Simulation)

3. **점진적 복잡도**
   - MVP → 확장 단계적 접근
   - 모듈별 독립적인 확장 가능

4. **관찰성 기본 탑재**
   - Prometheus: 메트릭 수집
   - Grafana: 대시보드
   - Alertmanager: 알림 관리

5. **컨테이너 기반 배포**
   - Docker Compose 단일 호스트
   - 필요시 모듈별 컨테이너 분리 가능

## 3. 시스템 구조

자세한 시스템 구조는 [C4 아키텍처 다이어그램](./c4_architecture.md)을 참조하세요.

### 3.1 주요 컨테이너

| 컨테이너 | 기술 스택 | 책임 |
|---------|----------|------|
| Database | PostgreSQL | 거래 데이터 저장 |
| Redis | Redis | Pub/Sub 메시징 |
| Analytics | Python | 백테스트 및 분석 |
| API | FastAPI | REST/WebSocket 처리 |
| Bot | Python | 전략 실행 |

### 3.2 주요 컴포넌트

#### API 서비스
- REST: HTTP 요청 처리
- WebSocket: 실시간 데이터 처리
- Auth: 인증/인가
- Health: 상태 모니터링

#### Bot 서비스
- Strategy: 전략 실행
- Risk: 리스크 관리
- Exec: 주문 실행
- Sim: 시뮬레이션

## 4. 데이터 흐름

### 4.1 실시간 거래 (LIVE/SIM)
1. WebSocket을 통한 실시간 시세 수신
2. Redis Pub/Sub을 통한 가격 업데이트 브로드캐스트
3. TradingBot이 전략 실행
4. RiskManager가 주문 검증
5. OrderExecutor/SimulatorExecutor가 주문 처리
6. 결과를 Redis를 통해 브로드캐스트

### 4.2 백테스트
1. HistoricalDataLoader가 과거 데이터 로드
2. StrategyTester가 전략 실행
3. SimulatorExecutor가 가상 체결
4. PerformanceReporter가 결과 분석
5. PostgreSQL에 결과 저장

## 5. 비기능적 요구사항

| 항목 | 목표치 | 비고 |
|-----|--------|------|
| 지연 | 평균 ≤ 250ms, P99 ≤ 600ms | VPS 단일 호스트 왕복 |
| RPO/RTO | 5분 / 30분 | Postgres WAL, Redis AOF |
| 가용성 | 99.5% /월 | 컨테이너 자동 재시작 |
| 보안 | NAVER KMS 관리 키, 30일 회전 | GitHub Actions OIDC |

## 6. 배포 구성

| 계층 | 컨테이너 | 비고 |
|-----|----------|------|
| App | sigma-app | MODE=live/sim/backtest |
| Data | redis, postgres | Named volume db-data |
| Scheduler | sigma-scheduler | 전략 교체 및 리포트 cron |
| Observability | prometheus, grafana, alertmanager | dev/prod 공통 |
| Dev-only | sim_replay, sim_grafana | dev compose override |

## 7. 용어 설명

| 용어 | 설명 |
|-----|------|
| Tick | 100ms 단위 호가/체결 스냅샷 |
| Fill | 주문 체결 이벤트 |
| MODE | live/sim/backtest 환경 스위치 |

## 8. 버전 이력

| 버전 | 날짜 | 주요 변경 |
|-----|------|----------|
| v1.0 | 2025-05-21 | Baseline (거래 5 모듈) |
| v1.1 | 2025-05-22 | Metrics/Notification/Dashboard 추가 |
| v1.2 | 2025-05-22 | SimulatorExecutor/HistoricalDataLoader 통합 |
| v1.3 | 2025-05-23 | C4 아키텍처 다이어그램 적용 |
| v1.4 | 2025-05-23 | 문서 구조 개선 |

---
