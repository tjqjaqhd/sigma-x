# SIGMA 모듈 사양서

이 문서는 SIGMA 프로젝트의 각 모듈을 명확히 기록하기 위한 문서입니다. 모든 항목은 누락 없이 작성하며, 해당 사항이 없을 경우 **해당 없음**으로 표기합니다.

## 1. 모듈 개요
* 모듈명: FastAPI_InitApp
* 작성자: TBD
* 작성일: 2025-05-23
* 최종 검토자: TBD
* 최종 수정일: 2025-05-23

FastAPI 애플리케이션을 생성하고 모든 라우터와 미들웨어를 등록한다. 설정에 따라
문서화 옵션과 인증 미들웨어를 활성화하며, `uvicorn` 실행 전에 호출된다.

## 2. 구조 개요
* 포함된 함수: `init_app`, `register_routes`
* 주요 메서드: `init_app(config: Config) -> FastAPI`
* 외부 API 제공 여부: FastAPI 인스턴스 반환
* 소스 파일 위치: `sigma/interfaces/fastapi_app.py`

## 3. 인터페이스 명세
### 3.1 입력
* 입력 유형: 설정 객체
* 형식 및 구조: `Config` 인스턴스
* 제약 조건: DB 접속 정보 및 토큰 필수

### 3.2 출력
* 출력 유형: `FastAPI` 객체
* 형식 및 구조: FastAPI 인스턴스
* 반환 조건: 라우터 등록 완료 시

## 4. 내부 처리 로직
1. 설정을 기반으로 FastAPI 생성
2. 공통 미들웨어(로그, CORS) 등록
3. REST 및 WebSocket 라우터 추가
4. 이벤트 핸들러(on_startup)에서 Redis 연결 준비

## 5. 예외 처리
* 설정 누락 → `ValueError` 발생 후 애플리케이션 중단
* 라우터 등록 중 오류 → 로그 기록 후 예외 전파

## 6. 연관 모듈 및 외부 시스템
* 상위 호출자: run_bot.py 초기화 단계
* 하위 호출 대상: DashboardAPI, WebSocket_Endpoint
* 연계되는 DB/캐시/메시지큐: Redis, PostgreSQL
* 타 모듈 간 의존 관계: metrics.py, logging_service 사용

## 7. 리소스 및 성능
### 7.1 리소스 소비
* CPU 예상 사용량: 무시할 수준
* 메모리 예상 사용량: 100MB 이하

### 7.2 성능 기준
* 초기화 시간: 1초 이하
* 요청 처리 지연: FastAPI 기본 성능 준수

## 8. 설정 및 의존성
* 환경 변수: `API_DOCS=on|off`
* 의존성: `fastapi`, `uvicorn`

## 9. 테스트 및 검증
* 단위 테스트 항목: 라우터 등록 결과, 미들웨어 작동 여부
* 통합 테스트 체크리스트: WebSocket 및 REST 엔드포인트 호출
* 테스트 커버리지 목표: 80% 이상

## 10. 제약사항 및 향후 계획
* 향후 개선: 모듈별 라우터 자동 로드 기능
