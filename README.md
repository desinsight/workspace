# Desinsight Workspace - 통합 개발환경

## 🎯 프로젝트 개요

**SnapCodex**는 Desinsight의 AI 기반 건축 자동화 플랫폼입니다.  
Notion 기반 내역서 시스템을 중심으로 CAD 파서, PDF 도면 인식, 수량 산출 자동화를 통합한 MVP를 구축합니다.

## 🏗 시스템 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   사무실 환경    │◄──►│  Synology NAS   │◄──►│    집 환경      │
│   (Cursor AI)   │    │   중앙 허브      │    │   (Cursor AI)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   SnapCodex     │
                    │  통합 플랫폼     │
                    └─────────────────┘
```

## 📁 프로젝트 구조

```
workspace/
├── snapcodex/                  # 메인 프로젝트
│   ├── core/                  # 핵심 비즈니스 로직
│   │   └── notion_manager.py  # Notion API 통합 관리
│   ├── services/              # 마이크로서비스
│   │   ├── snapy/            # Notion → PDF 보고서
│   │   ├── snapgpt/          # AI 도면 분석
│   │   ├── snapprice/        # 실시간 단가 관리
│   │   └── snapnft/          # 디지털 인증
│   ├── parsers/              # 파일 파서들
│   ├── embeddings/           # AI 임베딩 시스템
│   ├── api/                  # REST API
│   ├── requirements.txt      # Python 의존성
│   ├── .env.example         # 환경 변수 템플릿
│   └── .env                 # 실제 환경 변수 (git 제외)
├── docker-configs/          # NAS 배포 설정
│   └── nas-docker-compose.yml
├── scripts/                 # 자동화 스크립트
│   ├── setup.sh            # 개발 환경 구축
│   ├── home_to_nas_sync.sh # 집 → NAS 동기화
│   └── office_from_nas_sync.sh # NAS → 사무실 동기화
└── README.md               # 이 파일
```

## 🚀 빠른 시작

### 1. 환경 설정
```bash
# 저장소 클론
git clone <repository-url> ~/workspace
cd ~/workspace

# 자동 설정 실행
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 2. Notion 연결 테스트
```bash
cd snapcodex
source venv/bin/activate
python core/notion_manager.py
```

### 3. 개발 시작
```bash
cursor ~/workspace  # Cursor AI로 프로젝트 열기
```

## 🗄️ Notion 데이터베이스 구조

| 데이터베이스명 | 용도 | DB ID |
|---------------|------|-------|
| 공사비 보고서 | 메인 아웃풋 | -209c073e880280519a9cd86638e5c9c6 |
| 원가계산서 | 기본 계산 로직 | 20ac073e880280dba460c9d3741a2388 |
| 층별 집계표 | 공간별 상세 분석 | 209c073e8802806f967f000c323c5bd8 |
| 실별 집계표 | 실별 수량 관리 | 208c073e880280eebb3df3672f8f0cc3 |
| 내역서 | 세부 항목 관리 | 205c073e880280ca9c32dcb4871324a0 |
| 단가 DB | 실시간 자재비 | DB-205c073e880280c8ba2febd705e0e789 |
| 설계도서 DB | 도면 기반 수량 | 207c073e88028005928edfbd6c002a8c |

## 🔄 개발 워크플로우

### 집에서 작업 시
```bash
# 작업 완료 후 NAS로 백업
./scripts/home_to_nas_sync.sh
```

### 사무실 도착 시
```bash
# NAS에서 최신 버전 동기화
./scripts/office_from_nas_sync.sh
```

## 🐳 NAS 인프라 구축

### Docker 서비스 구성
- **Gitea**: Git 중앙 저장소
- **PostgreSQL**: 메인 데이터베이스
- **Redis**: 캐싱 시스템
- **Ollama**: 로컬 LLM
- **ChromaDB**: 벡터 데이터베이스
- **SnapCodex API**: 메인 애플리케이션 서버
- **Nginx**: 리버스 프록시
- **Syncthing**: 파일 동기화

### NAS 배포
```bash
# NAS에 SSH 접속
ssh admin@nas.local

# Docker 환경 구축
cd /volume1/docker-configs
docker-compose -f nas-docker-compose.yml up -d
```

## 🧠 AI 시스템 구성

### 로컬 LLM + RAG
- **Ollama**: 로컬 LLM 엔진
- **ChromaDB**: 벡터 저장소
- **임베딩**: 도면/문서 벡터화
- **의미 검색**: AI 기반 정보 추출

### MVP 기능
1. **CAD 파서**: DWG/PDF 파일 자동 분석
2. **수량 산출**: AI 기반 면적/길이 계산
3. **Notion 연동**: 자동 데이터 업데이트
4. **PDF 생성**: 표준 양식 보고서 출력

## 🔧 개발 도구

### MCP (Model Context Protocol) 설정
Claude Desktop과 로컬 파일시스템 연동:
```json
{
  "mcpServers": {
    "workspace-filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "/Users/gyungchulbae/workspace"],
      "env": {"NODE_ENV": "development"}
    }
  }
}
```

### 권장 개발 환경
- **IDE**: Cursor AI (AI 코딩 지원)
- **Python**: 3.9+ (가상환경 사용)
- **Git**: 버전 관리 및 NAS 동기화
- **Docker**: 컨테이너 환경 (NAS 배포용)

## 📊 개발 단계별 계획

### Phase 1: 기반 인프라 (2주)
- [x] MCP 파일시스템 연동
- [x] Notion API 통합 관리자
- [x] 기본 프로젝트 구조
- [ ] NAS Docker 환경 구축

### Phase 2: CAD/PDF 파서 (3주)
- [ ] DWG/DXF 파일 파싱
- [ ] PDF 도면 OCR 인식
- [ ] 공간 구분 및 면적 계산
- [ ] 치수선 자동 추출

### Phase 3: AI 임베딩 및 자동화 (4주)
- [ ] 로컬 LLM 설정
- [ ] RAG 시스템 구축
- [ ] 수량 산출 자동화
- [ ] Notion 데이터 동기화

### Phase 4: 통합 및 배포 (1주)
- [ ] 전체 시스템 통합
- [ ] 성능 최적화
- [ ] 사용자 인터페이스
- [ ] 배포 자동화

## 🔐 보안 설정

### 환경 변수 관리
- `.env` 파일은 git에서 제외
- `.env.example`로 템플릿 제공
- NAS 백업 시 민감 정보 제외

### 접근 권한
- SSH 키 기반 NAS 접근
- Notion API 토큰 암호화
- Docker 컨테이너 격리

## 🎯 성공 지표

### MVP 완성 기준
1. **연속성**: 집↔사무실 완벽 동기화
2. **자동화**: CAD → Notion → PDF 파이프라인
3. **정확도**: 수량 산출 95% 이상 정확도
4. **성능**: 도면 분석 5분 이내 완료

## 🤝 기여 가이드

### 개발 규칙
- 커밋 메시지: Conventional Commits 표준
- 코드 스타일: Black + Flake8
- 테스트: pytest (커버리지 90% 목표)
- 문서화: Docstring (Google Style)

---

**Developed by Desinsight** 🏗️  
**AI-Powered Construction Automation Platform** 🤖
