# 🖥️ Desinsight 다른 PC 작업환경 세팅 가이드

## 📋 목차
1. [🎯 개요](#-개요)
2. [⚙️ 시스템 요구사항](#-시스템-요구사항)
3. [🐳 Docker 설치](#-docker-설치)
4. [📥 Desinsight 워크스페이스 설치](#-desinsight-워크스페이스-설치)
5. [🔧 개발 환경 세팅](#-개발-환경-세팅)
6. [🌐 네트워크 및 포트 설정](#-네트워크-및-포트-설정)
7. [📂 볼륨 마운트 설정](#-볼륨-마운트-설정)
8. [🛠️ 팀 워크플로우](#-팀-워크플로우)
9. [❓ 문제 해결](#-문제-해결)

---

## 🎯 개요

이 가이드는 **Desinsight 분산 RAG 시스템**을 다른 PC에서 빠르게 설치하고 작업환경을 구축하는 방법을 안내합니다.

### 🏗️ 시스템 구성
- **5개 디바이스**: HOME iMac i7 64GB, Mac Mini M2 Pro 32GB, Office iMac i7 40GB, Mac Studio M4 Pro 64GB, Mobile
- **3개 NAS**: SnapCodex NAS (192.168.219.175), Desinsight2 NAS, Office NAS
- **중앙 저장소**: Docker 이미지 및 설정 파일

---

## ⚙️ 시스템 요구사항

### 🖥️ 하드웨어 요구사항

| 구분 | 최소 사양 | 권장 사양 | 비고 |
|------|-----------|-----------|------|
| **CPU** | 2코어 | 4코어 이상 | Intel/AMD/Apple Silicon |
| **메모리** | 4GB | 8GB 이상 | Docker 컨테이너용 |
| **디스크** | 10GB | 50GB 이상 | SSD 권장 |
| **네트워크** | 1Mbps | 100Mbps 이상 | NAS 접근용 |

### 💻 지원 OS

| OS | 버전 | Docker 지원 |
|----|----- |------------|
| **macOS** | 10.15+ | ✅ Docker Desktop |
| **Windows** | 10/11 | ✅ Docker Desktop |
| **Ubuntu** | 18.04+ | ✅ Docker Engine |
| **CentOS** | 7+ | ✅ Docker Engine |

---

## 🐳 Docker 설치

### 🍎 macOS 설치

#### A. Homebrew 방식 (권장)
```bash
# 1. Homebrew 설치 (없는 경우)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Docker Desktop 설치
brew install --cask docker

# 3. Docker Desktop 실행
open /Applications/Docker.app

# 4. 설치 확인
docker --version
docker-compose --version
```

#### B. 직접 다운로드 방식
```bash
# 1. Docker Desktop 다운로드
curl -o Docker.dmg https://desktop.docker.com/mac/main/amd64/Docker.dmg

# 2. 설치 파일 실행
open Docker.dmg
# Applications 폴더로 드래그

# 3. Docker 실행 및 권한 허용
open /Applications/Docker.app
```

### 🪟 Windows 설치

#### A. 직접 다운로드 (권장)
```powershell
# 1. WSL2 설치 (Windows 10/11)
wsl --install

# 2. Docker Desktop 다운로드
# https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe

# 3. 설치 파일 실행
# Docker Desktop Installer.exe 더블클릭

# 4. 재부팅 후 Docker 실행

# 5. 설치 확인
docker --version
```

#### B. Chocolatey 방식
```powershell
# 1. Chocolatey 설치 (관리자 권한)
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# 2. Docker Desktop 설치
choco install docker-desktop

# 3. 재부팅
```

### 🐧 Linux (Ubuntu) 설치

```bash
# 1. 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# 2. 필수 패키지 설치
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# 3. Docker GPG 키 추가
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 4. Docker 저장소 추가
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Docker Engine 설치
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# 6. Docker Compose 설치
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 7. 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER

# 8. 재로그인 또는 재부팅

# 9. 설치 확인
docker --version
docker-compose --version
```

### 🔧 Docker 초기 설정

```bash
# 1. Docker 서비스 시작 (Linux)
sudo systemctl start docker
sudo systemctl enable docker

# 2. 설치 테스트
docker run hello-world

# 3. Docker 정보 확인
docker info
```

---

## 📥 Desinsight 워크스페이스 설치

### 🚀 자동 설치 (권장)

#### A. 원클릭 설치 스크립트
```bash
# 1. 설치 스크립트 다운로드
curl -O https://raw.githubusercontent.com/desinsight/workspace/main/load_workspace_from_nas.sh

# 2. 실행 권한 부여
chmod +x load_workspace_from_nas.sh

# 3. 자동 설치 실행
./load_workspace_from_nas.sh
```

#### B. Git 클론 방식
```bash
# 1. 저장소 클론
git clone https://github.com/desinsight/workspace.git
cd workspace

# 2. NAS에서 워크스페이스 로드
./load_workspace_from_nas.sh
```

### 🔧 수동 설치

#### Step 1: NAS 접근 설정
```bash
# 1. SSH 키 설정 (권장)
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
ssh-copy-id admin@192.168.219.175

# 2. 또는 비밀번호 방식으로 테스트
ssh admin@192.168.219.175
```

#### Step 2: 이미지 다운로드
```bash
# 1. 작업 디렉토리 생성
mkdir -p ~/desinsight && cd ~/desinsight

# 2. 최신 워크스페이스 이미지 확인
ssh admin@192.168.219.175 "ls -lt /volume1/docker-images/desinsight_workspace_*.tar | head -1"

# 3. 이미지 다운로드
scp admin@192.168.219.175:/volume1/docker-images/desinsight_workspace_YYYYMMDD_HHMMSS.tar .

# 4. 설정 파일 다운로드
scp admin@192.168.219.175:/volume1/docker-images/desinsight_configs_YYYYMMDD_HHMMSS.tar.gz .
```

#### Step 3: 이미지 로드 및 실행
```bash
# 1. Docker 이미지 로드
docker load -i desinsight_workspace_*.tar

# 2. 설정 파일 압축 해제
tar -xzf desinsight_configs_*.tar.gz
cd desinsight_configs_*/

# 3. 워크스페이스 실행
docker-compose -f docker-compose.workspace.yml up -d

# 4. 실행 확인
docker ps
```

---

## 🔧 개발 환경 세팅

### 🖥️ 기본 워크스페이스 설정

#### A. 프로덕션 모드
```bash
# 1. 기본 실행
docker-compose -f docker-compose.workspace.yml up -d

# 2. 상태 확인
docker-compose -f docker-compose.workspace.yml ps

# 3. 로그 확인
docker-compose -f docker-compose.workspace.yml logs -f
```

#### B. 개발 모드
```bash
# 1. 개발 모드 실행
docker-compose -f docker-compose.workspace.yml --profile development up -d

# 2. JupyterLab 접속
open http://localhost:8888

# 3. 개발 도구 확인
docker exec -it desinsight-dev bash
```

### 📝 IDE 및 편집기 연동

#### A. VS Code 연동
```bash
# 1. VS Code Docker 확장 설치
code --install-extension ms-vscode-remote.remote-containers

# 2. 컨테이너에 연결
# Ctrl+Shift+P → "Remote-Containers: Attach to Running Container"
# desinsight-workspace 선택

# 3. 워크스페이스 열기
# File → Open Folder → /workspace
```

#### B. JetBrains 연동 (PyCharm)
```bash
# 1. Docker 인터프리터 설정
# Settings → Project → Python Interpreter → Add
# Docker Compose 선택

# 2. Compose 파일 지정
# docker-compose.workspace.yml 선택

# 3. 서비스 선택
# desinsight-workspace 선택
```

#### C. JupyterLab 설정
```bash
# 1. JupyterLab 접속
open http://localhost:8888

# 2. 확장 프로그램 설치
jupyter labextension install @jupyterlab/git
jupyter labextension install @jupyterlab/github

# 3. 테마 설정
pip install jupyterlab_theme_dark
```

---

## 🌐 네트워크 및 포트 설정

### 🔗 포트 매핑 확인

```bash
# 1. 사용 중인 포트 확인
docker port desinsight-workspace

# 2. 포트 충돌 해결
sudo lsof -i :5000
# 충돌 시 docker-compose.yml에서 포트 변경
```

### 🛡️ 방화벽 설정

#### macOS 방화벽
```bash
# 1. 방화벽 상태 확인
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# 2. 포트 허용 (필요시)
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/bin/docker
```

#### Linux iptables
```bash
# 1. 포트 허용
sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT

# 2. 설정 저장
sudo iptables-save > /etc/iptables/rules.v4
```

#### Windows 방화벽
```powershell
# PowerShell 관리자 권한으로 실행
New-NetFirewallRule -DisplayName "Desinsight-5000" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow
New-NetFirewallRule -DisplayName "Desinsight-8000" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
```

### 🔄 프록시 설정 (기업 환경)

```bash
# 1. Docker 프록시 설정
mkdir -p ~/.docker
cat > ~/.docker/config.json << EOF
{
  "proxies": {
    "default": {
      "httpProxy": "http://proxy.company.com:8080",
      "httpsProxy": "http://proxy.company.com:8080",
      "noProxy": "localhost,127.0.0.1,192.168.219.175"
    }
  }
}
EOF

# 2. 컨테이너 환경 변수
docker run -d \
  --name desinsight-workspace \
  -e HTTP_PROXY=http://proxy.company.com:8080 \
  -e HTTPS_PROXY=http://proxy.company.com:8080 \
  -e NO_PROXY=localhost,127.0.0.1,192.168.219.175 \
  desinsight/workspace:latest
```

---

## 📂 볼륨 마운트 설정

### 💾 데이터 영구 저장

#### A. Named Volume 방식 (권장)
```yaml
# docker-compose.workspace.yml 설정
volumes:
  desinsight_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /Users/username/desinsight_data  # 로컬 경로
```

#### B. Bind Mount 방식
```bash
# 1. 로컬 디렉토리 생성
mkdir -p ~/desinsight/{data,logs,models,configs}

# 2. 권한 설정
chmod 755 ~/desinsight
chmod -R 777 ~/desinsight/logs

# 3. 마운트로 실행
docker run -d \
  --name desinsight-workspace \
  -v ~/desinsight/data:/workspace/shared-data \
  -v ~/desinsight/logs:/workspace/logs \
  -v ~/desinsight/models:/workspace/shared-data/models \
  -v ~/desinsight/configs:/workspace/docker-configs \
  -p 5000:5000 -p 8000:8000 \
  desinsight/workspace:latest
```

### 🔄 NAS 직접 마운트 (고급)

#### macOS NAS 마운트
```bash
# 1. NAS 마운트 포인트 생성
sudo mkdir -p /Volumes/snapcodex

# 2. SMB 마운트
sudo mount -t smbfs //admin@192.168.219.175/volume1 /Volumes/snapcodex

# 3. 자동 마운트 설정 (/etc/fstab)
echo "//admin@192.168.219.175/volume1 /Volumes/snapcodex smbfs rw,auto" | sudo tee -a /etc/fstab

# 4. Docker에서 마운트 사용
docker run -d \
  --name desinsight-workspace \
  -v /Volumes/snapcodex/workspace:/workspace/nas-data:ro \
  desinsight/workspace:latest
```

#### Linux NFS 마운트
```bash
# 1. NFS 클라이언트 설치
sudo apt install -y nfs-common

# 2. 마운트 포인트 생성
sudo mkdir -p /mnt/snapcodex

# 3. NFS 마운트
sudo mount -t nfs 192.168.219.175:/volume1 /mnt/snapcodex

# 4. 자동 마운트 설정
echo "192.168.219.175:/volume1 /mnt/snapcodex nfs defaults,_netdev 0 0" | sudo tee -a /etc/fstab
```

---

## 🛠️ 팀 워크플로우

### 👥 멀티 개발자 환경

#### A. 개발자별 포트 할당
```bash
# 개발자 A (포트 5000-5009)
docker run -d --name desinsight-dev-a \
  -p 5000:5000 -p 5001:8000 -p 5002:8888 \
  desinsight/workspace:latest

# 개발자 B (포트 5010-5019)  
docker run -d --name desinsight-dev-b \
  -p 5010:5000 -p 5011:8000 -p 5012:8888 \
  desinsight/workspace:latest
```

#### B. 환경별 설정 파일
```bash
# 1. 환경별 설정 디렉토리
mkdir -p ~/desinsight/{dev,staging,prod}

# 2. 개발 환경 설정
cat > ~/desinsight/dev/.env << EOF
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=debug
NAS_HOST=192.168.219.175
OLLAMA_HOST=http://localhost:11434
EOF

# 3. 환경별 실행
docker-compose --env-file ~/desinsight/dev/.env up -d
```

### 🔄 코드 동기화

#### A. Git 워크플로우
```bash
# 1. 컨테이너 내부에서 Git 설정
docker exec -it desinsight-workspace bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"

# 2. SSH 키 설정
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
cat ~/.ssh/id_rsa.pub
# GitHub/GitLab에 공개키 등록

# 3. 코드 동기화
git pull origin main
git add .
git commit -m "Update from container"
git push origin main
```

#### B. 실시간 코드 동기화 (rsync)
```bash
# 1. rsync를 통한 양방향 동기화
# 로컬 → 컨테이너
rsync -avz ~/local-workspace/ desinsight-workspace:/workspace/

# 컨테이너 → 로컬  
docker cp desinsight-workspace:/workspace/ ~/local-workspace/

# 2. 자동 동기화 스크립트
cat > sync_workspace.sh << 'EOF'
#!/bin/bash
watch -n 5 'rsync -avz ~/local-workspace/ desinsight-workspace:/workspace/'
EOF
chmod +x sync_workspace.sh
```

### 📊 모니터링 및 로깅

#### A. 통합 로그 관리
```bash
# 1. 로그 수집 설정
docker-compose -f docker-compose.workspace.yml logs -f --tail=100

# 2. 로그 파일 확인
docker exec -it desinsight-workspace tail -f /workspace/logs/dashboard/monitoring.log

# 3. 로그 로테이션 설정
docker exec -it desinsight-workspace bash -c "
cat > /etc/logrotate.d/desinsight << EOF
/workspace/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    copytruncate
}
EOF"
```

#### B. 성능 모니터링
```bash
# 1. 컨테이너 리소스 사용량
docker stats desinsight-workspace

# 2. 상세 모니터링 (cAdvisor)
docker run -d \
  --name=cadvisor \
  -p 8080:8080 \
  -v /:/rootfs:ro \
  -v /var/run:/var/run:ro \
  -v /sys:/sys:ro \
  -v /var/lib/docker/:/var/lib/docker:ro \
  gcr.io/cadvisor/cadvisor:latest
```

---

## ❓ 문제 해결

### 🔧 일반적인 문제들

#### A. 포트 충돌
```bash
# 문제: "Port already in use" 오류
# 해결: 사용 중인 프로세스 확인 및 종료
sudo lsof -i :5000
sudo kill -9 <PID>

# 또는 다른 포트 사용
docker run -p 5001:5000 desinsight/workspace:latest
```

#### B. 권한 문제
```bash
# 문제: Permission denied 오류
# 해결: Docker 그룹 추가 (Linux)
sudo usermod -aG docker $USER
newgrp docker

# macOS: Docker Desktop 재시작
killall Docker && open /Applications/Docker.app
```

#### C. 메모리 부족
```bash
# 문제: Out of memory 오류
# 해결: Docker 메모리 제한 증가
# Docker Desktop → Settings → Resources → Memory → 8GB

# 또는 컨테이너별 메모리 제한
docker run --memory=4g desinsight/workspace:latest
```

#### D. 네트워크 연결 실패
```bash
# 문제: NAS 연결 실패
# 해결 1: VPN 연결 확인
ping 192.168.219.175

# 해결 2: DNS 설정 확인
nslookup desinsight2.local

# 해결 3: 방화벽 설정 확인
telnet 192.168.219.175 22
```

### 🧹 시스템 정리

#### A. Docker 정리
```bash
# 1. 중지된 컨테이너 제거
docker container prune -f

# 2. 사용하지 않는 이미지 제거
docker image prune -a -f

# 3. 볼륨 정리
docker volume prune -f

# 4. 전체 정리
docker system prune -a -f --volumes
```

#### B. 로그 정리
```bash
# 1. Docker 로그 크기 제한
cat > /etc/docker/daemon.json << EOF
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
EOF

# 2. 로그 수동 정리
docker exec -it desinsight-workspace bash -c "
find /workspace/logs -name '*.log' -mtime +7 -delete
"
```

### 📞 지원 및 문의

#### A. 로그 수집 스크립트
```bash
# 문제 발생 시 로그 수집
cat > collect_logs.sh << 'EOF'
#!/bin/bash
mkdir -p desinsight-logs
docker logs desinsight-workspace > desinsight-logs/container.log 2>&1
docker exec desinsight-workspace ps aux > desinsight-logs/processes.log
docker exec desinsight-workspace df -h > desinsight-logs/disk.log
docker exec desinsight-workspace free -h > desinsight-logs/memory.log
tar -czf desinsight-logs-$(date +%Y%m%d-%H%M%S).tar.gz desinsight-logs/
echo "로그 수집 완료: desinsight-logs-$(date +%Y%m%d-%H%M%S).tar.gz"
EOF
chmod +x collect_logs.sh
```

#### B. 팀 지원 채널
- **Slack**: #desinsight-support
- **Email**: dev-team@desinsight.com
- **Wiki**: https://wiki.desinsight.com/docker-setup
- **이슈 트래커**: https://github.com/desinsight/workspace/issues

---

## 🎯 빠른 시작 체크리스트

### ✅ 설치 전 체크리스트
- [ ] Docker Desktop/Engine 설치 완료
- [ ] NAS (192.168.219.175) 접근 가능
- [ ] SSH 키 또는 비밀번호 준비
- [ ] 최소 8GB 디스크 여유 공간
- [ ] 포트 5000-8888 사용 가능

### ✅ 설치 후 체크리스트
- [ ] `docker ps`로 컨테이너 실행 확인
- [ ] http://localhost:5000 접속 가능
- [ ] http://localhost:8888 JupyterLab 접속 가능
- [ ] 로그 파일 생성 확인 (`docker logs`)
- [ ] 볼륨 마운트 정상 동작 확인

### ✅ 개발 환경 체크리스트
- [ ] IDE/편집기 Docker 연동 완료
- [ ] Git 설정 및 SSH 키 등록
- [ ] 로컬 작업 디렉토리 동기화 설정
- [ ] 팀 공유 설정 (포트, 환경변수) 적용
- [ ] 백업 및 복구 절차 숙지

---

**🎉 이제 다른 PC에서도 Desinsight 분산 RAG 시스템을 완벽하게 사용할 수 있습니다!**

추가 질문이나 문제가 있으시면 언제든지 문의하세요! 🚀 