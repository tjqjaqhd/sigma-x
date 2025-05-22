# data.models 모듈 사양

## 1. 모듈 개요

* 모듈명: data.models
* 작성자: AI 자동화
* 작성일: 2024-06-XX
* 최종 검토자: AI 자동화
* 최종 수정일: 2024-06-XX

**설명:**
시장 데이터, 시스템 설정, 전략 파라미터, 주문, 포지션, 알림 등 트레이딩 시스템의 모든 핵심 엔터티를 SQLAlchemy ORM 모델로 정의하는 모듈.

## 2. 구조 개요

* 포함된 클래스:
  - MarketData: 시장 데이터 테이블
  - SystemConfig: 시스템 설정 테이블
  - StrategyParam: 전략 파라미터 테이블
  - Order: 주문 정보 테이블
  - Position: 포지션 상태 테이블
  - Alert: 알림 메시지 테이블
* 주요 함수/메서드 목록:
  - 각 클래스: SQLAlchemy ORM 표준 생성자/속성
* 외부 API 제공 여부: 해당 없음

## 3. 인터페이스 명세

### 3.1. 입력 (Input)
* 입력 유형: 각 엔터티별 속성값(dict)
* 형식 및 구조: 예) {"symbol": str, "price": float, ...}
* 제약 조건: PK/필수값 존재, 타입 일치
* 예시: {"symbol": "BTC", "price": 100.0}

### 3.2. 출력 (Output)
* 출력 유형: ORM 인스턴스, DB row
* 형식 및 구조: MarketData, SystemConfig 등 ORM 객체
* 예시: MarketData(symbol="BTC", price=100.0)
* 반환 조건: DB 조회/생성/수정/삭제 시

### 3.3. API 엔드포인트 (해당 시)
* URL: 해당 없음
* Method: 해당 없음
* 인증: 해당 없음
* 설명: 해당 없음
* 요청/응답 예시: 해당 없음

## 4. 내부 처리 로직
* 처리 흐름 요약:
  1. 각 클래스는 Base를 상속받아 __tablename__ 및 컬럼 정의
  2. SQLAlchemy의 표준 ORM 매핑 사용
* 순서도/플로우차트: 해당 없음
* 알고리즘 요약: SQLAlchemy ORM 표준 매핑

## 5. 예외 처리
* 주요 예외 유형: 해당 없음(내부적으로 DB 제약조건 위반 등 가능)
* 발생 조건: PK 중복, 타입 불일치 등
* 대응 방식: SQLAlchemy 예외 발생
* 로깅/알림: 해당 없음

## 6. 연관 모듈 및 외부 시스템
* 상위 호출자: core/adaptation, core/execution, data/collector 등
* 하위 호출 대상: db/database
* 연계되는 DB/캐시/메시지큐: market_data, system_config, strategy_param, orders, positions, alert(일반 알림만) 테이블
* 타 모듈 간 의존 관계: db/database

## 7. 리소스 및 성능
### 7.1. 리소스 소비
* CPU 예상 사용량: 매우 낮음(ORM 매핑)
* 메모리 예상 사용량: 매우 낮음
* 병렬성 또는 멀티스레딩 여부: 해당 없음
### 7.2. 성능 기준
* 처리량 기준 (TPS/건수): DB 트랜잭션 빈도에 따라 다름
* 응답 시간: 매우 짧음
* 지연 허용 한계: 해당 없음
* 초기화 시간: 매우 짧음

## 8. 설정 및 의존성
* 사용하는 DB 테이블 및 필드: market_data, system_config, strategy_param, orders, positions, alert
* 설정값 및 기본값: 해당 없음
* 외부 환경 변수: 해당 없음
* 사용하는 서드파티/외부 API: SQLAlchemy

## 9. 테스트 및 검증
* 단위 테스트 항목: 각 모델 생성/조회/수정/삭제 정상 동작
* 예외 테스트 항목: PK 중복, 타입 불일치 등
* 통합 테스트 체크리스트: 전체 DB 연동 모듈과 통합
* 테스트 커버리지 목표: 90% 이상

## 10. 제약사항 및 향후 계획
* 현재 한계: 관계형 제약조건/인덱스 최소화
* 기술적 부채: 단순 테이블 구조, 외래키 미사용
* 향후 개선/확장 예정 사항: 관계/인덱스 강화, 스키마 확장
* 폐지 예정 요소: 해당 없음

| 객체 | 설명 |
|------|------|
| `MarketData` | 시장 데이터를 저장하는 테이블 |
| `SystemConfig` | 시스템 설정을 저장하는 테이블 |
| `StrategyParam` | 전략 파라미터를 저장하는 테이블 |
| `Order` | 주문 정보를 저장하는 테이블 |
| `Position` | 포지션 상태를 저장하는 테이블 |
| `Alert` | 알림 메시지를 저장하는 테이블 |

