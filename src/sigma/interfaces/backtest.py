"""간단한 백테스트 CLI 모듈.

사양은 ``docs/4_development/module_specs/interfaces/Backtest_CLI_Spec.md`` 를
참고한다. 실제 거래 로직 대신 로그만 출력한다.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
from typing import Any, Dict

from sigma.common.config_loader import ConfigLoader


async def run_backtest(config_path: str, start: str, end: str) -> Dict[str, Any]:
    """백테스트 메인 루틴."""

    loader = ConfigLoader()
    config = loader.load(config_path)
    logging.getLogger(__name__).info("백테스트 기간 %s ~ %s", start, end)
    # 실제 로직 대신 결과 요약만 반환
    return {"config": config, "start": start, "end": end}


def cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    args = parser.parse_args(argv)

    asyncio.run(run_backtest(args.config, args.start, args.end))
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(cli())
