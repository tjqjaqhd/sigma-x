from sigma.common.notification_service import NotificationService


def test_notification_service_init():
    ns = NotificationService()
    assert hasattr(ns, "send")
