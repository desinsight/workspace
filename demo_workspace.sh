#!/bin/bash

# 🚀 Desinsight 워크스페이스 데모 스크립트
# 이 스크립트는 워크스페이스의 주요 기능들을 시연합니다

set -e

# 색상 코드
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 로고 출력
echo -e "${CYAN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║         🚀 Desinsight 분산 RAG 워크스페이스               ║
║              실시간 모니터링 시스템 데모                  ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# 함수들
print_header() {
    echo -e "\n${PURPLE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}  $1${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════${NC}\n"
}

print_step() {
    echo -e "${CYAN}🔹 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

check_dependencies() {
    print_header "📦 의존성 확인"
    
    # Python 확인
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        print_success "Python: $PYTHON_VERSION"
    else
        print_error "Python3가 설치되지 않았습니다"
        exit 1
    fi
    
    # Docker 확인
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version)
        print_success "Docker: $DOCKER_VERSION"
    else
        print_warning "Docker가 설치되지 않았습니다 (선택사항)"
    fi
    
    # Git 확인
    if command -v git &> /dev/null; then
        GIT_VERSION=$(git --version)
        print_success "Git: $GIT_VERSION"
    else
        print_warning "Git이 설치되지 않았습니다"
    fi
    
    # 필수 Python 패키지 확인
    print_step "Python 패키지 확인 중..."
    if python3 -c "import psutil, requests" 2>/dev/null; then
        print_success "필수 Python 패키지가 설치되어 있습니다"
    else
        print_warning "일부 Python 패키지가 누락되었습니다"
        echo -e "${YELLOW}다음 명령어로 설치하세요: pip install psutil requests${NC}"
    fi
}

show_workspace_structure() {
    print_header "🏗️ 워크스페이스 구조"
    
    print_step "주요 디렉토리 구조:"
    echo "workspace/"
    echo "├── 📊 실시간 모니터링 시스템"
    echo "│   ├── enhanced_realtime_server.py"
    echo "│   ├── device_monitoring_agent.py"
    echo "│   └── integrated_dashboard_server.py"
    echo "├── 🐳 Docker 설정"
    echo "│   ├── Dockerfile.monitoring"
    echo "│   ├── docker-compose.monitoring.yml"
    echo "│   └── build_monitoring_docker.sh"
    echo "├── 📖 문서"
    echo "│   ├── WORKSPACE_USAGE_GUIDE.md"
    echo "│   └── INTEGRATED_DASHBOARD_DEPLOYMENT.md"
    echo "└── 🔧 관리 스크립트"
    echo "    ├── manage_nas_dashboard.sh"
    echo "    └── start_nas_dashboard.sh"
}

demo_monitoring_server() {
    print_header "📊 실시간 모니터링 서버 데모"
    
    print_step "모니터링 서버 상태 확인..."
    
    # 포트 확인
    if lsof -i :5004 2>/dev/null | grep -q LISTEN; then
        print_success "포트 5004에서 서비스가 실행 중입니다"
        print_info "URL: http://localhost:5004"
    else
        print_warning "포트 5004에서 실행 중인 서비스가 없습니다"
        
        print_step "모니터링 서버 시작 옵션:"
        echo "1. python3 enhanced_realtime_server.py"
        echo "2. python3 integrated_dashboard_server.py"
        echo "3. ./build_monitoring_docker.sh"
    fi
    
    # 모니터링 대상 디바이스
    print_step "모니터링 대상 디바이스:"
    echo "🖥️  HOME iMac i7 64GB (192.168.219.100)"
    echo "🖥️  Mac Mini M2 Pro 32GB (192.168.219.101)"
    echo "🖥️  Office iMac i7 40GB (192.168.219.102)"
    echo "🖥️  Mac Studio M4 Pro 64GB (192.168.219.103)"
    echo "📱 Mobile Ecosystem (mobile)"
    echo ""
    echo "💾 SnapCodex NAS (192.168.219.175)"
    echo "💾 Desinsight2 NAS (desinsight2.local)"
    echo "💾 Office NAS (desinsight.synology.me)"
}

