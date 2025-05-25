# 운영 매뉴얼

시스템 모니터링과 장애 대응 절차를 정리한 문서입니다.

## 1. 모니터링
- `htop` 또는 `btop`을 사용해 CPU와 메모리 사용량을 실시간으로 확인합니다.
- 로그 파일을 주기적으로 점검해 오류 여부를 확인합니다.

## 2. 장애 대응 절차
1. 서비스 상태 확인
   ```bash
   docker compose ps
   ```
2. 이상이 있는 컨테이너 재시작
   ```bash
   docker compose restart api
   ```
3. Redis 장애 시 데이터 백업본으로 복구합니다.

## 3. 백업 정책
- `sigma_system.yaml` 등 주요 설정 파일을 주기적으로 백업합니다.
- Redis의 `dump.rdb` 파일을 안전한 위치에 보관합니다.

시스템 전반 구조는 다음 다이어그램을 참고하십시오.

![시스템 다이어그램](sigma_system_diagram.svg)
