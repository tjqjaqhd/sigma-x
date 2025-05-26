from __future__ import annotations


class OrderHandler:
    """주어진 신호를 실제 주문으로 실행하는 역할."""

    def __init__(self, api_client, db_session, redis_client):
        self.api_client = api_client
        self.db_session = db_session
        self.redis_client = redis_client

    def execute_order(self, signal, amount):
        """주문 실행 로직."""
        # 거래소 API 호출
        response = self.api_client.place_order(signal, amount)

        # 결과 반환
        return response
