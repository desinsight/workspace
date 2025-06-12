#!/bin/bash

# 색상 정의
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 로그 함수
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

# Ollama 서버 상태 확인
check_ollama() {
    if curl -s http://localhost:11434/api/tags > /dev/null; then
        return 0
    else
        return 1
    fi
}

# Ollama 서버 시작
start_ollama() {
    log "Starting Ollama server..."
    if command -v docker &> /dev/null; then
        # Docker로 Ollama 실행
        docker run -d --name ollama -p 11434:11434 ollama/ollama
        log "Ollama server started in Docker container"
    else
        error "Docker is not installed. Please install Docker first."
        exit 1
    fi
}

# 프론트엔드 의존성 설치 및 시작
start_frontend() {
    log "Installing frontend dependencies..."
    cd "$(dirname "$0")/.."
    npm install

    log "Starting frontend development server..."
    npm run dev
}

# 메인 실행
main() {
    log "Starting SnapCodex development environment..."

    # Ollama 서버 확인 및 시작
    if ! check_ollama; then
        warn "Ollama server is not running"
        start_ollama
    else
        log "Ollama server is already running"
    fi

    # Ollama 서버가 완전히 시작될 때까지 대기
    log "Waiting for Ollama server to be ready..."
    for i in {1..30}; do
        if check_ollama; then
            log "Ollama server is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            error "Ollama server failed to start"
            exit 1
        fi
        sleep 1
    done

    # 프론트엔드 시작
    start_frontend
}

# 스크립트 실행
main 