import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))  # noqa: E402

from src.redis import Redis  # noqa: E402


def test_redis_run():
    obj = Redis()
    assert obj.run() is None
