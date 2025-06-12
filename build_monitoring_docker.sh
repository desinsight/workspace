#!/bin/bash
# build_monitoring_docker.sh - 실시간 모니터링 시스템 Docker 빌드 스크립트

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로그 함수
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 프로젝트 정보
PROJECT_NAME="desinsight-monitoring"
IMAGE_NAME="desinsight/monitoring-dashboard"
VERSION="1.0.0"
DOCKERFILE="Dockerfile.monitoring"
COMPOSE_FILE="docker-compose.monitoring.yml"

log_info "🚀 Desinsight 실시간 모니터링 시스템 Docker 빌드 시작"
log_info "프로젝트: $PROJECT_NAME"
log_info "이미지명: $IMAGE_NAME:$VERSION"

# 1. 기존 컨테이너 정리
log_info "🧹 기존 컨테이너 정리 중..."
docker-compose -f $COMPOSE_FILE down --remove-orphans 2>/dev/null || true
docker container prune -f 2>/dev/null || true

# 2. Docker 이미지 빌드
log_info "🔨 Docker 이미지 빌드 중..."
docker build -f $DOCKERFILE -t $IMAGE_NAME:$VERSION -t $IMAGE_NAME:latest .

if [ $? -eq 0 ]; then
    log_success "Docker 이미지 빌드 완료: $IMAGE_NAME:$VERSION"
else
    log_error "Docker 이미지 빌드 실패"
    exit 1
fi

# 3. 이미지 정보 확인
log_info "📋 빌드된 이미지 정보:"
docker images | grep desinsight/monitoring

# 4. Docker Compose로 서비스 시작
log_info "🚀 Docker Compose로 서비스 시작 중..."
docker-compose -f $COMPOSE_FILE up -d

if [ $? -eq 0 ]; then
    log_success "서비스 시작 완료"
else
    log_error "서비스 시작 실패"
    exit 1
fi

# 5. 서비스 상태 확인
log_info "⏳ 서비스 시작 대기 중 (30초)..."
sleep 30

log_info "🔍 서비스 상태 확인:"
docker-compose -f $COMPOSE_FILE ps

# 6. 헬스체크
log_info "🏥 헬스체크 수행 중..."
HEALTH_CHECK_URL="http://localhost:5004/api/devices"

for i in {1..5}; do
    if curl -s -f $HEALTH_CHECK_URL > /dev/null; then
        log_success "헬스체크 성공: $HEALTH_CHECK_URL"
        break
    else
        log_warning "헬스체크 시도 $i/5 실패, 10초 후 재시도..."
        sleep 10
    fi
    
    if [ $i -eq 5 ]; then
        log_error "헬스체크 최종 실패"
        log_info "컨테이너 로그 확인:"
        docker-compose -f $COMPOSE_FILE logs --tail=20
        exit 1
    fi
done

# 7. 접속 정보 출력
log_success "🎉 Desinsight 실시간 모니터링 시스템 배포 완료!"
echo ""
echo "📡 접속 정보:"
echo "  - 실시간 모니터링 대시보드: http://localhost:5004"
echo "  - 통합 대시보드 (백업): http://localhost:5003"
echo "  - 간단 대시보드 (백업): http://localhost:5002"
echo ""
echo "🔧 관리 명령어:"
echo "  - 로그 확인: docker-compose -f $COMPOSE_FILE logs -f"
echo "  - 서비스 중지: docker-compose -f $COMPOSE_FILE down"
echo "  - 서비스 재시작: docker-compose -f $COMPOSE_FILE restart"
echo "  - 컨테이너 상태: docker-compose -f $COMPOSE_FILE ps"
echo ""
echo "🐳 Docker 이미지:"
echo "  - 이미지명: $IMAGE_NAME:$VERSION"
echo "  - 크기: $(docker images $IMAGE_NAME:$VERSION --format "table {{.Size}}" | tail -n 1)"
echo ""

# 8. 브라우저 열기 (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    log_info "🌐 브라우저에서 대시보드 열기..."
    open "http://localhost:5004"
fi

log_success "✅ 모든 작업 완료!" 