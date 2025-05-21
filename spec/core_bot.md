# core.bot 모듈 사양

| 객체 | 설명 |
|------|------|
| `TradingBot` | 전략 실행과 주문 처리를 담당합니다. 생성 시 `BaseStrategy`와 `DataCollector`를 받습니다. `run()` 실행 시 시장 데이터를 수집하여 전략 신호를 생성하고 `OrderExecutor`로 전달합니다. |
