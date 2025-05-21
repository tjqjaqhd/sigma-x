from abc import ABC, abstractmethod


class PluginBase(ABC):
    """플러그인 표준 인터페이스. 모든 플러그인은 이 클래스를 상속받아야 한다."""

    name: str = "base"

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    def on_load(self):
        """플러그인 로드 시 실행되는 메서드."""
        pass

    def on_event(self, event: str, **kwargs):
        """이벤트 발생 시 실행되는 메서드."""
        pass
