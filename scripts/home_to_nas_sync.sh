#!/bin/bash

echo "🏠 Home to NAS sync script"
echo "🔄 Syncing workspace to NAS..."

# NAS 주소 설정 (snapcodex.synology.me)
NAS_HOST=${NAS_HOST:-"192.168.219.175"}
NAS_USER=${NAS_USER:-"admin"}
NAS_DDNS="snapcodex.synology.me"
WORKSPACE_PATH="$HOME/workspace"
NAS_WORKSPACE_PATH="/volume1/workspace"

# 1. Git 백업
echo "📁 Git repository backup..."
cd "$WORKSPACE_PATH"
git add .
git commit -m "auto: backup from home $(date '+%Y-%m-%d %H:%M:%S')" || echo "No changes to commit"
git push origin main || echo "Git push failed - will use rsync backup"

# 2. rsync 동기화
echo "🔄 rsync synchronization..."
rsync -avz --delete \
    --exclude='.git/' \
    --exclude='node_modules/' \
    --exclude='__pycache__/' \
    --exclude='.env' \
    --exclude='*.log' \
    "$WORKSPACE_PATH/" "$NAS_USER@$NAS_HOST:$NAS_WORKSPACE_PATH/"

if [ $? -eq 0 ]; then
    echo "✅ Sync to NAS completed successfully!"
else
    echo "❌ Sync to NAS failed!"
    exit 1
fi

# 3. 백업 확인
echo "🔍 Verifying backup..."
ssh "$NAS_USER@$NAS_HOST" "ls -la $NAS_WORKSPACE_PATH/" || echo "SSH verification failed"

echo "🎯 Home backup mission completed!"
