#!/bin/bash

# Desinsight Workspace Docker Entrypoint
# 환경 자동 감지 및 서비스 시작

set -e

echo "🚀 Desinsight Workspace Container Starting..."
echo "============================================"

# 환경 변수 확인
DEVICE_TYPE=${DEVICE_TYPE:-"auto_detect"}
DEVICE_ROLE=${DEVICE_ROLE:-"auto_detect"}

echo "🔍 Environment Detection:"
echo "   Device Type: $DEVICE_TYPE"
echo "   Device Role: $DEVICE_ROLE"

# 시스템 리소스 감지
CPU_CORES=$(nproc)
MEMORY_MB=$(( $(grep MemTotal /proc/meminfo | awk '{print $2}') / 1024 ))
MEMORY_GB=$(( MEMORY_MB / 1024 ))

echo "   CPU Cores: $CPU_CORES"
echo "   Memory: ${MEMORY_GB}GB"

# 자동 역할 결정 (지정되지 않은 경우)
if [ "$DEVICE_ROLE" = "auto_detect" ]; then
    if [ "$MEMORY_GB" -ge 48 ]; then
        DEVICE_ROLE="inference_server"
        echo "   🧠 Auto-detected role: High-performance inference server"
    elif [ "$MEMORY_GB" -ge 24 ]; then
        DEVICE_ROLE="central_controller"
        echo "   🎛️ Auto-detected role: Central controller"
    elif [ "$MEMORY_GB" -ge 12 ]; then
        DEVICE_ROLE="embedding_server"
        echo "   ⚡ Auto-detected role: Embedding server"
    else
        DEVICE_ROLE="ui_server"
        echo "   🌐 Auto-detected role: UI server"
    fi
fi

# 작업 디렉토리 설정
cd /workspace

# 로그 디렉토리 생성
mkdir -p /workspace/logs

# Python 환경 확인
echo ""
echo "🐍 Python Environment:"
python3 --version
pip3 --version

# 설치된 패키지 확인
echo ""
echo "📦 Installed packages:"
pip3 list | grep -E "(ollama|fastapi|torch|transformers)" || echo "Core packages will be installed as needed"

# 역할별 서비스 시작
echo ""
echo "🎯 Starting services for role: $DEVICE_ROLE"
echo "============================================"

case $DEVICE_ROLE in
    "central_controller")
        echo "🎛️ Starting Central Controller services..."
        
        # 중앙 제어 서비스 시작
        if [ -f "/workspace/central-control/orchestrator/rag_orchestrator.py" ]; then
            echo "Starting RAG Orchestrator..."
            python3 /workspace/central-control/orchestrator/rag_orchestrator.py &
        fi
        
        # 웹 대시보드 서빙 (간단한 HTTP 서버)
        if [ -f "/workspace/central-control/dashboard/index.html" ]; then
            echo "Starting Web Dashboard on port 8000..."
            cd /workspace/central-control/dashboard
            python3 -m http.server 8000 --bind 0.0.0.0 &
            cd /workspace
        fi
        
        # API 서버 시작 (향후 구현)
        echo "Central Controller services started!"
        ;;
        
    "embedding_server")
        echo "⚡ Starting Embedding Server services..."
        
        # 임베딩 API 서버 시작
        echo "Starting Embedding API on port 8002..."
        # 향후 임베딩 서비스 구현
        python3 -c "
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class EmbeddingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'healthy', 'service': 'embedding'}).encode())
        else:
            self.send_response(404)
            self.end_headers()

server = HTTPServer(('0.0.0.0', 8002), EmbeddingHandler)
print('Embedding service running on port 8002')
server.serve_forever()
" &
        
        echo "Embedding Server services started!"
        ;;
        
    "inference_server")
        echo "🧠 Starting Inference Server services..."
        
        # Ollama 서비스 시작 (가능한 경우)
        if command -v ollama &> /dev/null; then
            echo "Starting Ollama service..."
            ollama serve &
            sleep 5
            
            # 기본 모델 풀 (없는 경우)
            ollama list | grep -q "llama3.2:3b" || ollama pull llama3.2:3b &
        fi
        
        # 추론 API 서버 시작
        echo "Starting Inference API on port 8003..."
        python3 -c "
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class InferenceHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'healthy', 'service': 'inference'}).encode())
        else:
            self.send_response(404)
            self.end_headers()

