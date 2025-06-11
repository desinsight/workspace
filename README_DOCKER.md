# 🚀 Desinsight Workspace Docker 컨테이너화

## 📋 개요

Desinsight RAG 워크스페이스를 Docker 컨테이너로 패키징하여 **5대 디바이스 어디서든 원클릭으로 동일한 개발환경**을 구축할 수 있습니다.

## 🏗 아키텍처

```
📦 desinsight/workspace:latest
├── 🐍 Python 3.11 + 모든 의존성
├── 📁 SnapCodex 프로젝트 전체
├── 🔧 RAG 시스템 도구들
├── 🗄️ 3-NAS 연결 설정
├── 🌐 웹 대시보드
├── ⚙️ 환경별 자동 설정
└── 🚀 원클릭 시작 스크립트
```

## 🚀 빠른 시작

### **1단계: 시스템 준비**

```bash
# Docker 설치 확인
docker --version
docker-compose --version

# 워크스페이스로 이동
cd /path/to/workspace
```

### **2단계: 원클릭 배포**

```bash
# 🏠 현재 시스템에 맞는 환경 자동 배포
./scripts/one_click_deploy.sh single

# 또는 Makefile 사용
make quick-start
```

### **3단계: 접속 확인**

```bash
# 대시보드 열기
open http://localhost:8000

# 상태 확인
make status
```

## 🖥 배포 모드

### **📱 Single Device (자동 감지)**
```bash
./scripts/one_click_deploy.sh single
```
- 현재 시스템 사양을 자동 감지
- 최적의 역할 자동 할당

### **🏠 HOME Environment**
```bash
./scripts/one_click_deploy.sh home
```
- 중앙 제어 서버 (iMac i7 64GB)
- 임베딩 서버 (Mac Mini M2 Pro 32GB)

### **🏢 OFFICE Environment**
```bash
./scripts/one_click_deploy.sh office
```
- 추론 서버 (Mac Studio M4 Pro 64GB)
- UI 서버 (iMac i7 40GB)

### **🌐 Full Ecosystem**
```bash
./scripts/one_click_deploy.sh all
# 또는
make deploy-all
```
- 전체 5-Device + 3-NAS 생태계
- PostgreSQL, Redis, ChromaDB 포함

### **🔧 Development Mode**
```bash
./scripts/one_click_deploy.sh dev
# 또는
make deploy-dev
```
- Jupyter Notebook 포함
- 모든 개발 도구 설치

## 📊 서비스 포트

| 서비스 | 포트 | 설명 |
|--------|------|------|
| 📊 Central Dashboard | 8000 | 중앙 제어 대시보드 |
| 🔗 API Server | 8001 | REST API 서버 |
| ⚡ Embedding API | 8002 | 임베딩 서비스 |
| 🧠 Inference API | 8003 | 추론 서비스 |
| 🌐 Web UI | 8004 | 사용자 인터페이스 |
| 📈 ChromaDB | 8005 | 벡터 데이터베이스 |
| 🐘 PostgreSQL | 5432 | 관계형 DB |
| 🔴 Redis | 6379 | 캐시 서버 |
| 📓 Jupyter | 8888 | 개발환경 (dev 모드) |
| 📊 Grafana | 3001 | 모니터링 (admin/desinsight2024) |

## 🛠 Makefile 명령어

### **이미지 관리**
```bash
make build          # 모든 이미지 빌드
make build-base      # 기본 이미지만 빌드
make build-dev       # 개발 환경 빌드
make push            # 레지스트리에 푸시
make pull            # 이미지 풀
```

### **배포 관리**
```bash
make deploy-single   # 단일 디바이스 배포
make deploy-home     # HOME 환경 배포
make deploy-office   # OFFICE 환경 배포
make deploy-all      # 전체 생태계 배포
make deploy-dev      # 개발 환경 배포
```

### **모니터링 & 관리**
```bash
make status          # 컨테이너 상태 확인
make logs            # 로그 확인
make monitor         # 대시보드 열기
make shell           # 컨테이너 쉘 접속
make test            # 시스템 테스트
```

### **정리 & 백업**
```bash
make stop            # 모든 컨테이너 중지
make clean           # 정리
make clean-dev       # 개발 데이터만 정리
make backup          # 데이터 백업
make restore         # 백업 복구
make reset           # ⚠️ 전체 리셋
```

### **조합 명령**
```bash
make redeploy        # 빌드 + 전체 배포
make quick-start     # 개발환경 빠른 시작
make production      # 프로덕션 배포 + 백업
```

