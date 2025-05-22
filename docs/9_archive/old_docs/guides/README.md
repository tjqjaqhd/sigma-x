# Sigma 시스템 가이드라인

이 문서는 sigma 프로젝트의 사용자 및 개발자, 운영자를 위한 공식 가이드라인이다.

## 목차
- [설치 및 환경설정](../setup/)
- [아키텍처 개요](../architecture/architecture_summary.md)
- [요구사항 및 사양서](../requirements/)
- [구조 개편 지침](../structure_refactor_instruction.md)
- [플러그인 개발 가이드](../requirements/plugins/plugins.md)
- [운영 및 유지보수](#운영-및-유지보수)
- [문서 관리 및 작성 규칙](#문서-관리-및-작성-규칙)

---

## 운영 및 유지보수
- 시스템 설정은 DB(SystemConfig) 기반으로 관리
- 실시간 데이터: WebSocket→Redis Pub/Sub 구조
- 주문 파이프라인: RabbitMQ 기반
- 알림: NotificationService 일원화
- 시뮬레이션/실거래 모드 통합 관리
- 테스트/운영 환경 분리, 로그/임시파일 커밋 금지

## 문서 관리 및 작성 규칙
- 모든 문서는 목적별로 docs/requirements, docs/architecture, docs/guides 등으로 분류
- 존재하지 않는 문서 참조/링크 금지, 실제 파일만 연결
- 미구현 항목은 반드시 "TODO:" 형식으로 작성
- 용어는 시스템 전체에서 일관되게 사용(예: 알림(notification), 주문(order), 시뮬레이션(simulation) 등)
- 문서/코드/운영환경 변경 시 반드시 관련 문서 동기화

---

> 최신 가이드라인은 본 README와 각 하위 문서를 참고할 것. 추가 문의/기여는 프로젝트 관리자에게 문의.
