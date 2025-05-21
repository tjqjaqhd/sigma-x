from sigma.plugins.plugin_base import PluginBase
from sigma.utils.slack_notifier import SlackNotifier


class TestPlugin(PluginBase):
    name = "test"

    def on_load(self):
        notifier = SlackNotifier()
        notifier.send_message("[TestPlugin] 플러그인 로드됨")

    def on_event(self, event: str, **kwargs):
        notifier = SlackNotifier()
        notifier.send_message(f"[TestPlugin] 이벤트 발생: {event}, 데이터: {kwargs}")