demo_agent_installation() {
    print_header "📱 디바이스 에이전트 설치 데모"
    
    print_step "에이전트 설치 및 실행 방법:"
    
    echo -e "${CYAN}1. 필수 패키지 설치:${NC}"
    echo "   pip install psutil requests"
    echo ""
    
    echo -e "${CYAN}2. 에이전트 실행:${NC}"
    echo "   python3 device_monitoring_agent.py \\"
    echo "     --name \"Mac Studio M4 Pro\" \\"
    echo "     --dashboard \"http://192.168.219.175:5004\" \\"
    echo "     --interval 5"
    echo ""
    
    # 현재 시스템 정보 수집 데모
    print_step "현재 시스템 정보 수집 테스트:"
    
    if python3 -c "import psutil" 2>/dev/null; then
        echo -e "${CYAN}CPU 사용률:${NC}"
        python3 -c "import psutil; print(f'  {psutil.cpu_percent(interval=1)}%')"
        
        echo -e "${CYAN}메모리 사용률:${NC}"
        python3 -c "import psutil; mem = psutil.virtual_memory(); print(f'  {mem.percent}% ({mem.used // (1024**3):.1f}GB / {mem.total // (1024**3):.1f}GB)')"
        
        echo -e "${CYAN}디스크 사용률:${NC}"
        python3 -c "import psutil; disk = psutil.disk_usage('/'); print(f'  {disk.percent}% ({disk.used // (1024**3):.1f}GB / {disk.total // (1024**3):.1f}GB)')"
    else
        print_warning "psutil 패키지가 설치되지 않아 시스템 정보를 수집할 수 없습니다"
    fi
}

