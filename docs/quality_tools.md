# Snyk CLI 사용법

이 문서는 Snyk CLI를 활용하여 의존성 보안 취약점을 진단하는 방법을 설명합니다.

## 설치
```bash
npm install -g snyk
```

## 로그인
Snyk 계정이 없다면 [Snyk 웹사이트](https://snyk.io)에서 가입 후 토큰을 발급받습니다.
```bash
snyk auth <발급받은_토큰>
```

## 취약점 검사
프로젝트 루트에서 다음 명령을 실행합니다.
```bash
snyk test
```

## 모니터링
CI 파이프라인에 정기 분석을 추가하려면 다음 명령을 사용합니다.
```bash
snyk monitor
```

이후 Snyk 대시보드에서 프로젝트 상태를 확인할 수 있습니다.
