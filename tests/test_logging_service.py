from sigma.common.logging_service import LoggingService


def test_get_logger():
    service = LoggingService()
    logger = service.get_logger("test")
    assert logger.name == "test"


def test_set_level():
    service = LoggingService()
    service.set_level("DEBUG")
    assert service._logger.level == 10  # logging.DEBUG
