from sigma.legacy.historical_loader import HistoricalDataLoader


def test_historical_loader_init():
    loader = HistoricalDataLoader()
    assert hasattr(loader, "load_csv")
