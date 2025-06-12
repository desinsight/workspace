# Desinsight 분산 RAG 시스템 Docker 배포 가이드

## 🎯 개요

**Desinsight 분산 RAG 시스템**의 완전한 Docker 컨테이너화 및 NAS 기반 배포 시스템입니다.

### 🏗️ 아키텍처
- **5개 디바이스**: HOME iMac i7 64GB, Mac Mini M2 Pro 32GB, Office iMac i7 40GB, Mac Studio M4 Pro 64GB, Mobile
- **3개 NAS**: SnapCodex NAS (192.168.219.175), Desinsight2 NAS, Office NAS (desinsight.synology.me)
- **통합 모니터링**: 실시간 시스템 메트릭, 서비스 상태, 네트워크 연결

---

## 📦 생성된 Docker 이미지

### 1. 📊 모니터링 대시보드 (이미 완성)
- **위치**: `/Users/gyungchulbae/workspace/dashboard/`
- **이미지**: `desinsight/monitoring-dashboard:latest`
- **크기**: ~254MB
- **기능**: 실시간 모니터링, 5개 디바이스 상태, 3개 NAS 연결 추적

### 2. 🏠 통합 워크스페이스 (신규 생성)
- **위치**: `/Users/gyungchulbae/workspace/`
- **이미지**: `desinsight/workspace:latest`
- **포함 서비스**: 
  - 모니터링 대시보드 (포트 5000)
  - 중앙 제어기 (포트 8000)
  - UI 서버 (포트 8080)
  - Streamlit (포트 8501)
  - Gradio (포트 7860)
  - JupyterLab (포트 8888)

---

## 🚀 빌드 및 배포 방법

### A. 현재 PC에서 빌드 및 NAS 업로드

```bash
# 1. 워크스페이스 통합 빌드 및 NAS 배포
./build_workspace_deploy.sh

# 2. (옵션) 대시보드만 별도 빌드
cd dashboard
./build_and_deploy.sh
```

### B. 다른 PC에서 NAS로부터 로드

```bash
# 1. 간단 로드 (추천)
./load_workspace_from_nas.sh

# 2. (옵션) 대시보드만 로드
cd dashboard
./load_from_nas.sh
```

---

## 📂 파일 구조

```
workspace/
├── 🐳 Docker 이미지 파일들
│   ├── Dockerfile.workspace              # 통합 워크스페이스용
│   ├── docker-compose.workspace.yml     # 전체 스택 오케스트레이션
│   ├── docker-workspace-entrypoint.sh   # 컨테이너 초기화
│   ├── build_workspace_deploy.sh        # 빌드&NAS 배포
│   └── load_workspace_from_nas.sh       # NAS에서 로드
│
├── 📊 대시보드 (별도 Docker)
│   └── dashboard/
│       ├── Dockerfile
│       ├── docker-compose.yml
│       ├── build_and_deploy.sh
│       └── load_from_nas.sh
│
└── 🗂️ 기존 프로젝트 구조
    ├── central-control/
    ├── rag-engine/
    ├── rag-system/
    ├── snapcodex/
    └── ...
```

---

## 🗄️ NAS 저장 구조

### SnapCodex NAS (192.168.219.175)

```
/volume1/docker-images/           # Docker 이미지 저장소
├── desinsight_workspace_YYYYMMDD_HHMMSS.tar    # 워크스페이스 이미지
├── desinsight_monitoring_YYYYMMDD_HHMMSS.tar   # 대시보드 이미지
├── desinsight_configs_YYYYMMDD_HHMMSS.tar.gz   # 설정 파일들
└── desinsight_deployment_YYYYMMDD_HHMMSS.md    # 배포 정보

/volume1/docker-backups/          # 백업 저장소
└── (위 파일들의 백업 복사본)

/volume1/workspace/               # 워크스페이스 백업
└── (전체 프로젝트 파일들)
```

---

## 🎮 사용 방법

### 1️⃣ 현재 PC에서 즉시 실행

```bash
# A. 기본 워크스페이스 실행
docker run -d --name desinsight-workspace \
  -p 5000:5000 -p 8000:8000 -p 8080:8080 \
  -p 8501:8501 -p 7860:7860 -p 8888:8888 \
  desinsight/workspace:latest

# B. Docker Compose 전체 스택 (권장)
docker-compose -f docker-compose.workspace.yml up -d

# C. 개발 모드
docker-compose -f docker-compose.workspace.yml --profile development up -d
```

### 2️⃣ 다른 PC에서 사용

```bash
# Step 1: NAS에서 로드 (자동화)
./load_workspace_from_nas.sh

# Step 2: 웹 접속
open http://localhost:5000
```

### 3️⃣ 수동 배포 (고급)

```bash
# 1. NAS에서 다운로드
scp admin@192.168.219.175:/volume1/docker-images/desinsight_workspace_*.tar .
scp admin@192.168.219.175:/volume1/docker-images/desinsight_configs_*.tar.gz .

# 2. 이미지 로드
docker load -i desinsight_workspace_*.tar

# 3. 설정 파일 압축 해제
tar -xzf desinsight_configs_*.tar.gz

# 4. 실행
cd desinsight_configs_*/
docker-compose -f docker-compose.workspace.yml up -d
```

