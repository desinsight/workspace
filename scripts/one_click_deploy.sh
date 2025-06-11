#!/bin/bash

# Desinsight Workspace One-Click Deploy
# 5-Device + 3-NAS 분산 RAG 생태계 원클릭 배포 시스템

set -e  # 에러 발생시 중단

# 색상 코드 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 로고 출력
print_logo() {
    echo -e "${BLUE}"
    echo "████████▄   ▄████████    ▄████████  ▄█  ███▄▄▄▄      ▄████████  ▄█    ▄██████▄     ▄█    █▄      ███"
    echo "███   ▀███ ███    ███   ███    ███ ███  ███▀▀▀██▄   ███    ███ ███   ███    ███   ███    ███ ▀█████████▄"
    echo "███    ███ ███    █▀    ███    █▀  ███▌ ███   ███   ███    █▀  ███▌  ███    █▀    ███    ███    ▀███▀▀██"
    echo "███    ███ ▄███▄▄▄       ▄███▄▄▄   ███▌ ███   ███   ▄███▄▄▄     ███▌ ▄███          ███    ███     ███   ▀"
    echo "███    ███▀▀███▀▀▀      ▀▀███▀▀▀   ███▌ ███   ███  ▀▀███▀▀▀     ███▌▀▀███ ████▄  ▀███████████     ███"
    echo "███    ███  ███    █▄    ███    █▄  ███  ███   ███    ███    █▄  ███  ███    ███   ███    ███     ███"
    echo "███   ▄███  ███    ███   ███    ███ ███  ███   ███    ███    ███ ███  ███    ███   ███    ███     ███"
    echo "████████▀   ██████████   ██████████ █▀    ▀█   █▀     ██████████ █▀    ██████▀    ███    █▀     ▄████▀"
    echo -e "${NC}"
    echo -e "${PURPLE}🚀 Workspace Docker One-Click Deploy${NC}"
    echo -e "${CYAN}   5-Device + 3-NAS 분산 RAG 생태계${NC}"
    echo "========================================================================"
}

# 변수 설정
REGISTRY="desinsight"
VERSION="latest"
DEPLOY_MODE=${1:-"single"}
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
WORKSPACE_DIR=$(dirname "$SCRIPT_DIR")

# 시스템 정보 감지
detect_system() {
    echo -e "${YELLOW}🔍 시스템 환경 감지 중...${NC}"
    
    # CPU 정보
    if [[ "$OSTYPE" == "darwin"* ]]; then
        CPU_INFO=$(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo "Unknown")
        MEMORY_GB=$(( $(sysctl -n hw.memsize 2>/dev/null || echo "0") / 1024 / 1024 / 1024 ))
        OS_TYPE="macOS"
    else
        CPU_INFO=$(grep "model name" /proc/cpuinfo | head -1 | cut -d: -f2 | xargs || echo "Unknown")
        MEMORY_GB=$(( $(grep MemTotal /proc/meminfo | awk '{print $2}') / 1024 / 1024 ))
        OS_TYPE="Linux"
    fi
    
    echo -e "${GREEN}✅ 시스템 정보:${NC}"
    echo "   💻 OS: $OS_TYPE"
    echo "   🧠 CPU: $CPU_INFO"
    echo "   💾 Memory: ${MEMORY_GB}GB"
    echo ""
}

# Docker 설치 확인
check_docker() {
    echo -e "${YELLOW}🐳 Docker 환경 확인 중...${NC}"
    
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker가 설치되지 않았습니다!${NC}"
        echo "설치 방법:"
        echo "  macOS: brew install docker"
        echo "  Linux: curl -fsSL https://get.docker.com | sh"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        echo -e "${RED}❌ Docker 데몬이 실행되지 않았습니다!${NC}"
        echo "Docker Desktop을 시작하거나 'sudo systemctl start docker'를 실행하세요."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${YELLOW}⚠️ docker-compose가 없습니다. Docker Compose V2를 사용합니다.${NC}"
    fi
    
    DOCKER_VERSION=$(docker version --format '{{.Server.Version}}')
    echo -e "${GREEN}✅ Docker $DOCKER_VERSION 실행 중${NC}"
    echo ""
}

