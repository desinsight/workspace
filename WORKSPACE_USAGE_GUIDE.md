# 🚀 Desinsight 분산 RAG 워크스페이스 사용 가이드

## 📋 목차
1. [워크스페이스 구조](#워크스페이스-구조)
2. [빠른 시작](#빠른-시작)
3. [실시간 모니터링](#실시간-모니터링)
4. [Docker 배포](#docker-배포)
5. [개발 환경 설정](#개발-환경-설정)
6. [주요 컴포넌트](#주요-컴포넌트)
7. [API 사용법](#api-사용법)
8. [문제 해결](#문제-해결)

---

## 🏗️ 워크스페이스 구조

### **📁 주요 디렉토리**

```
workspace/
├── 📊 실시간 모니터링 시스템
│   ├── realtime_monitoring_server.py      # 실시간 모니터링 서버
│   ├── enhanced_realtime_server.py        # 하트비트 수신 기능 포함
│   ├── device_monitoring_agent.py         # 클라이언트 모니터링 에이전트
│   ├── integrated_dashboard_server.py     # 통합 대시보드
│   └── simple_dashboard_server.py         # 간단 대시보드
│
├── 🐳 Docker 컨테이너
│   ├── Dockerfile.monitoring              # 모니터링 시스템 이미지
│   ├── docker-compose.monitoring.yml      # 모니터링 Docker Compose
│   ├── docker-compose.workspace.yml       # 전체 워크스페이스 Compose
│   └── build_monitoring_docker.sh         # Docker 빌드 스크립트
│
├── 🔧 관리 스크립트
│   ├── manage_nas_dashboard.sh             # NAS 대시보드 관리
│   ├── start_nas_dashboard.sh              # NAS 대시보드 시작
│   ├── nas_ssh_setup.sh                   # SSH 키 설정
│   └── upload_to_nas.sh                   # NAS 업로드
│
├── 📖 문서
│   ├── INTEGRATED_DASHBOARD_DEPLOYMENT.md # 대시보드 배포 가이드
│   ├── DOCKER_DEPLOYMENT_GUIDE.md         # Docker 배포 가이드
│   ├── PC_SETUP_GUIDE.md                  # PC 설정 가이드
│   └── SSH_KEY_AUTH_GUIDE.md               # SSH 인증 가이드
│
├── 🏭 RAG 시스템
│   ├── snapcodex/                          # SnapCodex RAG 엔진
│   ├── rag-engine/                         # RAG 처리 엔진
│   └── rag-system/                         # RAG 시스템 코어
│
├── 🎛️ 중앙 제어
│   ├── central-control/                    # 중앙 제어 시스템
│   ├── dashboard/                          # 대시보드 컴포넌트
│   └── orchestrator/                       # 오케스트레이터
│
└── 🔌 인프라
    ├── docker/                             # Docker 서비스들
    ├── logs/                               # 로그 파일들
    └── shared-data/                        # 공유 데이터
```

---

## ⚡ 빠른 시작

### **1️⃣ 전체 시스템 시작**

```bash
# 워크스페이스 클론
git clone https://github.com/desinsight/workspace.git
cd workspace

# Docker로 전체 시스템 시작
docker-compose -f docker-compose.workspace.yml up -d

# 또는 모니터링만 시작
./build_monitoring_docker.sh
```

### **2️⃣ 로컬 개발 환경**

```bash
# Python 가상환경 생성
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 실시간 모니터링 서버 시작
python3 enhanced_realtime_server.py
```

### **3️⃣ 접속 정보**

| 서비스 | URL | 설명 |
|--------|-----|------|
| **실시간 모니터링** | http://localhost:5004 | 5대 디바이스 + 3대 NAS 모니터링 |
| **통합 대시보드** | http://localhost:5003 | 전체 시스템 통합 대시보드 |
| **간단 대시보드** | http://localhost:5002 | 기본 모니터링 대시보드 |
| **API 엔드포인트** | http://localhost:5004/api | REST API |

---

## 📊 실시간 모니터링

### **🖥️ 대시보드 시작**

```bash
# 향상된 실시간 모니터링 서버 (권장)
python3 enhanced_realtime_server.py

# 기본 실시간 모니터링 서버
python3 realtime_monitoring_server.py

# 통합 대시보드
python3 integrated_dashboard_server.py

# 간단 대시보드
python3 simple_dashboard_server.py
```

### **📱 디바이스 에이전트 설치**

각 모니터링할 디바이스에서:

```bash
# 필요 라이브러리 설치
pip install psutil requests

# 에이전트 실행
python3 device_monitoring_agent.py \
  --name "디바이스명" \
  --dashboard "http://대시보드_IP:5004" \
  --interval 5
```

### **🔍 모니터링 대상**

**5대 디바이스:**
1. HOME iMac i7 64GB (192.168.219.100)
2. Mac Mini M2 Pro 32GB (192.168.219.101)
3. Office iMac i7 40GB (192.168.219.102)
4. Mac Studio M4 Pro 64GB (192.168.219.103)
5. Mobile Ecosystem (mobile)

**3대 NAS:**
1. SnapCodex NAS (192.168.219.175)
2. Desinsight2 NAS (desinsight2.local)
3. Office NAS (desinsight.synology.me)

---

## 🐳 Docker 배포

### **🔨 이미지 빌드**

```bash
# 모니터링 시스템 빌드
docker build -f Dockerfile.monitoring -t desinsight/monitoring-dashboard:1.0.0 .

# 자동 빌드 스크립트 실행
./build_monitoring_docker.sh
```

### **🚀 컨테이너 실행**

```bash
# 단일 컨테이너
docker run -d -p 5004:5004 desinsight/monitoring-dashboard:1.0.0

# Docker Compose
docker-compose -f docker-compose.monitoring.yml up -d

# 전체 워크스페이스
docker-compose -f docker-compose.workspace.yml up -d
```

### **📋 Docker 관리**

```bash
# 컨테이너 상태 확인
docker-compose -f docker-compose.monitoring.yml ps

# 로그 확인
docker-compose -f docker-compose.monitoring.yml logs -f

# 서비스 재시작
docker-compose -f docker-compose.monitoring.yml restart

# 서비스 중지
docker-compose -f docker-compose.monitoring.yml down
```

---

## 🛠️ 개발 환경 설정

### **🐍 Python 환경**

```bash
# Python 3.9+ 필요
python3 --version

# 가상환경 생성
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate    # Windows

# 의존성 설치
pip install -r requirements.txt
pip install -r requirements_simple.txt  # 간단 버전
```

### **📦 필수 패키지**

```python
# requirements.txt 주요 패키지
psutil==5.9.0       # 시스템 모니터링
requests==2.31.0    # HTTP 클라이언트
socketserver        # 웹 서버 (내장)
json               # JSON 처리 (내장)
time               # 시간 처리 (내장)
subprocess         # 프로세스 실행 (내장)
```

### **🔧 개발 도구**

```bash
# 코드 포맷팅
pip install black flake8

# 타입 체킹
pip install mypy

# 테스트
pip install pytest
```

---

## 🔩 주요 컴포넌트

### **1. 실시간 모니터링 서버**

**파일:** `enhanced_realtime_server.py`

```python
# 서버 시작
PORT = 5004
print(f"🚀 실시간 모니터링 서버 시작: http://localhost:{PORT}")

# 주요 기능
- 하트비트 수신 (/api/heartbeat)
- 디바이스 등록 (/api/register)
- 실시간 데이터 API (/api/devices)
- NAS 상태 API (/api/nas)
- 웹 대시보드 (/)
```

### **2. 디바이스 모니터링 에이전트**

**파일:** `device_monitoring_agent.py`

```python
# 에이전트 실행
agent = DeviceMonitoringAgent(
    dashboard_url="http://192.168.219.175:5004",
    device_name="Mac Studio M4 Pro"
)
agent.run(interval=5)

# 수집 데이터
- CPU 사용률 (psutil.cpu_percent)
- 메모리 사용률 (psutil.virtual_memory)
- 디스크 사용률 (psutil.disk_usage)
- 네트워크 정보 (psutil.net_io_counters)
```

### **3. 통합 대시보드**

**파일:** `integrated_dashboard_server.py`

```python
# 특징
- 5대 디바이스 + 3대 NAS 통합 모니터링
- Glassmorphism UI 디자인
- 실시간 프로그레스바
- 디바이스별 색상 코딩
- 30초 자동 새로고침
```

---

## 🔌 API 사용법

### **📡 REST API 엔드포인트**

| 엔드포인트 | 메서드 | 설명 | 예시 |
|------------|--------|------|------|
| `/` | GET | 웹 대시보드 | http://localhost:5004/ |
| `/api/devices` | GET | 디바이스 상태 조회 | curl http://localhost:5004/api/devices |
| `/api/nas` | GET | NAS 상태 조회 | curl http://localhost:5004/api/nas |
| `/api/heartbeat` | POST | 하트비트 전송 | curl -X POST -H "Content-Type: application/json" -d '{"device_name":"test","cpu":"50%"}' http://localhost:5004/api/heartbeat |
| `/api/register` | POST | 디바이스 등록 | curl -X POST -H "Content-Type: application/json" -d '{"name":"test","ip":"192.168.1.100"}' http://localhost:5004/api/register |

### **📋 API 응답 예시**

**GET /api/devices**
```json
{
  "timestamp": "2025-06-12 12:00:00",
  "devices": [
    {
      "name": "Mac Studio M4 Pro 64GB",
      "ip": "192.168.219.103",
      "status": "online",
      "cpu": "25%",
      "memory": "54%",
      "disk": "2%",
      "last_update": "12:00:00"
    }
  ]
}
```

**POST /api/heartbeat**
```json
{
  "device_name": "Mac Studio M4 Pro",
  "ip": "192.168.219.103",
  "timestamp": "2025-06-12 12:00:00",
  "cpu": "25%",
  "memory": "54%",
  "disk": "2%",
  "status": "online"
}
```

---

## 🔧 NAS 관리

### **📡 NAS 대시보드 관리**

```bash
# NAS 대시보드 시작
./start_nas_dashboard.sh

# NAS 대시보드 전체 관리
./manage_nas_dashboard.sh start    # 시작
./manage_nas_dashboard.sh stop     # 중지
./manage_nas_dashboard.sh restart  # 재시작
./manage_nas_dashboard.sh status   # 상태 확인
./manage_nas_dashboard.sh open     # 브라우저 열기
./manage_nas_dashboard.sh log      # 로그 확인
```

### **🔐 SSH 설정**

```bash
# SSH 키 생성 및 설정
./nas_ssh_key_setup.sh

# SSH 연결 테스트
ssh nas "hostname && date"

# 파일 업로드
./upload_to_nas.sh
```

---

## 🐛 문제 해결

### **🔍 일반적인 문제**

| 문제 | 해결책 |
|------|--------|
| **포트 충돌** | `lsof -i :5004` 로 포트 사용 확인 후 `kill -9 PID` |
| **Docker 빌드 실패** | `docker system prune -a` 후 재빌드 |
| **하트비트 연결 실패** | 방화벽 설정 확인, IP 주소 확인 |
| **NAS 연결 실패** | SSH 키 설정 확인, 네트워크 연결 확인 |

### **🔧 로그 확인**

```bash
# 서버 로그
tail -f logs/monitoring.log

# Docker 로그
docker logs container_name -f

# 시스템 로그
journalctl -u monitoring-service -f
```

### **⚡ 성능 최적화**

```bash
# 메모리 사용량 확인
ps aux | grep python3 | awk '{print $4}' | paste -sd+ | bc

# CPU 사용량 확인
top -p $(pgrep -d, python3)

# 디스크 사용량 확인
du -sh workspace/
```

---

## 📚 추가 문서

- [📊 통합 대시보드 배포 가이드](INTEGRATED_DASHBOARD_DEPLOYMENT.md)
- [🐳 Docker 배포 가이드](DOCKER_DEPLOYMENT_GUIDE.md)
- [💻 PC 설정 가이드](PC_SETUP_GUIDE.md)
- [🔐 SSH 키 인증 가이드](SSH_KEY_AUTH_GUIDE.md)

---

## 🆘 지원

**GitHub 저장소:** https://github.com/desinsight/workspace

**이슈 리포트:** GitHub Issues 탭 활용

**실시간 모니터링:** http://localhost:5004

---

*© 2025 Desinsight Team - 분산 RAG 시스템 워크스페이스* 