## 🔧 환경별 최적화

### **자동 역할 할당**
```bash
# 시스템 메모리에 따른 자동 역할 결정
64GB+ → inference_server    # 🧠 고성능 추론
32GB+ → central_controller  # 🎛️ 중앙 제어
16GB+ → embedding_server    # ⚡ 임베딩 처리
8GB+  → ui_server          # 🌐 사용자 인터페이스
```

### **디바이스별 설정**
- **HOME iMac i7 64GB**: 중앙 제어 + 오케스트레이션
- **Mac Mini M2 Pro 32GB**: 임베딩 + 벡터 처리
- **Mac Studio M4 Pro 64GB**: 고성능 추론
- **Office iMac i7 40GB**: 웹 UI + 사용자 접점

## 📁 프로젝트 구조

```
workspace/
├── Dockerfile                    # 멀티 스테이지 빌드
├── docker-compose.yml            # 전체 생태계 구성
├── Makefile                      # 관리 명령어
├── requirements.txt              # Python 의존성
├── scripts/
│   └── one_click_deploy.sh       # 원클릭 배포 스크립트
├── docker/
│   ├── entrypoint.sh             # 컨테이너 진입점
│   ├── central-controller/       # 중앙 제어 설정
│   ├── embedding-server/         # 임베딩 서버 설정
│   ├── inference-server/         # 추론 서버 설정
│   ├── ui-server/               # UI 서버 설정
│   ├── development/             # 개발 환경 설정
│   ├── postgres/                # PostgreSQL 설정
│   ├── redis/                   # Redis 설정
│   └── grafana/                 # Grafana 설정
```

## 🌐 네트워크 설정

### **포트 포워딩**
```bash
# 기본 포트 매핑
-p 8000:8000  # 대시보드
-p 8001:8001  # API
-p 8002:8002  # 임베딩
-p 8003:8003  # 추론
-p 8004:8004  # UI
```

### **볼륨 마운트**
```bash
# 데이터 영속성
-v ./data:/workspace/data
-v ./config:/workspace/config
-v ./logs:/workspace/logs
```

## 🔍 트러블슈팅

### **Docker 설치 확인**
```bash
# macOS
brew install docker docker-compose

# Docker Desktop 시작 확인
docker info
```

### **포트 충돌 해결**
```bash
# 사용 중인 포트 확인
lsof -i :8000

# 다른 포트로 실행
docker run -p 8080:8000 desinsight/workspace:latest
```

### **메모리 부족**
```bash
# Docker 메모리 확인
docker system df

# 불필요한 이미지 정리
docker image prune -f
```

### **로그 확인**
```bash
# 실시간 로그
make logs

# 특정 서비스 로그
make logs-central
make logs-embedding
```

## 📊 모니터링

### **헬스체크**
```bash
# 서비스 상태 확인
curl http://localhost:8000/health
curl http://localhost:8002/health
curl http://localhost:8003/health
```

### **리소스 모니터링**
```bash
# 컨테이너 리소스 사용량
docker stats desinsight-central-controller

# 시스템 전체 상태
make status
```

## 🚀 고급 사용법

### **커스텀 설정**
```bash
# 환경 변수로 설정 오버라이드
docker run -e DEVICE_TYPE=custom -e MEMORY_LIMIT=32GB desinsight/workspace:latest
```

### **개발 모드**
```bash
# 코드 변경 실시간 반영
docker run -v $(pwd):/workspace desinsight/development:latest
```

### **프로덕션 배포**
```bash
# 전체 생태계 배포
make production

# 백업 포함 안전 배포
make backup && make deploy-all
```

## 🎯 다음 단계

1. **✅ 기본 배포**: `make quick-start`로 개발환경 시작
2. **🔧 환경 커스터마이징**: 필요에 따라 설정 조정
3. **🌐 분산 배포**: 다른 디바이스에 역할별 배포
4. **📊 모니터링**: Grafana 대시보드로 시스템 관찰
5. **🚀 프로덕션**: 안정적인 서비스 운영

---

## 🎉 성공!

이제 **어떤 Mac에서든 5분 내에** 완전한 Desinsight RAG 환경을 구축할 수 있습니다!

```bash
# 한 줄 명령으로 모든 것이 준비됩니다
make quick-start && open http://localhost:8000
```

**환경 차이 걱정 없이**, **설정 실수 없이**, **즉시 개발 시작** 가능합니다! 🚀 