# 이미지 확인 및 빌드
check_and_build_images() {
    echo -e "${YELLOW}📦 이미지 확인 및 빌드...${NC}"
    
    IMAGES_TO_CHECK=(
        "$REGISTRY/workspace:$VERSION"
        "$REGISTRY/central-controller:$VERSION"
        "$REGISTRY/embedding-server:$VERSION"
        "$REGISTRY/inference-server:$VERSION"
        "$REGISTRY/ui-server:$VERSION"
        "$REGISTRY/development:$VERSION"
    )
    
    MISSING_IMAGES=()
    
    for image in "${IMAGES_TO_CHECK[@]}"; do
        if ! docker image inspect "$image" >/dev/null 2>&1; then
            MISSING_IMAGES+=("$image")
        fi
    done
    
    if [ ${#MISSING_IMAGES[@]} -gt 0 ]; then
        echo -e "${YELLOW}⚠️ 누락된 이미지들을 빌드합니다...${NC}"
        cd "$WORKSPACE_DIR"
        
        if [ -f "Makefile" ]; then
            make build
        else
            docker build -t "$REGISTRY/workspace:$VERSION" .
            docker build -t "$REGISTRY/central-controller:$VERSION" --target central-controller .
            docker build -t "$REGISTRY/embedding-server:$VERSION" --target embedding-server .
            docker build -t "$REGISTRY/inference-server:$VERSION" --target inference-server .
            docker build -t "$REGISTRY/ui-server:$VERSION" --target ui-server .
            docker build -t "$REGISTRY/development:$VERSION" --target development .
        fi
        
        echo -e "${GREEN}✅ 이미지 빌드 완료${NC}"
    else
        echo -e "${GREEN}✅ 모든 이미지가 준비되어 있습니다${NC}"
    fi
    echo ""
}

# 기존 컨테이너 정리
cleanup_existing() {
    echo -e "${YELLOW}🧹 기존 컨테이너 정리 중...${NC}"
    
    # Desinsight 관련 컨테이너 중지 및 제거
    CONTAINERS=$(docker ps -aq --filter "name=desinsight" 2>/dev/null || true)
    if [ -n "$CONTAINERS" ]; then
        echo "기존 컨테이너를 중지하고 제거합니다..."
        docker stop $CONTAINERS 2>/dev/null || true
        docker rm $CONTAINERS 2>/dev/null || true
        echo -e "${GREEN}✅ 기존 컨테이너 정리 완료${NC}"
    else
        echo -e "${GREEN}✅ 정리할 컨테이너가 없습니다${NC}"
    fi
    echo ""
}

# 디바이스별 배포 함수
deploy_device() {
    local device_type=$1
    local device_role=$2
    local container_name=$3
    local port_base=$4
    local image_target=$5
    
    echo -e "${BLUE}🖥️ Deploying $device_type ($device_role)...${NC}"
    
    # 환경별 포트 설정
    case $device_role in
        "central_controller")
            PORTS="-p 8000:8000 -p 8001:8001 -p 3000:3000"
            ;;
        "embedding_server")
            PORTS="-p 8002:8002 -p 8006:8006"
            ;;
        "inference_server")
            PORTS="-p 8003:8003 -p 8007:8007"
            ;;
        "ui_server")
            PORTS="-p 8004:8004 -p 8008:8008"
            ;;
        *)
            PORTS="-p $port_base:$port_base"
            ;;
    esac
    
    # 볼륨 설정
    VOLUMES="-v $WORKSPACE_DIR/data:/workspace/data -v $WORKSPACE_DIR/config:/workspace/config"
    
    # 환경 변수 설정
    ENV_VARS="-e DEVICE_TYPE=$device_type -e DEVICE_ROLE=$device_role"
    
    # 컨테이너 실행
    docker run -d \
        --name "$container_name" \
        $PORTS \
        $VOLUMES \
        $ENV_VARS \
        --restart unless-stopped \
        --network bridge \
        "$REGISTRY/$image_target:$VERSION"
    
    # 헬스체크
    echo "컨테이너 시작 대기 중..."
    sleep 5
    
    if docker ps | grep -q "$container_name"; then
        echo -e "${GREEN}✅ $device_type deployed successfully on port $port_base${NC}"
    else
        echo -e "${RED}❌ $device_type deployment failed${NC}"
        docker logs "$container_name" 2>/dev/null || true
        return 1
    fi
}

