# 배포 뷰 및 NFR

본 시스템은 다음과 같은 NFR(비기능 요구사항)을 충족하도록 설계되었습니다.

- **신뢰성**: 단일 VPS에서 모든 서비스가 동작하므로 서비스 모니터링과 장애 복구가 중요합니다.
- **보안성**: 외부 접근을 최소화하고 필요 시 VPN 또는 방화벽 정책을 적용합니다.
- **유지보수성**: 컨테이너 기반 배포를 통해 서비스의 버전 관리와 롤백을 쉽게 수행합니다.

## 배포 구성 다이어그램

```mermaid
deploymentDiagram
    node "Naver Cloud VPC" {
        node "sigma (Ubuntu 24.04, 4 vCPU, 16GB RAM)" {
            component "data_collector" as DC
            component "trade_executor" as TE
            database "redis" as Redis
            queue "rabbitmq" as MQ
        }
    }
    DC --> Redis
    TE --> Redis
    DC --> MQ
    TE --> MQ
```

## 서버 사양

* **플랫폼**: Naver Cloud Platform (VPC 환경)
* **서버 이름**: sigma (ID: 105080454)
* **공인 IP**: 223.130.139.218
* **비공인 IP**: 10.0.1.6
* **이미지**: Ubuntu 24.04 LTS (ubuntu-24.04-base)
* **서버 사양**: s4-g3 (vCPU 4개 / 메모리 16GB)
* **스토리지**: 100GB SSD(`/dev/vda`)
* **하이퍼바이저**: KVM
* **서버 상태**: 운영 중
* **생성일시**: 2025-05-12 16:32 (KST)
* **구동일시**: 2025-05-19 19:57 (KST)
* **VPC 이름**: sigma-vpc
* **Subnet**: public-subnet1 (KR-1)

해당 서버는 위와 같은 사양으로 동작하며, 공인 IP를 통해 외부와 통신하고 VPC 내부에서는 비공인 IP를 사용합니다.
