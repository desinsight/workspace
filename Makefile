# Desinsight Workspace Docker 관리 Makefile
# 5-Device + 3-NAS 분산 RAG 생태계

.PHONY: help build push pull deploy-* clean status logs monitor test

# 변수 설정
REGISTRY := desinsight
IMAGE_NAME := workspace
VERSION := latest
FULL_IMAGE := $(REGISTRY)/$(IMAGE_NAME):$(VERSION)

# Docker Compose 파일
COMPOSE_FILE := docker-compose.yml

# 기본 타겟 (help 표시)
help:
	@echo "🏗 Desinsight Workspace Docker 관리"
	@echo "=================================="
	@echo ""
	@echo "📦 이미지 관리:"
	@echo "  build         - 모든 이미지 빌드"
	@echo "  build-base    - 기본 워크스페이스 이미지만 빌드"
	@echo "  build-dev     - 개발 환경 이미지 빌드"
	@echo "  push          - 이미지를 레지스트리에 푸시"
	@echo "  pull          - 이미지를 레지스트리에서 풀"
	@echo ""
	@echo "🚀 배포 관리:"
	@echo "  deploy-single - 단일 디바이스 배포"
	@echo "  deploy-home   - HOME 환경 배포 (중앙제어+임베딩)"
	@echo "  deploy-office - OFFICE 환경 배포 (추론+UI)"
	@echo "  deploy-all    - 전체 생태계 배포"
	@echo "  deploy-dev    - 개발 환경 배포"
	@echo ""
	@echo "🔧 관리 도구:"
	@echo "  status        - 컨테이너 상태 확인"
	@echo "  logs          - 로그 확인"
	@echo "  monitor       - 대시보드 열기"
	@echo "  clean         - 정리"
	@echo "  test          - 시스템 테스트"

# ==========================================
# 이미지 빌드
# ==========================================

# 모든 이미지 빌드
build:
	@echo "🏗️ Building all Desinsight Workspace images..."
	docker build -t $(FULL_IMAGE) .
	docker build -t $(REGISTRY)/central-controller:$(VERSION) --target central-controller .
	docker build -t $(REGISTRY)/embedding-server:$(VERSION) --target embedding-server .
	docker build -t $(REGISTRY)/inference-server:$(VERSION) --target inference-server .
	docker build -t $(REGISTRY)/ui-server:$(VERSION) --target ui-server .
	docker build -t $(REGISTRY)/development:$(VERSION) --target development .
	@echo "✅ Build completed successfully!"

# 기본 워크스페이스만 빌드 (빠른 테스트용)
build-base:
	@echo "🏗️ Building base workspace image..."
	docker build -t $(FULL_IMAGE) --target base-workspace .
	@echo "✅ Base build completed!"

# 개발 환경 빌드
build-dev:
	@echo "🏗️ Building development environment..."
	docker build -t $(REGISTRY)/development:$(VERSION) --target development .
	@echo "✅ Development build completed!"

# 이미지 레지스트리에 푸시
push:
	@echo "📤 Pushing images to registry..."
	docker push $(FULL_IMAGE)
	docker push $(REGISTRY)/central-controller:$(VERSION)
	docker push $(REGISTRY)/embedding-server:$(VERSION)
	docker push $(REGISTRY)/inference-server:$(VERSION)
	docker push $(REGISTRY)/ui-server:$(VERSION)
	docker push $(REGISTRY)/development:$(VERSION)
	@echo "✅ Push completed!"

# 이미지 풀
pull:
	@echo "📥 Pulling images from registry..."
	docker pull $(FULL_IMAGE)
	@echo "✅ Pull completed!"

# ==========================================
# 배포 관리
# ==========================================

# 단일 디바이스 배포 (현재 디바이스에 맞는 환경 자동 감지)
deploy-single:
	@echo "📱 Single device deployment..."
	@./scripts/one_click_deploy.sh single
	@echo "✅ Single deployment completed!"
	@make monitor

# HOME 환경 배포 (중앙 제어 + 임베딩)
deploy-home:
	@echo "🏠 HOME environment deployment..."
	@./scripts/one_click_deploy.sh home
	@echo "✅ HOME deployment completed!"
	@make monitor

# OFFICE 환경 배포 (추론 + UI)
deploy-office:
	@echo "🏢 OFFICE environment deployment..."
	@./scripts/one_click_deploy.sh office
	@echo "✅ OFFICE deployment completed!"
	@make monitor

# 전체 생태계 배포
deploy-all:
	@echo "🌐 Full ecosystem deployment..."
	docker-compose -f $(COMPOSE_FILE) up -d
	@echo "✅ Full deployment completed!"
	@make status
	@make monitor

# 개발 환경 배포
deploy-dev:
	@echo "🔧 Development environment deployment..."
	docker run -d \
		--name desinsight-dev \
		-p 8000:8000 -p 8001:8001 -p 8002:8002 -p 8003:8003 -p 8004:8004 -p 8888:8888 \
		-v $(PWD):/workspace \
		-v $(PWD)/data:/workspace/data \
		--restart unless-stopped \
		$(REGISTRY)/development:$(VERSION)
	@echo "✅ Development deployment completed!"
	@echo "🔗 Jupyter: http://localhost:8888"

# ==========================================
# 관리 도구
# ==========================================

