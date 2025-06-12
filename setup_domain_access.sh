#!/bin/bash

# 🌐 nas.snapcodex.com 도메인 접속 설정 스크립트
# NAS 서버에서 실행하여 외부 도메인 접속을 활성화합니다

set -e

# 색상 코드
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# 로고
echo -e "${CYAN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║           🌐 nas.snapcodex.com 도메인 접속 설정           ║
║              실시간 모니터링 대시보드                     ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

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

# 현재 상태 확인
check_current_status() {
    print_header "📊 현재 상태 확인"
    
    print_step "도메인 DNS 해석 확인..."
    DOMAIN_IP=$(nslookup nas.snapcodex.com | grep "Address:" | tail -1 | awk '{print $2}')
    print_info "nas.snapcodex.com → $DOMAIN_IP"
    
    print_step "로컬 NAS IP 확인..."
    LOCAL_IP="192.168.219.175"
    print_info "로컬 NAS IP → $LOCAL_IP"
    
    print_step "포트 5004 상태 확인..."
    if netstat -an | grep -q ":5004.*LISTEN"; then
        print_success "포트 5004가 로컬에서 리스닝 중입니다"
    else
        print_warning "포트 5004가 리스닝 상태가 아닙니다"
    fi
}

# 방화벽 설정
setup_firewall() {
    print_header "🔥 방화벽 설정"
    
    print_step "현재 방화벽 상태 확인..."
    
    # macOS 방화벽 확인
    if [[ "$OSTYPE" == "darwin"* ]]; then
        print_info "macOS 방화벽 설정:"
        sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate || true
        
        print_step "포트 5004 허용 설정..."
        echo "sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/bin/python3"
        echo "sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblockapp /usr/bin/python3"
        
    # Linux 방화벽 확인
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_info "Linux 방화벽 설정:"
        
        # UFW 확인
        if command -v ufw &> /dev/null; then
            print_step "UFW로 포트 5004 허용..."
            echo "sudo ufw allow 5004/tcp"
            echo "sudo ufw reload"
        fi
        
        # iptables 확인
        if command -v iptables &> /dev/null; then
            print_step "iptables로 포트 5004 허용..."
            echo "sudo iptables -A INPUT -p tcp --dport 5004 -j ACCEPT"
            echo "sudo iptables-save"
        fi
    fi
}

# 포트포워딩 설정 가이드
setup_port_forwarding() {
    print_header "🔀 포트포워딩 설정 가이드"
    
    print_step "라우터 설정이 필요합니다:"
    echo ""
    echo -e "${CYAN}1. 라우터 관리 페이지 접속:${NC}"
    echo "   http://192.168.219.1 (일반적인 게이트웨이)"
    echo ""
    echo -e "${CYAN}2. 포트포워딩 설정:${NC}"
    echo "   외부 포트: 5004"
    echo "   내부 IP: 192.168.219.175"
    echo "   내부 포트: 5004"
    echo "   프로토콜: TCP"
    echo ""
    echo -e "${CYAN}3. 방화벽 설정:${NC}"
    echo "   포트 5004 TCP 허용"
    echo ""
    
    print_warning "라우터 설정은 관리자 권한이 필요합니다"
}

