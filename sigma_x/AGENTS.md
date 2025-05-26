```markdown
# AGENT for src

## 목적
자동매매 핵심 로직(시세 수집·전략·주문 실행·API 서버)을 담은 디렉터리입니다.

## 테스트 규칙
- 외부 WS/HTTP 요청은 `aioresponses`·`patch` 로 **모의**  
- Redis·RabbitMQ 는 `fakeredis`·`fakerabbitmq` 사용  
- 모든 루프에 `limit` 또는 `asyncio.wait_for`로 **자동 종료**  
- 테스트 동안 실 DB·실 거래소·네트워크 접근 **금지**

## 테스트 스타일
- `pytest-asyncio` 사용, 함수마다 `@pytest.mark.asyncio`  
- **단일 기능 검증**(Arrange-Act-Assert) & 한 테스트당 1 assert 권장  
- 통합 테스트는 `asyncio.gather` 로 다중 컴포넌트 연결 후 결과 확인

## 예시 도구
```python
@pytest.mark.asyncio
async def test_data_collector_with_fake_ws(aioresponses):
    from src.data_collector import DataCollector
    mock_ws = FakeWebSocket(messages=[{"price": 1}]*3)
    col = DataCollector(websocket=mock_ws)
    await col.run(limit=3)
    assert col.collected_count == 3
-변경사항이 있으면 알맞게 고치세요