server = HTTPServer(('0.0.0.0', 8003), InferenceHandler)
print('Inference service running on port 8003')
server.serve_forever()
" &
        
        echo "Inference Server services started!"
        ;;
        
    "ui_server")
        echo "🌐 Starting UI Server services..."
        
        # 웹 UI 서버 시작
        echo "Starting Web UI on port 8004..."
        python3 -c "
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class UIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'healthy', 'service': 'ui'}).encode())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'''
            <html>
            <head><title>Desinsight UI Server</title></head>
            <body>
                <h1>🌐 Desinsight UI Server</h1>
                <p>UI Server is running successfully!</p>
                <p>Device Role: UI Server</p>
            </body>
            </html>
            ''')
        else:
            self.send_response(404)
            self.end_headers()

server = HTTPServer(('0.0.0.0', 8004), UIHandler)
print('UI service running on port 8004')
server.serve_forever()
" &
        
        echo "UI Server services started!"
        ;;
        
    "development")
        echo "🔧 Starting Development Environment..."
        
        # Jupyter Notebook 시작
        if command -v jupyter &> /dev/null; then
            echo "Starting Jupyter Notebook on port 8888..."
            jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root \
                --NotebookApp.token='' --NotebookApp.password='' &
        fi
        
        # 개발 서버 시작 (모든 포트)
        echo "Starting development services..."
        python3 -c "
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class DevHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'healthy', 'service': 'development'}).encode())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'''
            <html>
            <head><title>Desinsight Development</title></head>
            <body>
                <h1>🔧 Desinsight Development Environment</h1>
                <p>Development environment is running!</p>
                <ul>
                    <li><a href="http://localhost:8888">Jupyter Notebook</a></li>
                    <li><a href="/health">Health Check</a></li>
                </ul>
            </body>
            </html>
            ''')
        else:
            self.send_response(404)
            self.end_headers()

server = HTTPServer(('0.0.0.0', 8000), DevHandler)
print('Development service running on port 8000')
server.serve_forever()
" &
        
        echo "Development Environment services started!"
        ;;
        
    *)
        echo "❌ Unknown device role: $DEVICE_ROLE"
        echo "Available roles: central_controller, embedding_server, inference_server, ui_server, development"
        exit 1
        ;;
esac

# 모니터링 및 로그 출력
echo ""
echo "✅ All services started successfully!"
echo ""
echo "🌐 Service URLs:"
case $DEVICE_ROLE in
    "central_controller")
        echo "   📊 Dashboard: http://localhost:8000"
        echo "   🔗 API: http://localhost:8001"
        ;;
    "embedding_server")
        echo "   ⚡ Embedding API: http://localhost:8002"
        ;;
    "inference_server")
        echo "   🧠 Inference API: http://localhost:8003"
        ;;
    "ui_server")
        echo "   🌐 Web UI: http://localhost:8004"
        ;;
    "development")
        echo "   🔧 Development: http://localhost:8000"
        echo "   📓 Jupyter: http://localhost:8888"
        ;;
esac

echo ""
echo "📊 Container Status:"
echo "   Device Type: $DEVICE_TYPE"
echo "   Device Role: $DEVICE_ROLE"
echo "   CPU Cores: $CPU_CORES"
echo "   Memory: ${MEMORY_GB}GB"
echo "   Started: $(date)"

# 로그 파일에 시작 정보 기록
echo "[$(date)] Container started - Role: $DEVICE_ROLE, Memory: ${MEMORY_GB}GB" >> /workspace/logs/container.log

# 무한 대기 (컨테이너 유지)
echo ""
echo "🔄 Container is ready and running..."
echo "   Press Ctrl+C to stop"

# 신호 핸들러 설정
trap 'echo ""; echo "🛑 Shutting down services..."; exit 0' SIGTERM SIGINT

# 서비스 상태 모니터링 루프
while true; do
    # 프로세스 상태 확인
    if ! pgrep -f "python3" > /dev/null; then
        echo "⚠️ Service process stopped unexpectedly!"
    fi
    
    # 헬스체크 로그 (10분마다)
    if [ $(($(date +%s) % 600)) -eq 0 ]; then
        echo "[$(date)] Health check: Role=$DEVICE_ROLE, Memory=${MEMORY_GB}GB" >> /workspace/logs/container.log
    fi
    
    sleep 30
done 