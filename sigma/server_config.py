from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass
class ServerSpec:
    """서버 스펙 정보를 저장합니다."""

    platform: str
    server_name: str
    public_ip: str
    private_ip: str
    image: str
    spec: str
    storage: str
    hypervisor: str
    status: str
    created_at: str
    started_at: str
    vpc_name: str
    subnet: str


DEFAULT_SPEC = ServerSpec(
    platform="Naver Cloud Platform (VPC 환경)",
    server_name="sigma (ID: 105080454)",
    public_ip="223.130.139.218",
    private_ip="10.0.1.6",
    image="Ubuntu 24.04 LTS (ubuntu-24.04-base)",
    spec="s4-g3 (vCPU 4개 / 메모리 16GB)",
    storage="100GB SSD (/dev/vda)",
    hypervisor="KVM",
    status="운영 중",
    created_at="2025-05-12 16:32 (KST)",
    started_at="2025-05-19 19:57 (KST)",
    vpc_name="sigma-vpc",
    subnet="public-subnet1 (KR-1)",
)


def load_server_spec() -> ServerSpec:
    """환경 변수에서 서버 스펙을 로드하고 없으면 기본값을 사용합니다."""

    return ServerSpec(
        platform=os.getenv("SIGMA_PLATFORM", DEFAULT_SPEC.platform),
        server_name=os.getenv("SIGMA_SERVER_NAME", DEFAULT_SPEC.server_name),
        public_ip=os.getenv("SIGMA_PUBLIC_IP", DEFAULT_SPEC.public_ip),
        private_ip=os.getenv("SIGMA_PRIVATE_IP", DEFAULT_SPEC.private_ip),
        image=os.getenv("SIGMA_IMAGE", DEFAULT_SPEC.image),
        spec=os.getenv("SIGMA_SPEC", DEFAULT_SPEC.spec),
        storage=os.getenv("SIGMA_STORAGE", DEFAULT_SPEC.storage),
        hypervisor=os.getenv("SIGMA_HYPERVISOR", DEFAULT_SPEC.hypervisor),
        status=os.getenv("SIGMA_STATUS", DEFAULT_SPEC.status),
        created_at=os.getenv("SIGMA_CREATED_AT", DEFAULT_SPEC.created_at),
        started_at=os.getenv("SIGMA_STARTED_AT", DEFAULT_SPEC.started_at),
        vpc_name=os.getenv("SIGMA_VPC_NAME", DEFAULT_SPEC.vpc_name),
        subnet=os.getenv("SIGMA_SUBNET", DEFAULT_SPEC.subnet),
    )


__all__ = ["ServerSpec", "load_server_spec", "DEFAULT_SPEC"]
