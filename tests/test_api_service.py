from sigma.common.api_service import APIService


def test_api_service_init():
    api = APIService()
    assert hasattr(api, "get")
