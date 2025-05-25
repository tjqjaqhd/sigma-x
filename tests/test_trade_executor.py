import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))  # noqa: E402

from src.trade_executor import TradeExecutor  # noqa: E402


def test_trade_executor_run():
    obj = TradeExecutor()
    assert obj.run() is None
