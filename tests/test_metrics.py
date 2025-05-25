import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src import metrics_text, record_tick  # noqa: E402


def test_metrics_output():
    record_tick()
    text = metrics_text()
    assert "ticks_processed_total" in text
