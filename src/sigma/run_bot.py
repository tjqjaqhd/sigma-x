"""SIGMA 진입점 스크립트."""

from __future__ import annotations

import argparse
import asyncio
import logging

from .config_loader import ConfigLoader
from .event_loop import EventLoop


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["live", "sim", "backtest"], default="live")
    parser.add_argument("--config", required=False)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    loader = ConfigLoader()
    config = loader.load(args.config) if hasattr(loader, "load") else {}

    loop = EventLoop()
    if hasattr(loop, "run"):
        asyncio.run(loop.run(mode=args.mode, config=config))
    else:
        logger.warning("EventLoop.run이 구현되지 않았습니다")

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI 진입점
    raise SystemExit(main())

