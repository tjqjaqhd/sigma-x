# core.bot 모듈 사양

| 객체 | 설명 |
|------|------|
| `TradingBot` | 전략 실행과 주문 처리를 담당합니다. 생성 시 `BaseStrategy`와 `DataCollector`를 받습니다. `run(iterations)`을 호출하면 시장 데이터를 수집하고 전략 신호를 생성해 `OrderExecutor`로 전달합니다. |
