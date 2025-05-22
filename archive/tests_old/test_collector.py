from sigma.data.collector import DataCollector


def test_data_collector_returns_dict():
    collector = DataCollector()
    data = collector.fetch_market_data()
    assert isinstance(data, dict)
