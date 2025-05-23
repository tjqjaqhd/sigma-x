from sigma.core.commentary_module import CommentaryModule


class DummyRepo:
    def __init__(self):
        self.saved = None

    def save_commentary(self, text):
        self.saved = text


def test_generate_commentary(monkeypatch):
    repo = DummyRepo()
    logs = []

    class DummyLogger:
        def debug(self, msg, *args):
            logs.append(msg % args if args else msg)

    cm = CommentaryModule(repository=repo, logger=DummyLogger())
    summary = {"trades": 5, "pnl": 123.45}
    text = cm.generate(summary)
    assert text == "이번 기간 거래 5건, 수익 123.45"
    assert repo.saved == text
    assert any("코멘터리 생성" in log for log in logs)
