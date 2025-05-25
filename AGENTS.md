- 1.사용자의 기본 지시를 최대한 따라주세요
- 2.########################################
# 1) Python 개발환경 설치 (운영 + 개발)
########################################
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

########################################
# 2) 시스템 도구 설치 (AI 보조 개발환경 최적화)
########################################
sudo apt update && sudo apt install -y \
  xxd binutils diffutils procps file colordiff dhex \
  time htop iotop strace zip unzip p7zip-full \
  jq yq binwalk tree shellcheck python3-magic hyperfine \
  lsof ncdu net-tools gdb entr ripgrep fd-find fzf \
  bat btop duf git curl wget openssh-client

# fdfind → 'fd'로 symlink (Ubuntu만 해당)
[ -x /usr/bin/fdfind ] && sudo ln -sf $(which fdfind) ~/.local/bin/fd

########################################
# 3) Node/NPM 기반 문서 도구 설치
########################################
sudo apt install -y nodejs npm
sudo npm install -g markdownlint-cli jsonlint prettier
sudo npm install -g @mermaid-js/mermaid-cli
sudo apt install -y graphviz

########################################
# 4) 선택적 개발 도구 (권장)
########################################
pip install pyright
npm install -g pyright # 타입 검사용 (JS/Python 모두 대응)

########################################
# 5) poetry 기반 프로젝트 (사용 시)
########################################
# pip install poetry
# poetry install --with dev,test

이러한 도구들을 설치해뒀으니 사용하세요
- 3.pre-commit 와 ci는 현제 상황에 맞게 수정하세요
- 4.파일이나 문서를 수정하면 항상 연관문서들을 최신으로 업데이트 하세요
- 5.추가로 앞으로 작업에 필요하고 유용한 의존성이 있다면requirements.txt에 추가하세요
- 6.`docs/scripts/gen_diagrams.sh` 스크립트로 모든 다이어그램을 갱신하세요
