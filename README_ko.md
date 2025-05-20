# Sigma 서버 개요

이 문서는 Naver Cloud Platform에서 동작 중인 sigma VPS 서버의 기본 정보를 요약합니다. 또한 PR(풀 리퀘스트)이 제대로 동작하지 않을 때 확인해야 할 사항들을 정리합니다.

## 서버 정보

- 플랫폼: Naver Cloud Platform (VPC 환경)
- 서버 이름: sigma (ID: 105080454)
- 공인 IP: 223.130.139.218
- 비공인 IP: 10.0.1.6
- 이미지: Ubuntu 24.04 LTS (ubuntu-24.04-base)
- 서버 사양: s4-g3 (vCPU 4개 / 메모리 16GB)
- 스토리지: 100GB SSD(`/dev/vda`)
- 하이퍼바이저: KVM
- 서버 상태: 운영 중
- 생성일시: 2025-05-12 16:32 (KST)
- 구동일시: 2025-05-19 19:57 (KST)
- VPC 이름: sigma-vpc
- Subnet: public-subnet1 (KR-1)

## PR이 안 될 때 확인할 점

1. 원격 저장소가 설정되어 있는지 확인합니다.
   ```bash
   git remote -v
   ```
   출력이 없거나 오류가 발생하면 다음과 같이 원격 저장소를 추가합니다.
   ```bash
   git remote add origin <원격_저장소_URL>
   ```

2. 변경 사항을 커밋했는지 확인합니다.
   ```bash
   git status
   ```
   만약 커밋할 파일이 있다면 다음과 같이 커밋합니다.
   ```bash
   git add <파일들>
   git commit -m "커밋 메시지"
   ```

3. 푸시 권한이 있는지 확인합니다. 권한이 없다면 토큰이나 SSH 키 설정을 점검해야 합니다.

4. 위 사항이 모두 정상이라면 브랜치를 푸시하고 PR을 생성합니다.
   ```bash
   git push origin <브랜치명>
   ```

PR 생성 시 문제가 계속 발생한다면 구체적인 오류 메시지나 로그를 확인해 보는 것이 좋습니다.
