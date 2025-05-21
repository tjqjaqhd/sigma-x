# sigma/plugins plugin structure and development guide

## 목차
1. 목적
2. 플러그인 구조
3. 표준 인터페이스
4. 등록/실행 방식
5. 유틸리티 활용
6. 확장/적용 가이드
7. 참고

## 1. 목적
- sigma 시스템의 플러그인 확장 구조와 개발 표준을 정의한다.

## 2. 플러그인 구조
- 모든 플러그인은 `PluginBase` 클래스를 상속받아야 한다.
- sigma/plugins/ 폴더에 .py 파일로 추가한다.

## 3. 표준 인터페이스
- 필수 메서드:
    - `on_load(self)`: 플러그인 로드 시 실행
    - `on_event(self, event: str, **kwargs)`: 이벤트 발생 시 실행
- 예시:
```python
from sigma.plugins.plugin_base import PluginBase
class MyPlugin(PluginBase):
    name = "my_plugin"
    def on_load(self):
        ...
    def on_event(self, event: str, **kwargs):
        ...
```

## 4. 등록/실행 방식
- 시스템 초기화 시 자동으로 로드 및 on_load() 실행
- 이벤트 발생 시 on_event() 호출 가능

## 5. 유틸리티 활용
- 플러그인 내에서 `SlackNotifier` 등 sigma 유틸리티 자유롭게 활용 가능

## 6. 확장/적용 가이드
- 신규 플러그인 개발 시 반드시 PluginBase 상속
- 실전 적용 시 on_load, on_event 활용하여 외부 서비스 연동, 알림, 데이터 처리 등 구현

## 7. 참고
- 플러그인 로더 및 연동 구조는 [plugin_loader.md](plugin_loader.md) 참고 