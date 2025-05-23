from sigma.core.data_cleaner import DataCleaner


def test_data_cleaner_init():
    dc = DataCleaner()
    assert hasattr(dc, "clean")