---

## 🌐 웹 서비스 접속

| 서비스 | 포트 | URL | 설명 |
|--------|------|-----|------|
| 📊 모니터링 대시보드 | 5000 | http://localhost:5000 | 실시간 시스템 모니터링 |
| 🎛️ 중앙 제어기 | 8000 | http://localhost:8000 | RAG 시스템 제어 |
| 🖥️ UI 서버 | 8080 | http://localhost:8080 | 사용자 인터페이스 |
| 📈 Streamlit | 8501 | http://localhost:8501 | 데이터 시각화 |
| 🎨 Gradio | 7860 | http://localhost:7860 | AI 모델 인터페이스 |
| 📚 JupyterLab | 8888 | http://localhost:8888 | 개발 환경 |

---

## 🛠️ 관리 명령어

### Docker 컨테이너 관리

```bash
# 상태 확인
docker ps
docker-compose -f docker-compose.workspace.yml ps

# 로그 확인
docker logs desinsight-workspace -f
docker-compose -f docker-compose.workspace.yml logs -f

# 컨테이너 접속
docker exec -it desinsight-workspace bash

# 재시작
docker restart desinsight-workspace
docker-compose -f docker-compose.workspace.yml restart

# 중지/시작
docker stop desinsight-workspace
docker start desinsight-workspace

# 전체 스택 중지
docker-compose -f docker-compose.workspace.yml down
```

### 이미지 관리

```bash
# 이미지 목록
docker images | grep desinsight

# 이미지 삭제
docker rmi desinsight/workspace:latest
docker rmi desinsight/monitoring-dashboard:latest

# 시스템 정리
docker system prune -a
```

---

## 🔧 개발 모드

### 개발 환경 활성화

```bash
# 개발 모드로 실행
docker-compose -f docker-compose.workspace.yml --profile development up -d

# 또는 환경 변수로 설정
docker run -d --name desinsight-dev \
  -e DEVELOPMENT_MODE=true \
  -e FLASK_DEBUG=1 \
  -p 5001:5000 -p 8889:8888 \
  desinsight/workspace:latest
```

### 개발 모드 특징
- ✅ Flask 디버그 모드 활성화
- ✅ JupyterLab 자동 시작
- ✅ 코드 변경 시 자동 재로드
- ✅ 상세한 로깅

---

## 📋 전달사항

### ✅ 완성된 것들
1. **모니터링 대시보드 Docker 이미지** (254MB)
   - 실시간 시스템 모니터링
   - 5개 디바이스 상태 추적
   - 3개 NAS 연결 모니터링
   - WebSocket 실시간 통신

2. **통합 워크스페이스 Docker 이미지**
   - 전체 Desinsight RAG 시스템 포함
   - 다중 서비스 지원 (6개 포트)
   - AI/ML 라이브러리 사전 설치
   - 개발/프로덕션 모드 지원

3. **완전 자동화 스크립트**
   - 빌드 및 NAS 배포 자동화
   - 다른 PC에서 원클릭 설치
   - 설정 파일 자동 관리

### 🎯 사용 시나리오

#### A. 개발자 워크플로우
```bash
# 1. 코드 개발 후 이미지 빌드
./build_workspace_deploy.sh

# 2. 다른 PC에서 테스트
./load_workspace_from_nas.sh
```

#### B. 프로덕션 배포
```bash
# 1. 안정 버전 빌드
./build_workspace_deploy.sh

# 2. 각 디바이스에 배포
./load_workspace_from_nas.sh
```

#### C. 백업 및 복구
- NAS에 자동 백업 저장
- 버전별 이미지 관리
- 빠른 롤백 지원

### 🚨 주의사항

1. **네트워크 요구사항**
   - SnapCodex NAS (192.168.219.175) 접근 필요
   - SSH 키 또는 비밀번호 설정 필요

2. **시스템 요구사항**
   - Docker 및 Docker Compose 필수
   - 최소 4GB RAM, 권장 8GB
   - 충분한 디스크 공간 (이미지 크기에 따라)

3. **포트 충돌**
   - 5000, 8000, 8080, 8501, 7860, 8888 포트 사용
   - 필요시 docker-compose.yml에서 포트 변경

### 💡 다음 단계

1. **Ollama 통합**
   - 호스트 Ollama와 연동 설정
   - LLM 모델 자동 로드

2. **모니터링 강화**
   - Prometheus/Grafana 통합
   - 알림 시스템 구축

3. **CI/CD 파이프라인**
   - GitHub Actions 자동 빌드
   - 자동 NAS 배포

---

## 📞 문의 및 지원

- **개발팀**: Desinsight Team
- **문서 버전**: 4.0
- **최종 업데이트**: 2025-06-12

**🎉 Desinsight 분산 RAG 시스템 Docker 배포가 완료되었습니다!** 