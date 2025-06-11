#!/bin/bash

echo "🎯 Desinsight RAG 시스템 환경 확인"
echo "현재 하드웨어 및 소프트웨어 환경을 점검합니다..."

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

success() { echo -e "${GREEN}✅ $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; }
info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }

echo ""
# 1. 하드웨어 정보
info "🖥️ Hardware Information:"
echo "   Chip: $(sysctl -n machdep.cpu.brand_string)"
echo "   Memory: $(( $(sysctl -n hw.memsize) / 1024 / 1024 / 1024 ))GB RAM"
echo "   Cores: $(sysctl -n hw.ncpu) cores"

# Mac 모델 식별
if [[ $(sysctl -n machdep.cpu.brand_string) == *"M4"* ]]; then
    echo "   🏢 사무실 환경: Mac Studio M4 Max (추론 최적화)"
    ENVIRONMENT="office"
    ROLE="inference"
elif [[ $(sysctl -n machdep.cpu.brand_string) == *"M2"* ]]; then
    echo "   🏠 집 환경: Mac Mini M2 Pro (임베딩 최적화)"
    ENVIRONMENT="home"
    ROLE="embedding"
else
    echo "   🤔 Unknown Mac model"
    ENVIRONMENT="unknown"
    ROLE="general"
fi

echo ""

# 2. Ollama 설치 확인
info "🤖 Ollama Installation Check:"
if command -v ollama &> /dev/null; then
    success "Ollama is installed: $(ollama --version)"
    
    # 설치된 모델 확인
    echo "   📋 Installed models:"
    ollama list | grep -v "NAME" | while read line; do
        if [ ! -z "$line" ]; then
            echo "      - $line"
        fi
    done
    
    # Ollama 서비스 상태 확인
    if pgrep -f ollama > /dev/null; then
        success "Ollama service is running"
    else
        warning "Ollama service is not running - starting..."
        ollama serve &
        sleep 3
    fi
else
    error "Ollama is not installed"
    info "Install with: curl -fsSL https://ollama.ai/install.sh | sh"
fi

echo ""

# 3. Python 환경 확인
info "🐍 Python Environment Check:"
if command -v python3 &> /dev/null; then
    success "Python3 is available: $(python3 --version)"
    
    # 필요한 패키지 확인
    echo "   📦 Checking required packages:"
    packages=("sentence-transformers" "chromadb" "google-cloud-firestore" "ollama")
    
    for package in "${packages[@]}"; do
        if python3 -c "import $package" 2>/dev/null; then
            success "   $package is installed"
        else
            warning "   $package is not installed"
        fi
    done
else
    error "Python3 is not available"
fi

echo ""

# 4. 기존 NAS 연결 확인
info "🗄️ Existing NAS Connection Check:"
NAS_HOST="desinsight.synology.me"
NAS_PORT="5001"

if curl -s --connect-timeout 5 "https://$NAS_HOST:$NAS_PORT" > /dev/null; then
    success "기존 NAS ($NAS_HOST:$NAS_PORT) 연결 가능"
else
    warning "기존 NAS 연결 확인 필요"
fi

echo ""

# 5. Google Cloud SDK 확인
info "☁️ Google Cloud SDK Check:"
if command -v gcloud &> /dev/null; then
    success "Google Cloud SDK is installed: $(gcloud --version | head -1)"
    
    # 인증 상태 확인
    if gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -1 > /dev/null; then
        success "   Google Cloud authentication is active"
    else
        warning "   Google Cloud authentication required: gcloud auth login"
    fi
else
    warning "Google Cloud SDK not installed"
    info "Install with: curl https://sdk.cloud.google.com | bash"
fi

echo ""

# 6. 환경별 권장 모델
info "🎯 환경별 권장 설정:"
if [ "$ENVIRONMENT" = "office" ]; then
    echo "   🏢 사무실 환경 (Mac Studio M4 Max) - 추론 서버:"
    echo "      - llama3.1:70b (고성능 추론)"
    echo "      - codellama:34b (코드 분석)"
    echo "      - mistral:7b (빠른 응답)"
    echo ""
    echo "   🚀 설치 명령어:"
    echo "      ollama pull llama3.1:70b"
    echo "      ollama pull codellama:34b"
    echo "      ollama pull mistral:7b"

elif [ "$ENVIRONMENT" = "home" ]; then
    echo "   🏠 집 환경 (Mac Mini M2 Pro) - 임베딩 서버:"
    echo "      - llama3.1:7b (경량 모델)"
    echo "      - sentence-transformers (임베딩)"
    echo "      - 배치 처리 최적화"
    echo ""
    echo "   🚀 설치 명령어:"
    echo "      ollama pull llama3.1:7b"
    echo "      pip install sentence-transformers chromadb"
fi

echo ""

# 7. 네트워크 환경 확인
info "🌐 Network Environment Check:"
echo "   현재 IP: $(curl -s ifconfig.me || echo "확인 불가")"
echo "   로컬 IP: $(ifconfig | grep 'inet ' | grep -v '127.0.0.1' | head -1 | awk '{print $2}')"

# 집-사무실 연결 테스트 (ping)
if [ "$ENVIRONMENT" = "office" ]; then
    echo "   🏠 집 Mac Mini 연결 테스트 필요"
elif [ "$ENVIRONMENT" = "home" ]; then
    echo "   🏢 사무실 Mac Studio 연결 테스트 필요"
fi

echo ""

# 8. 다음 단계 가이드
info "📋 Next Steps for $ENVIRONMENT environment:"

if [ "$ENVIRONMENT" = "office" ]; then
    echo "   1. 고성능 모델 설치:"
    echo "      ollama pull llama3.1:70b"
    echo "      ollama pull codellama:34b"
    echo ""
    echo "   2. 추론 서버 설정:"
    echo "      cd ~/workspace"
    echo "      python setup_inference_server.py"
    echo ""
    echo "   3. 클라우드 벡터 DB 연결 설정"
    echo "   4. 집 환경과 동기화 설정"
    
elif [ "$ENVIRONMENT" = "home" ]; then
    echo "   1. 임베딩 모델 설치:"
    echo "      pip install sentence-transformers chromadb"
    echo "      ollama pull llama3.1:7b"
    echo ""
    echo "   2. NAS 데이터 수집 설정:"
    echo "      cd ~/workspace"
    echo "      python setup_nas_collector.py"
    echo ""
    echo "   3. 임베딩 생성 파이프라인 구축"
    echo "   4. 클라우드 동기화 설정"
    
else
    echo "   1. 환경 식별 후 역할 결정"
    echo "   2. Ollama 및 필요 패키지 설치"
    echo "   3. 네트워크 연결 설정"
fi

echo ""
echo "🎯 전체 시스템 구축을 위한 미션:"
echo "   Mission 1: 현재 환경 최적화 (이 스크립트 실행)"
echo "   Mission 2: NAS 데이터 수집 파이프라인 구축"
echo "   Mission 3: 분산 임베딩 시스템 구축"
echo "   Mission 4: 클라우드 벡터 DB 설정"
echo "   Mission 5: 집-사무실 동기화 시스템"
echo ""
success "환경 점검 완료! 다음 미션을 시작하세요 🚀"
