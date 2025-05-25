- 1.사용자의 기본 지시를 최대한 따라주세요
- 2.########################################
# 1) Python 가상환경 + requirements 설치
########################################
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

########################################
# 2) 시스템 도구 설치 (필요한 것만)
########################################
sudo apt update && sudo apt install -y \
  xxd binutils diffutils procps colordiff dhex \
  htop iotop strace unzip p7zip-full jq yq binwalk tree \
  shellcheck python3-magic hyperfine lsof ncdu net-tools gdb entr \
  ripgrep fd-find fzf bat btop duf

# fd 심볼릭 링크 (Ubuntu용)
[ -x /usr/bin/fdfind ] && mkdir -p ~/.local/bin && ln -sf $(which fdfind) ~/.local/bin/fd

########################################
# 3) 문서 도구만 NPM 설치 (node/npm 이미 있으므로 OK)
########################################
sudo npm install -g markdownlint-cli jsonlint prettier
sudo npm install -g @mermaid-js/mermaid-cli
sudo apt install -y graphviz

이러한 도구들을 설치해뒀으니 사용하세요
- 3.pre-commit 와 ci는 현제 상황에 맞게 수정하세요
- 4.파일이나 문서를 수정하면 항상 연관문서들을 최신으로 업데이트 하세요
- 5.추가로 앞으로 작업에 필요하고 유용한 의존성이 있다면requirements.txt에 추가하세요
- 6.`docs/scripts/gen_diagrams.sh` 스크립트로 모든 다이어그램을 갱신하세요
  루트 디렉터리에서 아래 명령을 실행하면 `.mmd`와 `.dot` 파일이 모두 SVG로 변환됩니다.
  ```bash
  bash docs/scripts/gen_diagrams.sh
  ```
  CI에서도 이 스크립트가 자동으로 실행되므로 문서 수정 후 반드시 실행 결과를 커밋하세요.
