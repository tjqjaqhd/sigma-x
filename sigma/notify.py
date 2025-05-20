from loguru import logger
from slack_sdk import WebClient

from .config import SLACK_TOKEN, SLACK_CHANNEL

client = WebClient(token=SLACK_TOKEN) if SLACK_TOKEN else None


def send_message(text: str) -> None:
    """Slack으로 메시지 전송"""
    logger.info(text)
    if client and SLACK_CHANNEL:
        try:
            client.chat_postMessage(channel=SLACK_CHANNEL, text=text)
        except Exception as e:
            logger.error(f"Slack 전송 실패: {e}")
