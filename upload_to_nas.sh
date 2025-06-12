#!/bin/bash

echo "🚀 Desinsight Docker 이미지 NAS 업로드"
echo "======================================"

# 설정
NAS_HOST="192.168.219.175"
NAS_SHARE="volume1"
MOUNT_POINT="/tmp/nas_mount"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')

# 1. 마운트 포인트 생성
echo "📁 마운트 포인트 생성..."
sudo mkdir -p "$MOUNT_POINT"

# 2. SMB 마운트 (macOS)
echo "🔗 NAS SMB 마운트 중..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sudo mount -t smbfs "//$NAS_HOST/$NAS_SHARE" "$MOUNT_POINT"
else
    # Linux
    sudo mount -t cifs "//$NAS_HOST/$NAS_SHARE" "$MOUNT_POINT" -o username=admin,password=
fi

if [ $? -eq 0 ]; then
    echo "✅ NAS 마운트 성공!"
else
    echo "❌ NAS 마운트 실패!"
    exit 1
fi

# 3. Docker 이미지 디렉토리 생성
echo "📂 Docker 이미지 디렉토리 생성..."
sudo mkdir -p "$MOUNT_POINT/docker-images"
sudo mkdir -p "$MOUNT_POINT/docker-backups"

# 4. 이미지 저장 및 업로드
echo "💾 Docker 이미지 저장 중..."

# 모니터링 대시보드
if docker images | grep -q "desinsight/monitoring-dashboard"; then
    echo "📊 모니터링 대시보드 이미지 저장..."
    docker save desinsight/monitoring-dashboard:latest | gzip > "desinsight_monitoring_${TIMESTAMP}.tar.gz"
    sudo cp "desinsight_monitoring_${TIMESTAMP}.tar.gz" "$MOUNT_POINT/docker-images/"
    echo "✅ 모니터링 대시보드 업로드 완료"
fi

# 워크스페이스 (simple)
if docker images | grep -q "desinsight/workspace.*simple"; then
    echo "🏗️ 워크스페이스 (Simple) 이미지 저장..."
    docker save desinsight/workspace:simple | gzip > "desinsight_workspace_simple_${TIMESTAMP}.tar.gz"
    sudo cp "desinsight_workspace_simple_${TIMESTAMP}.tar.gz" "$MOUNT_POINT/docker-images/"
    echo "✅ 워크스페이스 (Simple) 업로드 완료"
fi

# 워크스페이스 (full)
if docker images | grep -q "desinsight/workspace.*latest"; then
    echo "🏗️ 워크스페이스 (Full) 이미지 저장..."
    docker save desinsight/workspace:latest | gzip > "desinsight_workspace_full_${TIMESTAMP}.tar.gz"
    sudo cp "desinsight_workspace_full_${TIMESTAMP}.tar.gz" "$MOUNT_POINT/docker-images/"
    echo "✅ 워크스페이스 (Full) 업로드 완료"
fi

# 5. 설정 파일 백업
echo "⚙️ 설정 파일 백업..."
tar -czf "desinsight_configs_${TIMESTAMP}.tar.gz" \
    docker-compose*.yml \
    Dockerfile* \
    requirements*.txt \
    *.sh \
    dashboard/ \
    --exclude="*.tar*" \
    --exclude="__pycache__" \
    --exclude=".git"

sudo cp "desinsight_configs_${TIMESTAMP}.tar.gz" "$MOUNT_POINT/docker-backups/"

# 6. 업로드 완료 정보
echo "📋 업로드 완료 정보:"
echo "  📍 NAS 위치: //$NAS_HOST/$NAS_SHARE/docker-images/"
echo "  📊 모니터링: desinsight_monitoring_${TIMESTAMP}.tar.gz"
echo "  🏗️ 워크스페이스: desinsight_workspace_*_${TIMESTAMP}.tar.gz"
echo "  ⚙️ 설정파일: desinsight_configs_${TIMESTAMP}.tar.gz"

# 7. 마운트 해제
echo "🔓 NAS 마운트 해제..."
sudo umount "$MOUNT_POINT"
sudo rmdir "$MOUNT_POINT"

# 8. 로컬 임시 파일 정리
echo "🧹 로컬 임시 파일 정리..."
rm -f desinsight_*.tar.gz

echo "🎉 NAS 업로드 완료!"
echo ""
echo "📖 다른 PC에서 사용법:"
echo "  1. NAS 마운트: mount -t smbfs //$NAS_HOST/$NAS_SHARE /mnt/nas"
echo "  2. 이미지 로드: docker load -i /mnt/nas/docker-images/desinsight_*.tar.gz"
echo "  3. 컨테이너 실행: docker run -d -p 5000:5000 desinsight/workspace:simple" 