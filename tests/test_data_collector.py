import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))  # noqa: E402

from src.data_collector import DataCollector  # noqa: E402


def test_data_collector_run():
    obj = DataCollector()
    assert obj.run() is None
