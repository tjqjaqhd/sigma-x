import os
from typing import AsyncIterator


class HistoricalDataLoader:
    """과거 시세 데이터를 순차적으로 로드하는 간단한 로더."""

    def __init__(self, source: str | None = None) -> None:
        self.source = source or os.getenv("SIGMA_HISTORY_CSV", "history.csv")

    async def load(self) -> AsyncIterator[float]:
        """CSV 파일에서 가격을 비동기적으로 읽어 들인다."""
        if not os.path.exists(self.source):
            return
        with open(self.source) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                yield float(line)
