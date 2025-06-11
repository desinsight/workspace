#!/bin/bash

echo "🔧 SnapCodex Development Environment Setup"
echo "Setting up complete development environment for Desinsight..."

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 함수: 성공 메시지
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# 함수: 에러 메시지
error() {
    echo -e "${RED}❌ $1${NC}"
}

# 함수: 정보 메시지
info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# 함수: 경고 메시지
warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# 1. 기본 도구 확인
info "Checking required tools..."

# Python 확인
if command -v python3 &> /dev/null; then
    success "Python3 is installed: $(python3 --version)"
else
    error "Python3 is not installed!"
    exit 1
fi

# Git 확인
if command -v git &> /dev/null; then
    success "Git is installed: $(git --version)"
else
    error "Git is not installed!"
    exit 1
fi

# 2. 프로젝트 디렉토리 설정
WORKSPACE_DIR="$HOME/workspace"
SNAPCODEX_DIR="$WORKSPACE_DIR/snapcodex"

if [ ! -d "$WORKSPACE_DIR" ]; then
    info "Creating workspace directory..."
    mkdir -p "$WORKSPACE_DIR"
    success "Workspace directory created"
fi

cd "$WORKSPACE_DIR"

# 3. SnapCodex 환경 설정
if [ -d "$SNAPCODEX_DIR" ]; then
    info "SnapCodex directory exists, setting up environment..."
    cd "$SNAPCODEX_DIR"
    
    # Python 가상환경 설정
    if [ ! -d "venv" ]; then
        info "Creating Python virtual environment..."
        python3 -m venv venv
        success "Virtual environment created"
    fi
    
    # 가상환경 활성화
    source venv/bin/activate
    success "Virtual environment activated"
    
    # 의존성 설치
    if [ -f "requirements.txt" ]; then
        info "Installing Python dependencies..."
        pip install --upgrade pip
        pip install -r requirements.txt
        success "Dependencies installed"
    else
        warning "requirements.txt not found"
    fi
    
    # 환경 변수 설정
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            info "Creating .env file from template..."
            cp .env.example .env
            warning "Please edit .env file with your actual credentials"
        else
            error ".env.example not found"
        fi
    else
        success ".env file already exists"
    fi
    
else
    error "SnapCodex directory not found in workspace"
    exit 1
fi

# 4. Git 설정 확인
info "Checking Git configuration..."
if [ -z "$(git config --global user.name)" ]; then
    warning "Git user.name not set. Please run:"
    echo "git config --global user.name 'Your Name'"
fi

if [ -z "$(git config --global user.email)" ]; then
    warning "Git user.email not set. Please run:"
    echo "git config --global user.email 'ceo@desinsight.com'"
fi

# 5. Notion 연결 테스트
info "Testing Notion API connection..."
cd "$SNAPCODEX_DIR"
if [ -f "core/notion_manager.py" ] && [ -f ".env" ]; then
    python core/notion_manager.py
else
    warning "Cannot test Notion connection - files missing"
fi

# 6. Docker 확인 (선택사항)
if command -v docker &> /dev/null; then
    success "Docker is available: $(docker --version)"
    if command -v docker-compose &> /dev/null; then
        success "Docker Compose is available: $(docker-compose --version)"
    else
        warning "Docker Compose not found"
    fi
else
    warning "Docker not found - NAS deployment will be limited"
fi

# 7. 개발 도구 확인
info "Checking development tools..."

if command -v cursor &> /dev/null; then
    success "Cursor AI is available"
elif command -v code &> /dev/null; then
    success "VS Code is available"
else
    warning "No supported IDE found (Cursor AI or VS Code recommended)"
fi

# 8. MCP 설정 확인
MCP_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
if [ -f "$MCP_CONFIG" ]; then
    success "Claude MCP configuration found"
else
    warning "Claude MCP configuration not found"
    info "Run MCP setup if you want Claude file access"
fi

# 9. 스크립트 실행 권한 설정
info "Setting script permissions..."
chmod +x scripts/*.sh 2>/dev/null || true
success "Script permissions updated"

# 10. 완료 메시지
echo ""
echo "🎉 SnapCodex Development Environment Setup Complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Edit .env file with your actual Notion tokens"
echo "2. Test Notion connection: cd snapcodex && python core/notion_manager.py"
echo "3. Start development: cursor $WORKSPACE_DIR"
echo "4. For NAS setup: review docker-configs/nas-docker-compose.yml"
echo ""
echo "📁 Project Structure:"
echo "   ~/workspace/"
echo "   ├── snapcodex/          # Main project"
echo "   ├── docker-configs/     # NAS deployment configs"
echo "   ├── scripts/           # Automation scripts"
echo "   └── README.md          # Documentation"
echo ""
echo "🔧 Available Scripts:"
echo "   ./scripts/home_to_nas_sync.sh     # Backup to NAS"
echo "   ./scripts/office_from_nas_sync.sh # Restore from NAS"
echo "   ./scripts/setup.sh               # This setup script"
echo ""
echo "Happy coding! 🚀"
