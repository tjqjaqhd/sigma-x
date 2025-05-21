# 실행 모드 및 알림 체계 통일(Simulation & Notification) 지시 문서

## 1. 개요

SIGMA 시스템에서 시뮬레이션 처리 및 알림 시스템의 설계와 코드가 불일치하여 혼란을 일으키고 있습니다. 현재 별도 SimRunner 클래스가 문서에만 존재하며, NotificationService를 통한 알림 채널 확장이 제한적으로만 구현되어 있습니다.

## 2. 목표 상태

* 별도 SimRunner 컴포넌트를 제거하고, is\_simulation 플래그를 이용한 통일된 시뮬레이션 모드 구현
* NotificationService를 통해 Slack, 이메일 등 다양한 채널로의 알림 발송이 가능하도록 구조 정비
* "알림", "경고", "Alert" 등 혼용 용어의 통일 및 명확화

## 3. 작업 항목

| 우선순위   | 작업 내용                                                                       | 담당       | 예상 기간 |
| ------ | --------------------------------------------------------------------------- | -------- | ----- |
| HIGH   | SimRunner 관련 모든 문서 및 코드 제거하고, OrderExecutor 내 is\_simulation 플래그로 처리 방식 통합  | AI Agent | 1일    |
| HIGH   | NotificationService의 notify(level, message) 단일 인터페이스 구현 및 SlackNotifier를 통합 | AI Agent | 1일    |
| MEDIUM | EmailNotifier 기본 구조 마련 및 향후 확장 가능하도록 설계 준비                                  | AI Agent | 1일    |
| MEDIUM | 알림 관련 용어를 "알림(notification)"으로 문서 및 코드 전반에 걸쳐 통일화                           | AI Agent | 0.5일  |
| LOW    | 시뮬레이션 모드와 관련된 문서 및 예시를 명확히 업데이트하여 신규 개발자 혼란 방지                              | AI Agent | 0.5일  |

## 4. 체크리스트

* [ ] SimRunner의 흔적이 코드 및 문서에서 완전히 제거됨을 확인
* [ ] is\_simulation 플래그를 통한 모의 체결이 정상 작동함을 확인
* [ ] NotificationService가 Slack 및 향후 이메일 등 다중 채널을 지원할 수 있도록 준비됨을 확인
* [ ] 코드 및 문서의 모든 알림 관련 용어가 "알림(notification)"으로 일관되게 사용됨을 확인

## 5. 참고

* 이메일 발송은 SMTP 설정을 기준으로 하며, 실제 발송 로직은 향후 구현 예정
* NotificationService 구조는 플러그인 방식으로 설계하여 채널 확장을 용이하게 할 것
