SIGMA 자동매매 시스템 구현 요구사항

시스템 목표

24시간 무인 자동매매 운영

실시간 전략 조정 및 시장 변화 대응

모의체결 및 백테스트 환경 제공

사용자 맞춤형 대시보드 제공 (실시간 데이터 및 과거 성과 분석)


시스템 구성

1. 초기화 단계

환경변수 및 데이터베이스 설정 로드

ORM 테이블 자동 생성 (SQLAlchemy)

전역 로깅 시스템 설정

외부 플러그인 및 사용자 선호 설정 불러오기

모니터링 지표(Prometheus) 설정

시스템 헬스 체크 및 캐시(Redis) 초기화

알림 서비스 및 FastAPI REST/WS 서버 초기화


2. 실시간 처리 루프

WebSocket을 통해 실시간 가격 수신

Redis Pub/Sub을 이용한 실시간 가격 발행 및 구독

전략 신호 생성(TradingBot), 주문 실행(OrderExecutor)

모의 체결 시뮬레이션(SimRunner)

시장 국면 탐지(RegimeDetector) 및 전략 파라미터 자동 조정(ParamAdjuster)

주문 처리(RabbitMQ, OrderWorker, PostgreSQL)

리스크 관리 및 알림 서비스(NotificationService)

품질 평가 및 피드백 메커니즘

이상치 및 뉴스 기반 이벤트 처리


3. 스케줄러 작업

일일 전략 선택 및 최적화

데이터 정리 및 오래된 틱 데이터 자동 삭제

시스템 상태 정기 점검 및 알림

시장 추세 스캔 및 분석 데이터 저장

주간 성과 리포트 생성 및 배포

머신러닝 기반 전략 자동 튜닝

로그 회전 및 설정 동기화

사용자 활성 상태 및 권한 주기 점검


4. 시뮬레이션 모드

Redis 구독을 통한 실시간 데이터 모의체결

전략별 시그널 생성 및 결과 저장

모의체결 통계 및 결과 분석 자동화

데이터 시각화 및 리포트 생성

사용자 피드백 및 결과 내보내기


5. 백테스트 모드

히스토리 데이터 로드 (CSV, Parquet, PostgreSQL)

전략별 신호 생성 및 시뮬레이션 체결

백테스트 결과 요약 및 시각화

성능 비교 및 전략 개선 추천

리포트 생성 및 인사이트 공유


6. API 및 대시보드

FastAPI 기반 REST API 및 WebSocket 실시간 방송

React 기반의 실시간 및 과거 데이터 시각화 대시보드

사용자 인증 및 권한 관리

사용자 맞춤형 보고서 및 알림 제공

시스템 상태 모니터링 및 알림 서비스


운영 환경 권장 사항

VPS: Ubuntu 24.04, 4 vCPU, 16 GB RAM

시스템 부하 관리를 위한 resource limit(systemd)

데이터베이스: PostgreSQL + TimescaleDB (메모리 4GB 할당)

캐시 및 메시지 큐: Redis 및 RabbitMQ (메모리 각 500MB)

모니터링: Prometheus, Grafana 및 Alertmanager


본 문서를 기준으로 시스템을 구현하며, 각 모듈의 세부적인 사항은 플로우차트 및 테스트 코드를 참조한다.