# 단일 디바이스 배포
deploy_single() {
    echo -e "${PURPLE}📱 Single Device Deployment${NC}"
    echo "현재 시스템에 맞는 환경을 자동 감지하여 배포합니다."
    echo ""
    
    # 시스템 사양에 따른 역할 결정
    if [ "$MEMORY_GB" -ge 60 ]; then
        ROLE="inference_server"
        IMAGE="inference-server"
    elif [ "$MEMORY_GB" -ge 32 ]; then
        ROLE="central_controller"
        IMAGE="central-controller"
    elif [ "$MEMORY_GB" -ge 16 ]; then
        ROLE="embedding_server"
        IMAGE="embedding-server"
    else
        ROLE="ui_server"
        IMAGE="ui-server"
    fi
    
    echo -e "${CYAN}자동 감지된 역할: $ROLE${NC}"
    
    deploy_device "auto_detect" "$ROLE" "desinsight-workspace" "8000" "$IMAGE"
}

# HOME 환경 배포
deploy_home() {
    echo -e "${PURPLE}🏠 HOME Environment Deployment${NC}"
    echo "중앙 제어 서버 + 임베딩 서버를 배포합니다."
    echo ""
    
    # 중앙 제어 서버
    deploy_device "home_imac_i7_64gb" "central_controller" "desinsight-home-central" "8000" "central-controller"
    
    # 임베딩 서버
    deploy_device "mac_mini_m2pro_32gb" "embedding_server" "desinsight-home-embedding" "8002" "embedding-server"
}

# OFFICE 환경 배포
deploy_office() {
    echo -e "${PURPLE}🏢 OFFICE Environment Deployment${NC}"
    echo "추론 서버 + UI 서버를 배포합니다."
    echo ""
    
    # 추론 서버
    deploy_device "mac_studio_m4pro_64gb" "inference_server" "desinsight-office-inference" "8003" "inference-server"
    
    # UI 서버
    deploy_device "office_imac_i7_40gb" "ui_server" "desinsight-office-ui" "8004" "ui-server"
}

# 전체 생태계 배포
deploy_all() {
    echo -e "${PURPLE}🌐 Full Ecosystem Deployment${NC}"
    echo "전체 분산 RAG 생태계를 배포합니다."
    echo ""
    
    cd "$WORKSPACE_DIR"
    
    if [ -f "docker-compose.yml" ]; then
        if command -v docker-compose &> /dev/null; then
            docker-compose up -d
        else
            docker compose up -d
        fi
        
        echo -e "${GREEN}✅ Full ecosystem deployment completed!${NC}"
    else
        echo -e "${RED}❌ docker-compose.yml 파일을 찾을 수 없습니다!${NC}"
        exit 1
    fi
}

