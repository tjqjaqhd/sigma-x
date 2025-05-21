from sigma.utils.notification_service import NotificationService
from sigma.utils.slack_notifier import SlackNotifier


def test_notification_service(monkeypatch):
    sent: list[str] = []
    monkeypatch.setattr(SlackNotifier, "send_message", lambda self, text: sent.append(text))
    service = NotificationService()
    service.notify("hello")
    assert sent == ["[INFO] hello"]
