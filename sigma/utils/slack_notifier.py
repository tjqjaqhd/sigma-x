from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from sigma.config_loader import load_db_config

from sigma.utils.logger import logger

config = load_db_config()
SLACK_TOKEN = config.get("SLACK_TOKEN")
SLACK_CHANNEL = config.get("SLACK_CHANNEL")


class SlackNotifier:
    """Slack 채널로 메시지를 전송하는 유틸리티."""

    def __init__(self, token: str = SLACK_TOKEN, channel: str = SLACK_CHANNEL) -> None:
        self.client = WebClient(token=token)
        self.channel = channel

    def send_message(self, text: str) -> None:
        if not self.channel:
            logger.warning("Slack channel not configured")
            return
        try:
            self.client.chat_postMessage(channel=self.channel, text=text)
        except SlackApiError as exc:  # pragma: no cover - network call
            logger.error(f"Slack API error: {exc.response['error']}")
