#!/bin/bash

echo "🏢 Office from NAS sync script"
echo "🔄 Pulling latest changes from NAS..."

# NAS 주소 설정 (snapcodex.synology.me)
NAS_HOST=${NAS_HOST:-"192.168.219.175"}
NAS_USER=${NAS_USER:-"admin"}
NAS_DDNS="snapcodex.synology.me"
WORKSPACE_PATH="$HOME/workspace"
NAS_WORKSPACE_PATH="/volume1/workspace"

# 1. 디렉토리 생성 (존재하지 않는 경우)
mkdir -p "$WORKSPACE_PATH"

# 2. Git 클론 또는 풀
if [ -d "$WORKSPACE_PATH/.git" ]; then
    echo "📁 Git repository exists, pulling latest changes..."
    cd "$WORKSPACE_PATH"
    git pull origin main || echo "Git pull failed, using rsync"
else
    echo "📁 Cloning repository from NAS..."
    git clone "git@$NAS_HOST:desinsight/workspace.git" "$WORKSPACE_PATH" || echo "Git clone failed, using rsync"
fi

# 3. rsync 동기화 (Git이 실패한 경우의 백업)
echo "🔄 rsync synchronization from NAS..."
rsync -avz \
    --exclude='.git/' \
    --exclude='node_modules/' \
    --exclude='__pycache__/' \
    --exclude='*.log' \
    "$NAS_USER@$NAS_HOST:$NAS_WORKSPACE_PATH/" "$WORKSPACE_PATH/"

if [ $? -eq 0 ]; then
    echo "✅ Office sync completed successfully!"
else
    echo "❌ Office sync failed!"
    exit 1
fi

# 4. 환경 설정
cd "$WORKSPACE_PATH"
echo "🔧 Setting up environment..."

# Python 가상환경 설정 (snapcodex)
if [ -d "snapcodex" ]; then
    cd snapcodex
    if [ ! -d "venv" ]; then
        echo "🐍 Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    echo "📦 Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt || echo "Dependency installation failed"
    cd ..
fi

# 5. Cursor AI 시작
echo "🚀 Opening Cursor AI..."
if command -v cursor &> /dev/null; then
    cursor "$WORKSPACE_PATH"
else
    echo "Cursor AI not found, opening VS Code instead..."
    code "$WORKSPACE_PATH" || echo "No IDE found"
fi

echo "🎯 Office setup mission completed!"
echo "📝 Remember to run Notion connection test:"
echo "cd snapcodex && python core/notion_manager.py"