# 컨테이너 상태 확인
status:
	@echo "📊 Container Status:"
	@echo "===================="
	@docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Image}}" | grep desinsight || echo "No Desinsight containers running"
	@echo ""
	@echo "💾 Volume Usage:"
	@echo "==============="
	@docker system df -v | grep -E "(desinsight|workspace)" || echo "No Desinsight volumes"

# 로그 확인
logs:
	@echo "📜 Container Logs:"
	@echo "=================="
	@if [ -f $(COMPOSE_FILE) ]; then \
		docker-compose -f $(COMPOSE_FILE) logs -f --tail=50; \
	else \
		docker logs -f desinsight-workspace 2>/dev/null || \
		docker logs -f desinsight-dev 2>/dev/null || \
		echo "No running containers found"; \
	fi

# 특정 서비스 로그
logs-central:
	docker-compose -f $(COMPOSE_FILE) logs -f central-controller

logs-embedding:
	docker-compose -f $(COMPOSE_FILE) logs -f embedding-server

logs-inference:
	docker-compose -f $(COMPOSE_FILE) logs -f inference-server

logs-ui:
	docker-compose -f $(COMPOSE_FILE) logs -f ui-server

# 대시보드 열기
monitor:
	@echo "📊 Opening monitoring dashboards..."
	@open http://localhost:8000 2>/dev/null || echo "Dashboard URL: http://localhost:8000"
	@open http://localhost:3001 2>/dev/null || echo "Grafana URL: http://localhost:3001 (admin/desinsight2024)"

# ==========================================
# 테스트 및 디버깅
# ==========================================

# 시스템 테스트
test:
	@echo "🧪 Running system tests..."
	@echo "Testing container connectivity..."
	@docker run --rm --network container:desinsight-central-controller \
		curlimages/curl:latest curl -f http://localhost:8000/health || echo "Central controller test failed"
	@echo "✅ Basic tests completed!"

# 개발용 쉘 접속
shell:
	@echo "🐚 Opening development shell..."
	@docker exec -it desinsight-dev /bin/bash 2>/dev/null || \
	 docker exec -it desinsight-central-controller /bin/bash 2>/dev/null || \
	 echo "No running container found for shell access"

# 설정 확인
config:
	@echo "⚙️ Current Configuration:"
	@echo "========================="
	@echo "Registry: $(REGISTRY)"
	@echo "Image: $(IMAGE_NAME)"
	@echo "Version: $(VERSION)"
	@echo "Full Image: $(FULL_IMAGE)"
	@echo ""
	@echo "🐳 Docker Info:"
	@docker version --format "Docker: {{.Server.Version}}"
	@docker-compose version --short 2>/dev/null || echo "docker-compose not available"

# ==========================================
# 정리 작업
# ==========================================

# 중지 및 정리
stop:
	@echo "🛑 Stopping all containers..."
	@docker-compose -f $(COMPOSE_FILE) down 2>/dev/null || echo "Compose not running"
	@docker stop $$(docker ps -q --filter "name=desinsight") 2>/dev/null || echo "No containers to stop"

# 완전 정리
clean: stop
	@echo "🧹 Cleaning up containers, images, and volumes..."
	@docker container prune -f
	@docker image prune -f
	@docker volume prune -f
	@echo "✅ Cleanup completed!"

# 개발 데이터만 정리 (프로덕션 데이터 보존)
clean-dev:
	@echo "🧹 Cleaning development data only..."
	@docker stop desinsight-dev 2>/dev/null || true
	@docker rm desinsight-dev 2>/dev/null || true
	@echo "✅ Development cleanup completed!"

# 전체 시스템 리셋 (주의!)
reset: clean
	@echo "⚠️ FULL SYSTEM RESET - This will remove ALL Desinsight data!"
	@read -p "Are you sure? (yes/no): " confirm && [ "$$confirm" = "yes" ]
	@docker-compose -f $(COMPOSE_FILE) down -v
	@docker rmi $$(docker images -q desinsight/*) 2>/dev/null || true
	@echo "🔄 System reset completed!"

# ==========================================
# 백업 및 복구
# ==========================================

# 데이터 백업
backup:
	@echo "💾 Creating backup..."
	@mkdir -p backups/$$(date +%Y%m%d_%H%M%S)
	@docker run --rm \
		-v $$(docker volume ls -q | grep desinsight):latest \
		-v $(PWD)/backups/$$(date +%Y%m%d_%H%M%S):/backup \
		alpine tar czf /backup/desinsight_volumes.tar.gz /data
	@echo "✅ Backup completed in backups/ directory"

# 백업 복구
restore:
	@echo "📥 Restoring from backup..."
	@echo "Available backups:"
	@ls -la backups/ 2>/dev/null || echo "No backups found"
	@read -p "Enter backup directory name: " backup_dir && \
	docker run --rm \
		-v $$(docker volume ls -q | grep desinsight):latest \
		-v $(PWD)/backups/$$backup_dir:/backup \
		alpine tar xzf /backup/desinsight_volumes.tar.gz -C /
	@echo "✅ Restore completed!"

# ==========================================
# 자주 사용하는 조합 명령
# ==========================================

# 완전 재배포 (빌드 + 배포)
redeploy: build deploy-all

# 빠른 시작 (개발용)
quick-start: build-dev deploy-dev

# 프로덕션 배포
production: build push deploy-all backup 