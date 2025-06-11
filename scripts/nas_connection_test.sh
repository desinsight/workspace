#!/bin/bash

echo "🔍 SnapCodex NAS Connection Test"
echo "Testing connection to Synology NAS..."

# NAS 정보 설정
NAS_INTERNAL_IP="192.168.219.175"
NAS_DDNS="snapcodex.synology.me"
NAS_USER="admin"

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
info "NAS Information:"
echo "   Server Name: snapcodex"
echo "   Internal IP: $NAS_INTERNAL_IP"
echo "   DDNS: $NAS_DDNS"
echo "   MAC: 00-11-32-B8-60-D4"
echo ""

# 1. Ping 테스트 (내부 IP)
info "Testing internal IP connectivity..."
if ping -c 3 $NAS_INTERNAL_IP > /dev/null 2>&1; then
    success "Internal IP ($NAS_INTERNAL_IP) is reachable"
    NAS_HOST=$NAS_INTERNAL_IP
else
    error "Internal IP ($NAS_INTERNAL_IP) is not reachable"
    
    # 2. DDNS 테스트
    info "Testing DDNS connectivity..."
    if ping -c 3 $NAS_DDNS > /dev/null 2>&1; then
        success "DDNS ($NAS_DDNS) is reachable"
        NAS_HOST=$NAS_DDNS
    else
        error "DDNS ($NAS_DDNS) is not reachable"
        echo "Please check your network connection"
        exit 1
    fi
fi

# 3. 웹 UI 접근 테스트
info "Testing web interface..."
if curl -s --connect-timeout 5 "http://$NAS_HOST:5000" > /dev/null; then
    success "Web interface (http://$NAS_HOST:5000) is accessible"
else
    warning "Web interface may not be accessible"
fi

# 4. SSH 접근 테스트
info "Testing SSH access..."
if timeout 10 ssh -o ConnectTimeout=5 -o BatchMode=yes $NAS_USER@$NAS_HOST exit 2>/dev/null; then
    success "SSH access is available"
    SSH_AVAILABLE=true
else
    warning "SSH access requires authentication setup"
    info "To enable SSH: Control Panel → Terminal & SNMP → Enable SSH service"
    SSH_AVAILABLE=false
fi

# 5. Docker 서비스 확인 (SSH 가능한 경우)
if [ "$SSH_AVAILABLE" = true ]; then
    info "Checking Docker availability..."
    if ssh $NAS_USER@$NAS_HOST "which docker" > /dev/null 2>&1; then
        success "Docker is installed on NAS"
        
        # Docker 컨테이너 상태 확인
        RUNNING_CONTAINERS=$(ssh $NAS_USER@$NAS_HOST "docker ps --format 'table {{.Names}}\t{{.Status}}'" 2>/dev/null)
        if [ ! -z "$RUNNING_CONTAINERS" ]; then
            info "Running containers:"
            echo "$RUNNING_CONTAINERS"
        else
            info "No containers currently running"
        fi
    else
        warning "Docker not found - install Docker package from Package Center"
    fi
fi

# 6. 권장 다음 단계
echo ""
info "📋 Next Steps:"
echo "1. Install Docker package on NAS (if not installed)"
echo "2. Enable SSH service for automated deployment"
echo "3. Set up SSH key authentication:"
echo "   ssh-copy-id $NAS_USER@$NAS_HOST"
echo "4. Deploy Docker services:"
echo "   scp docker-configs/nas-docker-compose.yml $NAS_USER@$NAS_HOST:/volume1/"
echo "   ssh $NAS_USER@$NAS_HOST 'cd /volume1 && docker-compose up -d'"
echo ""

# 환경 변수 업데이트 제안
info "🔧 Update environment variables:"
echo "Edit snapcodex/.env file:"
echo "NAS_HOST=$NAS_HOST"
echo "POSTGRES_URL=postgresql://snapcodex:secure_password123@$NAS_HOST:5432/snapcodex"
echo "OLLAMA_BASE_URL=http://$NAS_HOST:11434"
echo "CHROMA_HOST=$NAS_HOST"

echo ""
success "NAS connection test completed!"
