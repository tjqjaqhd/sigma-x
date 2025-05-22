# Module\_Specification\_and\_Plugin\_Documentation\_Maintenance

이 문서는 모듈 사양서와 플러그인 개발 문서의 정확성과 최신성을 유지하기 위한 지침을 제공합니다.

---

## 1. 모듈 사양서 Placeholder 제거

모든 모듈 사양서의 메타 정보(작성일, 최종 수정일 등)는 Placeholder 대신 실제 값을 정확히 명시하여 유지해야 합니다.

### 예시

* 올바른 예:

  ```markdown
  <!--
  Author: 홍길동
  Created Date: 2024-06-10
  Last Modified: 2024-06-20
  Version: 1.0
  -->
  ```

* 잘못된 예:

  ```markdown
  <!--
  Author: 홍길동
  Created Date: 2024-06-XX
  Last Modified: 2024-XX-XX
  Version: X.X
  -->
  ```

---

## 2. 플러그인 개발 문서 실제 예제 추가

플러그인 개발 가이드 문서에 PluginBase를 상속받아 구현한 실제 플러그인 예시 코드와 활용 방법을 반드시 포함해야 합니다.

### 예시

```python
from sigma.plugins import PluginBase

class ExamplePlugin(PluginBase):
    def on_event(self, event):
        if event.type == 'order_filled':
            self.handle_order_filled(event)

    def handle_order_filled(self, event):
        print(f"Order filled: {event.details}")
```

---

## 3. 내부 링크 점검 및 유지

모든 문서 간의 내부 링크는 정확한 상대 경로를 사용하여 항상 점검하고 최신 상태로 유지합니다.

### 올바른 링크 예시

```markdown
[플러그인 로더 모듈 사양서](../system/plugin_loader.md)
```

---

## 4. 모듈 사양서 인덱스 표 유지 관리

사양서 인덱스는 정확한 모듈별 문서 경로를 항상 반영하며, 표의 형식 오류나 누락된 링크는 즉시 수정합니다.

### 예시

| 모듈 경로                  | 문서 링크                                |
| ---------------------- | ------------------------------------ |
| sigma/core/bot.py      | [core/bot.md](core/bot.md)           |
| sigma/web/dashboard.py | [web/dashboard.md](web/dashboard.md) |

---

이 지침을 통해 모듈 및 플러그인 관련 문서의 품질과 정확성을 유지하고, 개발자가 명확하게 정보를 활용할 수 있도록 관리해 주시기 바랍니다.
