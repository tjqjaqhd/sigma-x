# SIGMA VPS 서버 사양

이 문서는 SIGMA 자동매매 시스템이 운영되는 VPS의 기본 사양을 정의합니다. 환경 변수로 값을 재정의할 수 있으며, 기본값은 코드의 `DEFAULT_SPEC`에 명시되어 있습니다.

| 항목 | 기본값 |
| --- | --- |
| 플랫폼 | Naver Cloud Platform (VPC 환경) |
| 서버 이름 | sigma (ID: 105080454) |
| 공인 IP | 223.130.139.218 |
| 비공인 IP | 10.0.1.6 |
| 이미지 | Ubuntu 24.04 LTS (ubuntu-24.04-base) |
| 서버 사양 | s4-g3 (vCPU 4개 / 메모리 16GB) |
| 스토리지 | 100GB SSD(`/dev/vda`) |
| 하이퍼바이저 | KVM |
| 서버 상태 | 운영 중 |
| 생성일시 | 2025-05-12 16:32 (KST) |
| 구동일시 | 2025-05-19 19:57 (KST) |
| VPC 이름 | sigma-vpc |
| Subnet | public-subnet1 (KR-1) |

환경 변수 `SIGMA_PLATFORM` 등으로 각 값을 변경하여 사용할 수 있습니다.
