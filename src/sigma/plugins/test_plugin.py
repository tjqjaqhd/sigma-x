from src.sigma.plugins.plugin_base import PluginBase
from src.sigma.system.notification_service import notify


class TestPlugin(PluginBase):
    name = "test"

    def on_load(self):
        notify("INFO", "[TestPlugin] 플러그인 로드됨")

    def on_event(self, event: str, **kwargs):
        notify("INFO", f"[TestPlugin] 이벤트 발생: {event}, 데이터: {kwargs}")
