from sigma.core.news_handler import NewsHandler


def test_news_handler_init():
    nh = NewsHandler()
    assert hasattr(nh, "handle")