# 개발 환경 배포
deploy_dev() {
    echo -e "${PURPLE}🔧 Development Environment Deployment${NC}"
    echo "개발용 올인원 환경을 배포합니다."
    echo ""
    
    docker run -d \
        --name desinsight-dev \
        -p 8000:8000 -p 8001:8001 -p 8002:8002 -p 8003:8003 -p 8004:8004 -p 8888:8888 \
        -v "$WORKSPACE_DIR:/workspace" \
        -v "$WORKSPACE_DIR/data:/workspace/data" \
        -e DEVICE_TYPE=development \
        -e DEVICE_ROLE=development \
        --restart unless-stopped \
        "$REGISTRY/development:$VERSION"
    
    echo -e "${GREEN}✅ Development environment deployed!${NC}"
    echo -e "${CYAN}🔗 Jupyter Notebook: http://localhost:8888${NC}"
}

# 배포 상태 확인
check_deployment_status() {
    echo -e "${YELLOW}📊 Deployment Status Check${NC}"
    echo "================================================"
    
    # 실행 중인 컨테이너 확인
    RUNNING_CONTAINERS=$(docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep desinsight || echo "")
    
    if [ -n "$RUNNING_CONTAINERS" ]; then
        echo -e "${GREEN}✅ Running Containers:${NC}"
        echo "$RUNNING_CONTAINERS"
    else
        echo -e "${YELLOW}⚠️ No Desinsight containers are running${NC}"
    fi
    
    echo ""
    echo -e "${CYAN}🌐 Access URLs:${NC}"
    echo "   📊 Main Dashboard: http://localhost:8000"
    echo "   🔗 API Documentation: http://localhost:8000/docs"
    echo "   ⚡ Embedding API: http://localhost:8002"
    echo "   🧠 Inference API: http://localhost:8003"
    echo "   🌐 Web UI: http://localhost:8004"
    echo "   📈 ChromaDB: http://localhost:8005"
    echo "   📊 Grafana: http://localhost:3001 (admin/desinsight2024)"
    echo ""
}

# 도움말 출력
print_help() {
    echo "사용법: $0 [mode]"
    echo ""
    echo "배포 모드:"
    echo "  single    - 단일 디바이스 배포 (자동 감지)"
    echo "  home      - HOME 환경 배포 (중앙제어+임베딩)"
    echo "  office    - OFFICE 환경 배포 (추론+UI)"
    echo "  all       - 전체 생태계 배포 (Docker Compose)"
    echo "  dev       - 개발 환경 배포 (올인원)"
    echo "  help      - 이 도움말 표시"
    echo ""
    echo "예시:"
    echo "  $0 single     # 현재 머신에 맞는 환경 자동 배포"
    echo "  $0 home       # HOME 환경 배포"
    echo "  $0 all        # 전체 시스템 배포"
}

# 메인 실행 함수
main() {
    print_logo
    
    # 도움말 요청 확인
    if [[ "$DEPLOY_MODE" == "help" || "$DEPLOY_MODE" == "-h" || "$DEPLOY_MODE" == "--help" ]]; then
        print_help
        exit 0
    fi
    
    # 시스템 환경 확인
    detect_system
    check_docker
    
    # 이미지 확인 및 빌드
    check_and_build_images
    
    # 기존 환경 정리
    cleanup_existing
    
    # 배포 모드별 실행
    case $DEPLOY_MODE in
        "single")
            deploy_single
            ;;
        "home")
            deploy_home
            ;;
        "office")
            deploy_office
            ;;
        "all")
            deploy_all
            ;;
        "dev")
            deploy_dev
            ;;
        *)
            echo -e "${RED}❌ Unknown deployment mode: $DEPLOY_MODE${NC}"
            print_help
            exit 1
            ;;
    esac
    
    # 배포 완료 확인
    echo ""
    check_deployment_status
    
    echo ""
    echo -e "${GREEN}🎉 Desinsight Workspace deployment completed successfully!${NC}"
    echo -e "${PURPLE}📊 웹 대시보드를 열어 시스템 상태를 확인하세요.${NC}"
    
    # 대시보드 자동 열기 (macOS만)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sleep 2
        open http://localhost:8000 2>/dev/null || true
    fi
}

# 스크립트 실행
main "$@" 