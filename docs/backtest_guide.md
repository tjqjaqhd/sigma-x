# 백테스트 사용 가이드

이 문서는 SIGMA-X에서 백테스트 모드를 실행하는 기본 절차를 설명합니다.

## 1. 준비
- `DataCollector`와 `TradeExecutor` 모듈이 설치되어 있어야 합니다.
- 과거 데이터는 CSV 파일이나 데이터베이스에서 가져올 수 있습니다.

## 2. 실행 방법
아래 예시는 간단한 백테스트 스크립트입니다.

```python
import asyncio
from src.data_collector import DataCollector
from src.trade_executor import TradeExecutor

async def main():
    collector = DataCollector(url="ws://localhost:8765")
    executor = TradeExecutor()
    await asyncio.gather(
        collector.run(limit=100),
        executor.run(limit=100),
    )

asyncio.run(main())
```

- `limit` 값은 처리할 메시지 수를 제한합니다.
- 시세 데이터는 RabbitMQ 큐를 거쳐 처리되며, 결과 주문 내역은 PostgreSQL `orders` 테이블에도 기록됩니다.

## 3. 결과 분석
데이터베이스에 저장된 주문 기록을 조회해 전략 성과를 확인합니다.

```bash
psql -c 'SELECT * FROM orders;'
```

자세한 구조는 [백테스트 흐름](1_architecture/c3_backtest.md)을 참고하십시오.
