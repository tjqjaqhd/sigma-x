# system.plugin_loader 모듈 사양

## 목차
1. 목적
2. 구조 및 역할
3. 주요 함수/객체
4. 동작 방식
5. 참고

## 1. 목적
- 플러그인 자동 로드, 등록, 실행을 담당하는 시스템 모듈의 사양 정의

## 2. 구조 및 역할
- plugins/ 폴더 내 PluginBase 상속 플러그인을 동적으로 로드
- on_load() 자동 실행, run_all_plugins()로 일괄 실행 지원

## 3. 주요 함수/객체
| 객체/함수 | 설명 |
|-----------|------|
| `load_plugins(directory="plugins")` | plugins 폴더 내 PluginBase 상속 플러그인을 동적으로 불러오고, on_load()를 실행 |
| `run_all_plugins(*args, **kwargs)` | 등록된 모든 플러그인의 run 메서드를 실행 |
| `plugins` | 등록된 플러그인 인스턴스 리스트 |

## 4. 동작 방식
- 플러그인은 반드시 PluginBase를 상속해야 하며, run 메서드를 구현해야 함
- 시스템 초기화 시 load_plugins() 호출로 자동 로드 및 on_load() 실행
- run_all_plugins()로 일괄 실행 가능

## 5. 참고
- 플러그인 개발/확장 표준은 [plugins.md](plugins.md) 참고
