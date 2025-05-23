from sigma.common.event_loop import EventLoop


def test_event_loop_init():
    el = EventLoop()
    assert hasattr(el, "run")