# 리버스 프록시 설정
setup_reverse_proxy() {
    print_header "🔄 리버스 프록시 설정 (권장)"
    
    print_step "Nginx 리버스 프록시 설정 생성..."
    
    cat > nginx_monitoring.conf << 'EOF'
# /etc/nginx/sites-available/monitoring
server {
    listen 80;
    server_name nas.snapcodex.com;
    
    # HTTP to HTTPS 리다이렉트 (선택사항)
    # return 301 https://$server_name$request_uri;
    
    location / {
        proxy_pass http://192.168.219.175:5004;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket 지원 (필요시)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # API 엔드포인트
    location /api/ {
        proxy_pass http://192.168.219.175:5004/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
    
    print_success "nginx_monitoring.conf 파일이 생성되었습니다"
    
    print_step "Nginx 설정 적용 명령어:"
    echo "sudo cp nginx_monitoring.conf /etc/nginx/sites-available/monitoring"
    echo "sudo ln -s /etc/nginx/sites-available/monitoring /etc/nginx/sites-enabled/"
    echo "sudo nginx -t"
    echo "sudo systemctl reload nginx"
}

# SSL 인증서 설정
setup_ssl() {
    print_header "🔒 SSL 인증서 설정 (HTTPS)"
    
    print_step "Let's Encrypt 인증서 설정:"
    echo "sudo apt install certbot python3-certbot-nginx"
    echo "sudo certbot --nginx -d nas.snapcodex.com"
    
    print_step "SSL 인증서 자동 갱신:"
    echo "sudo crontab -e"
    echo "# 매월 1일 새벽 2시에 인증서 갱신"
    echo "0 2 1 * * /usr/bin/certbot renew --quiet"
}

# 모니터링 서버 도메인 지원 업데이트
update_monitoring_server() {
    print_header "🔧 모니터링 서버 도메인 지원 업데이트"
    
    print_step "서버 설정 업데이트 중..."
    
    # enhanced_realtime_server.py 백업
    if [ -f "enhanced_realtime_server.py" ]; then
        cp enhanced_realtime_server.py enhanced_realtime_server.py.backup
        print_success "기존 서버 파일 백업 완료"
    fi
    
    print_step "도메인 기반 접속을 위한 CORS 설정 추가..."
    
    cat > domain_cors_patch.py << 'EOF'
# CORS 헤더 추가 패치
def add_cors_headers(self):
    """CORS 헤더 추가"""
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    self.send_header('Access-Control-Allow-Credentials', 'true')

# 도메인 접속 허용 설정
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '192.168.219.175',
    'nas.snapcodex.com'
]
EOF
    
    print_success "CORS 패치 파일 생성 완료"
}

# 접속 테스트
test_domain_access() {
    print_header "🧪 도메인 접속 테스트"
    
    print_step "로컬 접속 테스트..."
    if curl -s --connect-timeout 5 "http://192.168.219.175:5004" | grep -q "Desinsight"; then
        print_success "로컬 접속 정상"
    else
        print_error "로컬 접속 실패"
    fi
    
    print_step "도메인 접속 테스트..."
    if curl -s --connect-timeout 10 "http://nas.snapcodex.com:5004" | grep -q "Desinsight"; then
        print_success "도메인 접속 정상"
    else
        print_warning "도메인 접속 실패 - 포트포워딩 설정 필요"
    fi
}

# 접속 URL 정보 출력
show_access_urls() {
    print_header "🌐 접속 URL 정보"
    
    echo -e "${CYAN}로컬 네트워크 접속:${NC}"
    echo "  http://192.168.219.175:5004"
    echo ""
    
    echo -e "${CYAN}도메인 접속 (포트포워딩 설정 후):${NC}"
    echo "  http://nas.snapcodex.com:5004"
    echo ""
    
    echo -e "${CYAN}리버스 프록시 설정 후:${NC}"
    echo "  http://nas.snapcodex.com"
    echo "  https://nas.snapcodex.com (SSL 설정 후)"
    echo ""
    
    echo -e "${CYAN}API 엔드포인트:${NC}"
    echo "  http://nas.snapcodex.com:5004/api/devices"
    echo "  http://nas.snapcodex.com:5004/api/nas"
    echo "  http://nas.snapcodex.com:5004/api/heartbeat"
}

# 메인 실행
main() {
    case "${1:-all}" in
        "status")
            check_current_status
            ;;
        "firewall")
            setup_firewall
            ;;
        "portforward")
            setup_port_forwarding
            ;;
        "proxy")
            setup_reverse_proxy
            ;;
        "ssl")
            setup_ssl
            ;;
        "update")
            update_monitoring_server
            ;;
        "test")
            test_domain_access
            ;;
        "urls")
            show_access_urls
            ;;
        "all")
            check_current_status
            setup_firewall
            setup_port_forwarding
            setup_reverse_proxy
            update_monitoring_server
            show_access_urls
            ;;
        *)
            echo "사용법: $0 [status|firewall|portforward|proxy|ssl|update|test|urls|all]"
            exit 1
            ;;
    esac
}

# 스크립트 실행
main "$@"

print_header "🎉 도메인 설정 완료"
print_success "nas.snapcodex.com 도메인 접속 설정이 완료되었습니다!"
print_info "포트포워딩 설정 후 외부에서 접속 가능합니다"
print_info "리버스 프록시 설정으로 포트 없이 접속할 수 있습니다" 