demo_docker_deployment() {
    print_header "🐳 Docker 배포 데모"
    
    if command -v docker &> /dev/null; then
        print_step "Docker 이미지 확인..."
        
        # 기존 이미지 확인
        if docker images | grep -q "desinsight/monitoring-dashboard"; then
            print_success "모니터링 Docker 이미지가 존재합니다"
            docker images | grep "desinsight/monitoring-dashboard"
        else
            print_warning "모니터링 Docker 이미지가 없습니다"
            echo -e "${YELLOW}빌드 명령어: ./build_monitoring_docker.sh${NC}"
        fi
        
        print_step "Docker Compose 파일 확인..."
        if [ -f "docker-compose.monitoring.yml" ]; then
            print_success "docker-compose.monitoring.yml 파일이 존재합니다"
            echo -e "${CYAN}실행 명령어:${NC}"
            echo "  docker-compose -f docker-compose.monitoring.yml up -d"
        else
            print_warning "docker-compose.monitoring.yml 파일이 없습니다"
        fi
        
        # 실행 중인 컨테이너 확인
        print_step "실행 중인 컨테이너 확인..."
        RUNNING_CONTAINERS=$(docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(monitoring|dashboard)" || echo "None")
        if [ "$RUNNING_CONTAINERS" != "None" ]; then
            print_success "실행 중인 모니터링 컨테이너:"
            echo "$RUNNING_CONTAINERS"
        else
            print_info "현재 실행 중인 모니터링 컨테이너가 없습니다"
        fi
    else
        print_warning "Docker가 설치되지 않았습니다"
    fi
}

demo_api_endpoints() {
    print_header "🔌 API 엔드포인트 데모"
    
    # 로컬 서버 확인
    if command -v curl &> /dev/null; then
        print_step "API 엔드포인트 테스트..."
        
        BASE_URL="http://localhost:5004"
        
        # 기본 헬스체크
        print_info "헬스체크 테스트: $BASE_URL"
        if curl -s --connect-timeout 3 "$BASE_URL" | grep -q "Desinsight" 2>/dev/null; then
            print_success "서버가 응답합니다"
        else
            print_warning "서버가 응답하지 않습니다"
        fi
        
        # API 엔드포인트 목록
        echo -e "\n${CYAN}사용 가능한 API 엔드포인트:${NC}"
        echo "  GET  $BASE_URL/              - 웹 대시보드"
        echo "  GET  $BASE_URL/api/devices   - 디바이스 상태"
        echo "  GET  $BASE_URL/api/nas       - NAS 상태"
        echo "  POST $BASE_URL/api/heartbeat - 하트비트 전송"
        echo "  POST $BASE_URL/api/register  - 디바이스 등록"
        
        echo -e "\n${CYAN}API 테스트 예시:${NC}"
        echo "  curl $BASE_URL/api/devices | jq"
        echo "  curl -X POST -H 'Content-Type: application/json' \\"
        echo "    -d '{\"device_name\":\"test\",\"cpu\":\"50%\"}' \\"
        echo "    $BASE_URL/api/heartbeat"
    else
        print_warning "curl이 설치되지 않아 API 테스트를 할 수 없습니다"
    fi
}

show_usage_commands() {
    print_header "💡 주요 사용 명령어"
    
    echo -e "${CYAN}📊 모니터링 서버 시작:${NC}"
    echo "  python3 enhanced_realtime_server.py        # 향상된 실시간 서버"
    echo "  python3 integrated_dashboard_server.py     # 통합 대시보드"
    echo "  python3 simple_dashboard_server.py         # 간단 대시보드"
    echo ""
    
    echo -e "${CYAN}📱 디바이스 에이전트:${NC}"
    echo "  python3 device_monitoring_agent.py \\"
    echo "    --name \"디바이스명\" \\"
    echo "    --dashboard \"http://대시보드_IP:5004\" \\"
    echo "    --interval 5"
    echo ""
    
    echo -e "${CYAN}🐳 Docker 관리:${NC}"
    echo "  ./build_monitoring_docker.sh               # Docker 이미지 빌드"
    echo "  docker-compose -f docker-compose.monitoring.yml up -d"
    echo "  docker-compose -f docker-compose.monitoring.yml down"
    echo ""
    
    echo -e "${CYAN}🔧 NAS 관리:${NC}"
    echo "  ./manage_nas_dashboard.sh start            # NAS 대시보드 시작"
    echo "  ./manage_nas_dashboard.sh status           # 상태 확인"
    echo "  ./start_nas_dashboard.sh                   # 간단 시작"
    echo ""
    
    echo -e "${CYAN}📖 문서 확인:${NC}"
    echo "  cat WORKSPACE_USAGE_GUIDE.md               # 워크스페이스 사용법"
    echo "  cat INTEGRATED_DASHBOARD_DEPLOYMENT.md     # 대시보드 배포 가이드"
    echo "  cat DOCKER_DEPLOYMENT_GUIDE.md             # Docker 배포 가이드"
}

interactive_demo() {
    print_header "🎮 대화형 데모"
    
    while true; do
        echo -e "\n${CYAN}다음 중 하나를 선택하세요:${NC}"
        echo "1. 실시간 모니터링 서버 시작"
        echo "2. 디바이스 에이전트 실행"
        echo "3. Docker 컨테이너 시작"
        echo "4. API 테스트"
        echo "5. 시스템 상태 확인"
        echo "6. 종료"
        
        read -p "선택 (1-6): " choice
        
        case $choice in
            1)
                print_step "실시간 모니터링 서버를 시작합니다..."
                echo "python3 enhanced_realtime_server.py를 실행하세요"
                ;;
            2)
                print_step "디바이스 에이전트 실행 명령어:"
                echo "python3 device_monitoring_agent.py --name \"$(hostname)\" --dashboard \"http://localhost:5004\" --interval 5"
                ;;
            3)
                print_step "Docker 컨테이너를 시작합니다..."
                if [ -f "docker-compose.monitoring.yml" ]; then
                    docker-compose -f docker-compose.monitoring.yml up -d
                else
                    echo "docker-compose.monitoring.yml 파일이 없습니다"
                fi
                ;;
            4)
                print_step "API 테스트를 실행합니다..."
                if command -v curl &> /dev/null; then
                    curl -s http://localhost:5004/api/devices || echo "서버가 실행되지 않았습니다"
                else
                    echo "curl이 설치되지 않았습니다"
                fi
                ;;
            5)
                print_step "시스템 상태 확인..."
                lsof -i :5004 || echo "포트 5004에서 실행 중인 서비스가 없습니다"
                ;;
            6)
                print_success "데모를 종료합니다"
                break
                ;;
            *)
                print_error "잘못된 선택입니다"
                ;;
        esac
    done
}

# 메인 실행
main() {
    case "${1:-all}" in
        "deps")
            check_dependencies
            ;;
        "structure")
            show_workspace_structure
            ;;
        "monitoring")
            demo_monitoring_server
            ;;
        "agent")
            demo_agent_installation
            ;;
        "docker")
            demo_docker_deployment
            ;;
        "api")
            demo_api_endpoints
            ;;
        "commands")
            show_usage_commands
            ;;
        "interactive")
            interactive_demo
            ;;
        "all")
            check_dependencies
            show_workspace_structure
            demo_monitoring_server
            demo_agent_installation
            demo_docker_deployment
            demo_api_endpoints
            show_usage_commands
            ;;
        *)
            echo "사용법: $0 [deps|structure|monitoring|agent|docker|api|commands|interactive|all]"
            exit 1
            ;;
    esac
}

# 스크립트 실행
main "$@"

print_header "🎉 데모 완료"
print_success "Desinsight 워크스페이스 데모가 완료되었습니다!"
print_info "더 자세한 정보는 WORKSPACE_USAGE_GUIDE.md를 참조하세요"
print_info "GitHub: https://github.com/desinsight/workspace" 