from sigma import (
    load_env,
    load_db_config,
    load_plugins,
    init_metrics,
    load_user_preferences,
    check_system_health,
    init_cache,
    configure_additional_services,
    init_notification,
    init_api,
    start_event_loop,
    init_session,
    init_logging,
)


def test_init_modules():
    load_env()
    assert "url" in load_db_config()
    assert load_plugins() == ["core"]
    metrics = init_metrics()
    metrics.inc("a")
    assert metrics.data["a"] == 1
    assert load_user_preferences()["lang"] == "ko"
    assert check_system_health() is True
    assert isinstance(init_cache(), dict)
    configure_additional_services()
    assert init_notification().active
    assert init_api().routes
    start_event_loop()
    assert isinstance(init_session(), object)
    init_logging()
