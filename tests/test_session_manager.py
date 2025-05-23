from sigma.common.session_manager import SessionManager


def test_session_manager_init():
    sm = SessionManager()
    assert hasattr(sm, "positions")