flowchart TB
  subgraph Initialization____Initialization__
    A["run_bot.py:main()"] --> B["config_loader.py:load_env(),load_db_config()"]
    B --> C["db/session.py:create_engine(),SessionLocal"]
    C --> D["db/models.py:Base.metadata.create_all()"]
    D --> E["logger.py:init_logger()"]
    E --> F["plugin_loader.py:load_plugins()"]
    F --> G["metrics.py:init_metrics()"]
    G --> H["user_prefs.py:load_user_preferences()"]
    H --> I["health_check.py:check_system_health()"]
    I --> J["cache.py:init_cache()"]
    J --> K["additional_setup.py:configure_additional_services()"]
    K --> L["notification_service.py:init_notification()"]
    L --> M["api_service.py:init_api()"]
    M --> N["event_loop.py:start_event_loop()"]
    N --> O["session_manager.py:init_session()"]
    O --> P["logging_service.py:init_logging()"]
  end
  subgraph RealTimeLoop____Real_Time_Loop__
    WS["WebSocket:receive_prices()"] --> Q["Redis.publish('price_update')"]
    Q --> TB["TradingBot:generate_signals(),execute_order()"]
    Q --> SIM["SimRunner:simulate_execution()"]
    Q --> RD["RegimeDetector:detect_regime()"]
    RD --> PA["ParamAdjuster:update_parameters()"]
    PA --> SPT["Update strategy_param table"]
    PA --> FB["FeedbackMechanism"]
    FB --> RD
    FB --> QA["QualityAssessment"]
    QA --> RD
    TB --> R["RabbitMQ Queue:publish_order_event()"]
    R --> OW["OrderWorker:consume_event(),place_api()"]
    OW --> DB1["PostgreSQL:store orders & positions"]
    OW --> PM["PaymentProcessor:process_payments()"]
    SIM --> DB2["PostgreSQL:store sim_orders"]
    TB --> MT["MetricsTracker:record_metrics()"]
    TB --> Notif["NotificationService:send_alerts()"]
    Notif --> Alerts["AlertLog"]
    TB --> Log["ActionLogger:log_actions()"]
    Log --> Alerts
    TB --> ST["StrategyTester:validate_strategy()"]
    ST --> TB
    TB --> RR["RiskManager:evaluate_risk()"]
    RR --> Alerts
    TB --> NS["NewsHandler:process_market_news()"]
    NS --> RD
    TB --> AD["AnomalyDetector:identify_outliers()"]
    AD --> TB
    TB --> DC["DataCleaner:clean_data()"]
    TB --> CMT["CommentaryModule:generate_market_commentary()"]
  end
  subgraph Scheduler____Scheduled_Jobs__
    SS["StrategySelector:daily at 03:00"] --> SPT
    SS --> OPT["OptimizationModule:run_backtests()"]
    OPT --> SPT
    DC["DataCleaner:prune_old_ticks()"] --> DB1
    HC["HealthCheck:every 30s"] --> Alerts
    HC --> HM["HealthMetrics:update_metrics()"]
    TS["TrendScanner:scan_trends()"] --> RD
    TS --> DB3["PostgreSQL:trend_data table"]
    PR["PerformanceReporter:weekly report"] --> DB4["PostgreSQL:performance_reports"]
    PR --> Alerts
    ML["MLModule:auto_tuning()"] --> OS["store_optimal_strategies"]
    SS --> PR
    SS --> ML
    SS --> LR["LogRotator:manage_logs()"]
    SS --> CS["ConfigSync:sync_with_cloud()"]
    SS --> UV["UserValidation:check_active_users()"]
    SS --> TM["TaskManager:manage_scheduled_tasks()"]
    SS --> UR["UserRightsManager:check_permissions()"]
    SS --> EA["EmailAlert:send_daily_summary()"]
  end
  subgraph Simulation____Simulation_Mode__
    RS["runner_sim.py:subscribe 'price_update'"] --> SM["StrategyManager:generate_signals()"]
    SM --> SX["SimulatorExecutor:simulate_fill()"]
    SX --> DB5["PostgreSQL:sim_orders"]
    SX --> ST["SimulationStats:generate_stats()"]
    ST --> SR["SimulationResults:analyze_results()"]
    ST --> EM["ErrorMonitor:log_execution_errors()"]
    SM --> DV["DataVisualizer:render_simulation()"]
    SM --> CL["ConfigLoader:load_simulation_config()"]
    CL --> SM
    SM --> REPO["ResultExporter:export_results()"]
    SM --> FEEDBACK["UserFeedback:collect_simulation_feedback()"]
  end
  subgraph Backtesting____Backtesting_Mode__
    CLI["backtest.py CLI:strategy & period args"] --> HD["HistoricalDataLoader:load_history()"]
    HD --> SM2["StrategyManager:generate_signals()"]
    SM2 --> SX2["SimulatorExecutor:simulate_fill()"]
    SX2 --> DB6["PostgreSQL:bt_summary"]
    SX2 --> VIZ["VisualizationTool:render_charts()"]
    VIZ --> REP["Report:generate_report()"]
    VIZ --> VM["VisualMetrics:update_metrics()"]
    VIZ --> IN["Insights:generate_insights()"]
    IN --> SH["ShareInsights:distribute()"]
    REP --> AP["ActionPlan:define_next_steps()"]
    REP --> QA2["QualityAssurance:review_report()"]
    QA2 --> R["ReportRepository:store_reports()"]
    HD --> AID["AlgorithmImprovementDetector:refine_strategy()"]
    AID --> REP
    SM2 --> CC["ChangeCalculator:monitor_strategy_changes()"]
    SM2 --> PL["PerformanceLogger:log_backtest_performance()"]
  end
  subgraph APIDashboard____API___Dashboard__
    FA["FastAPI:init_app()"] --> WS2["/ws endpoint"]
    WS2 --> Sub["Redis.subscribe('price_update')"]
    Sub --> FE["ReactDashboard:useWebSocket()"]
    FA --> REST["REST endpoints\n/api/orders,/api/pnl"]
    REST --> DB1_&_DB2_&_DB6_&_DB3
    FA --> Auth["AuthService:authenticate()"]
    FA --> LogSvc["LoggingService:log_requests()"]
    LogSvc --> Alerts
    FE --> US["UserSettings UI"]
    FE --> UP["UserProfile UI"]
    FE --> UR["UserReports UI"]
    Auth --> FE
    Auth --> Notif
    Auth --> Perm["PermissionsService"]
    FE --> RPT["ReportingModule:generate_user_reports()"]
    FE --> DL["DataLoader:fetch_user_data()"]
    FE --> AU["AnalyticsUI:display_user_metrics()"]
    FE --> ST["SystemStatus:display_system_health()"]
    ST --> HM
    FE --> HLP["HelpSection:display_help()"]
    HLP --> FE
    FE --> CH["ChartingModule:display_real_time_charts()"]
  end


테스트코드는 구현 필요 커버리지 90%이상 달성 별도 벤치마크 테스트 요청
