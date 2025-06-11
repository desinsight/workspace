#!/usr/bin/env python3
"""
Desinsight 분산 RAG 생태계 - HOME iMac 중앙 제어 서버 설정
5-Device + 3-NAS 아키텍처의 핵심 오케스트레이터
"""

import os
import json
import platform
import psutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class HomeImacSetup:
    def __init__(self):
        self.device_name = "HOME-iMac-i7-64GB"
        self.role = "central_controller"
        self.workspace = Path.home() / 'workspace'
        self.ecosystem_config = self.get_ecosystem_config()
        
        print("🏠 Desinsight 분산 RAG 생태계 중앙 제어 서버")
        print("=" * 60)
        print(f"📱 디바이스: {self.device_name}")
        print(f"🎯 역할: {self.role}")
        print(f"💻 CPU: {platform.processor()}")
        print(f"🧠 메모리: {round(psutil.virtual_memory().total/(1024**3))}GB")
        print(f"💾 디스크: {round(psutil.disk_usage('/').free/(1024**3))}GB 여유")
        
    def get_ecosystem_config(self) -> Dict:
        """분산 생태계 전체 설정"""
        return {
            "devices": {
                "HOME_iMac_i7_64GB": {
                    "role": "central_controller",
                    "services": ["orchestrator", "dashboard", "data_manager", "dev_server"],
                    "status": "current",
                    "ip": "192.168.219.103",
                    "ports": {"dashboard": 8080, "api": 8000, "monitoring": 3000}
                },
                "HOME_MacMini_M2Pro_32GB": {
                    "role": "embedding_server", 
                    "services": ["embedding_generator", "batch_processor", "model_trainer"],
                    "status": "pending",
                    "ip": "192.168.219.104",
                    "ports": {"embedding_api": 8001, "training": 8002}
                },
                "OFFICE_iMac_i7_40GB": {
                    "role": "ui_server",
                    "services": ["search_ui", "monitoring_dashboard", "collaboration"],
                    "status": "pending", 
                    "ip": "office.desinsight.local",
                    "ports": {"ui": 8082, "monitoring": 3001}
                },
                "OFFICE_MacStudio_M4Pro_64GB": {
                    "role": "inference_server",
                    "services": ["high_performance_inference", "api_gateway", "analysis"],
                    "status": "pending",
                    "ip": "studio.desinsight.local", 
                    "ports": {"inference": 8003, "api": 8004}
                },
                "MOBILE_iPhone_MacBook": {
                    "role": "client",
                    "services": ["mobile_app", "field_data_collection"],
                    "status": "pending"
                }
            },
            "nas_systems": {
                "SnapCodex_NAS": {
                    "purpose": "project_data",
                    "ip": "192.168.219.175",
                    "priority": "realtime_processing"
                },
                "Desinsight2_NAS": {
                    "purpose": "central_storage", 
                    "ip": "nas2.desinsight.local",
                    "priority": "high_availability"
                },
                "Office_Desinsight_NAS": {
                    "purpose": "backup_storage",
                    "ip": "desinsight.synology.me:5001", 
                    "priority": "disaster_recovery"
                }
            }
        }
    
    def setup_central_controller(self):
        """중앙 제어 서버 전체 설정"""
        print("\n🔧 중앙 제어 서버 설정 시작...")
        
        # 1. 디렉토리 구조 생성
        self.create_controller_directories()
        
        # 2. 설정 파일 생성
        self.create_config_files()
        
        # 3. 오케스트레이터 서비스 설정
        self.setup_orchestrator_service()
        
        # 4. 웹 대시보드 기본 설정
        self.setup_web_dashboard()
        
        # 5. 디바이스 연결 관리자 설정
        self.setup_device_manager()
        
        # 6. 상태 모니터링 설정
        self.setup_monitoring()
        
        print("✅ 중앙 제어 서버 설정 완료!")
        self.print_next_steps()
        
    def create_controller_directories(self):
        """컨트롤러 디렉토리 구조 생성"""
        print("\n📁 디렉토리 구조 생성...")
        
        dirs = [
            self.workspace / 'central-control',
            self.workspace / 'central-control' / 'orchestrator',
            self.workspace / 'central-control' / 'dashboard', 
            self.workspace / 'central-control' / 'monitoring',
            self.workspace / 'central-control' / 'configs',
            self.workspace / 'device-configs',
            self.workspace / 'logs',
            self.workspace / 'shared-data'
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ {dir_path}")
            
    def create_config_files(self):
        """생태계 설정 파일 생성"""
        print("\n⚙️ 설정 파일 생성...")
        
        # 생태계 전체 설정
        ecosystem_config_path = self.workspace / 'central-control' / 'configs' / 'ecosystem.json'
        with open(ecosystem_config_path, 'w', encoding='utf-8') as f:
            json.dump(self.ecosystem_config, f, ensure_ascii=False, indent=2)
        print(f"  ✅ 생태계 설정: {ecosystem_config_path}")
        
        # HOME iMac 전용 설정
        home_imac_config = {
            "device_info": {
                "name": "HOME-iMac-i7-64GB",
                "role": "central_controller",
                "cpu": platform.processor(),
                "memory_gb": round(psutil.virtual_memory().total/(1024**3)),
                "priority": "coordination"
            },
            "services": {
                "rag_orchestrator": {"port": 8000, "workers": 4},
                "web_dashboard": {"port": 8080, "theme": "dark"},
                "data_manager": {"port": 8005, "sync_interval": 300},
                "monitoring_hub": {"port": 3000, "alert_threshold": 80}
            },
            "performance": {
                "max_workers": 8,
                "memory_allocation_gb": 45,
                "cpu_threads": 16,
                "concurrent_connections": 100
            },
            "network": {
                "internal_ip": "192.168.219.103",
                "external_access": True,
                "ssl_enabled": False,
                "cors_origins": ["*"]
            }
        }
        
        home_config_path = self.workspace / 'device-configs' / 'home_imac_config.json'
        with open(home_config_path, 'w', encoding='utf-8') as f:
            json.dump(home_imac_config, f, ensure_ascii=False, indent=2)
        print(f"  ✅ HOME iMac 설정: {home_config_path}")
        
    def setup_orchestrator_service(self):
        """RAG 오케스트레이터 서비스 설정"""
        print("\n🎼 RAG 오케스트레이터 설정...")
        
        orchestrator_code = '''#!/usr/bin/env python3
"""
Desinsight RAG 오케스트레이터 - 분산 시스템 조율
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

class RAGOrchestrator:
    def __init__(self):
        self.config_path = Path.home() / 'workspace' / 'central-control' / 'configs' / 'ecosystem.json'
        self.devices = self.load_ecosystem_config()
        self.status = {"started_at": datetime.now().isoformat()}
        
    def load_ecosystem_config(self) -> Dict:
        """생태계 설정 로드"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    async def health_check_devices(self):
        """모든 디바이스 상태 확인"""
        print("🔍 디바이스 상태 확인 중...")
        results = {}
        
        for device_name, device_config in self.devices.get('devices', {}).items():
            if device_config['status'] == 'current':
                results[device_name] = {"status": "active", "role": device_config['role']}
            else:
                results[device_name] = {"status": "pending", "role": device_config['role']}
                
        return results
    
    async def coordinate_rag_request(self, query: str) -> Dict:
        """RAG 요청 분산 처리 조율"""
        print(f"🎯 RAG 요청 조율: {query}")
        
        # 1. 임베딩 서버에 벡터 검색 요청
        # 2. 추론 서버에 LLM 생성 요청  
        # 3. 결과 취합 및 반환
        
        return {
            "query": query,
            "coordinated_by": "HOME_iMac_Controller",
            "timestamp": datetime.now().isoformat(),
            "status": "coordinated"
        }
    
    def start_orchestrator(self):
        """오케스트레이터 시작"""
        print("🎼 RAG 오케스트레이터 시작됨")
        print(f"📊 관리 중인 디바이스: {len(self.devices.get('devices', {}))}")
        print(f"🗄️ 연결된 NAS: {len(self.devices.get('nas_systems', {}))}")
        
if __name__ == "__main__":
    orchestrator = RAGOrchestrator()
    orchestrator.start_orchestrator()
'''
        
        orchestrator_path = self.workspace / 'central-control' / 'orchestrator' / 'rag_orchestrator.py'
        with open(orchestrator_path, 'w', encoding='utf-8') as f:
            f.write(orchestrator_code)
        print(f"  ✅ 오케스트레이터: {orchestrator_path}")
        
    def setup_web_dashboard(self):
        """웹 대시보드 기본 설정"""
        print("\n🌐 웹 대시보드 설정...")
        
        dashboard_html = '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Desinsight 분산 RAG 생태계 대시보드</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               background: #1a1a1a; color: #fff; margin: 0; padding: 20px; }
        .container { max-width: 1400px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .ecosystem-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .device-card { background: #2a2a2a; border-radius: 12px; padding: 20px; border-left: 4px solid #00a8ff; }
        .device-card.active { border-left-color: #00ff88; }
        .device-card.pending { border-left-color: #ffa500; }
        .device-name { font-size: 18px; font-weight: bold; margin-bottom: 10px; }
        .device-role { color: #888; margin-bottom: 15px; }
        .service-list { list-style: none; padding: 0; }
        .service-list li { padding: 5px 0; color: #ccc; }
        .status-active { color: #00ff88; }
        .status-pending { color: #ffa500; }
        .nas-section { margin-top: 40px; }
        .nas-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; }
        .nas-card { background: #1e3a8a; border-radius: 8px; padding: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏗 Desinsight 분산 RAG 생태계</h1>
            <p>5-Device + 3-NAS 아키텍처 중앙 제어 대시보드</p>
        </div>
        
        <div class="ecosystem-grid">
            <div class="device-card active">
                <div class="device-name">🏠 HOME iMac i7 64GB</div>
                <div class="device-role">중앙 제어 서버</div>
                <div class="status-active">● 활성 상태</div>
                <ul class="service-list">
                    <li>🎼 RAG 오케스트레이터</li>
                    <li>🌐 웹 대시보드</li>
                    <li>📊 데이터 관리자</li>
                    <li>🔧 개발 서버</li>
                </ul>
            </div>
            
            <div class="device-card pending">
                <div class="device-name">🏠 Mac Mini M2 Pro 32GB</div>
                <div class="device-role">임베딩 서버</div>
                <div class="status-pending">● 설정 대기 중</div>
                <ul class="service-list">
                    <li>⚡ 임베딩 생성기</li>
                    <li>🔄 배치 프로세서</li>
                    <li>🧠 모델 트레이너</li>
                </ul>
            </div>
            
            <div class="device-card pending">
                <div class="device-name">🏢 Office iMac i7 40GB</div>
                <div class="device-role">UI 서버</div>
                <div class="status-pending">● 설정 대기 중</div>
                <ul class="service-list">
                    <li>🔍 검색 UI</li>
                    <li>📊 모니터링 대시보드</li>
                    <li>👥 협업 기능</li>
                </ul>
            </div>
            
            <div class="device-card pending">
                <div class="device-name">🏢 Mac Studio M4 Pro 64GB</div>
                <div class="device-role">추론 서버</div>
                <div class="status-pending">● 설정 대기 중</div>
                <ul class="service-list">
                    <li>🚀 고성능 추론</li>
                    <li>🌐 API 게이트웨이</li>
                    <li>🧮 분석 엔진</li>
                </ul>
            </div>
            
            <div class="device-card pending">
                <div class="device-name">📱 Mobile 클라이언트</div>
                <div class="device-role">사용자 인터페이스</div>
                <div class="status-pending">● 설정 대기 중</div>
                <ul class="service-list">
                    <li>📱 모바일 앱</li>
                    <li>📸 현장 데이터 수집</li>
                    <li>🌐 외부 접근</li>
                </ul>
            </div>
        </div>
        
        <div class="nas-section">
            <h2>🗄️ 3-Tier NAS 아키텍처</h2>
            <div class="nas-grid">
                <div class="nas-card">
                    <h3>SnapCodex 전용 NAS</h3>
                    <p>192.168.219.175</p>
                    <p>실시간 프로젝트 데이터 처리</p>
                </div>
                <div class="nas-card">
                    <h3>Desinsight2 메인 NAS</h3>
                    <p>중앙 저장소</p>
                    <p>고가용성 데이터 허브</p>
                </div>
                <div class="nas-card">
                    <h3>Office 백업 NAS</h3>
                    <p>desinsight.synology.me:5001</p>
                    <p>재해 복구 백업</p>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // 실시간 상태 업데이트 (향후 구현)
        console.log('🎯 Desinsight 분산 RAG 생태계 대시보드 로드됨');
    </script>
</body>
</html>'''
        
        dashboard_path = self.workspace / 'central-control' / 'dashboard' / 'index.html'
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(dashboard_html)
        print(f"  ✅ 대시보드: {dashboard_path}")
        
    def setup_device_manager(self):
        """디바이스 연결 관리자 설정"""
        print("\n🔗 디바이스 관리자 설정...")
        
        device_manager_code = '''#!/usr/bin/env python3
"""
디바이스 연결 및 상태 관리자
"""

import json
import asyncio
from pathlib import Path

class DeviceManager:
    def __init__(self):
        self.config_path = Path.home() / 'workspace' / 'central-control' / 'configs' / 'ecosystem.json'
        self.devices = self.load_config()
        
    def load_config(self):
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    async def ping_device(self, device_name: str, device_config: dict):
        """디바이스 연결 상태 확인"""
        try:
            if 'ip' in device_config:
                # 실제 ping 또는 HTTP 체크 구현
                print(f"  📡 {device_name}: 연결 확인 중...")
                return True
        except:
            return False
            
    async def setup_device_connection(self, device_name: str):
        """디바이스 연결 설정"""
        print(f"🔧 {device_name} 연결 설정 중...")
        # SSH 키 교환, 설정 동기화 등
        
    def generate_setup_script(self, device_name: str) -> str:
        """디바이스별 설정 스크립트 생성"""
        device_config = self.devices.get('devices', {}).get(device_name, {})
        role = device_config.get('role', 'unknown')
        
        script = "#!/bin/bash\\n"
        script += f"# {device_name} 자동 설정 스크립트\\n"
        script += f"echo '🎯 {device_name} 설정 시작...'\\n"
        script += f"echo '역할: {role}'\\n"
        script += "cd ~/workspace\\n"
        script += "mkdir -p distributed-rag\\n"
        script += "cd distributed-rag\\n"
        
        return script

if __name__ == "__main__":
    manager = DeviceManager()
    print("🔗 디바이스 관리자 시작됨")
'''
        
        manager_path = self.workspace / 'central-control' / 'device_manager.py'
        with open(manager_path, 'w', encoding='utf-8') as f:
            f.write(device_manager_code)
        print(f"  ✅ 디바이스 관리자: {manager_path}")
        
    def setup_monitoring(self):
        """모니터링 시스템 설정"""
        print("\n📊 모니터링 시스템 설정...")
        
        # 시스템 상태 로그 파일 생성
        log_path = self.workspace / 'logs' / 'ecosystem.log'
        log_path.touch()
        
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f"[{datetime.now().isoformat()}] 분산 RAG 생태계 중앙 제어 서버 시작\n")
            f.write(f"[{datetime.now().isoformat()}] HOME iMac i7 64GB 중앙 제어 서버 활성화\n")
            
        print(f"  ✅ 로그 시스템: {log_path}")
        
    def print_next_steps(self):
        """다음 단계 안내"""
        print("\n🚀 다음 단계 가이드")
        print("=" * 60)
        print("✅ Mission 1 완료: 중앙 제어 서버 설정")
        print("\n🔥 즉시 실행 가능:")
        print("1. 웹 대시보드 열기:")
        print(f"   open {self.workspace}/central-control/dashboard/index.html")
        print("\n2. 오케스트레이터 시작:")
        print(f"   python3 {self.workspace}/central-control/orchestrator/rag_orchestrator.py")
        print("\n3. Mission 2 - 디바이스 연결 테스트:")
        print("   python3 central-control/device_manager.py")
        print("\n📍 생성된 주요 파일:")
        print(f"  • 생태계 설정: central-control/configs/ecosystem.json")
        print(f"  • 웹 대시보드: central-control/dashboard/index.html") 
        print(f"  • 오케스트레이터: central-control/orchestrator/rag_orchestrator.py")
        print(f"  • 디바이스 관리자: central-control/device_manager.py")

def main():
    """중앙 제어 서버 설정 실행"""
    print("🎯 Desinsight 분산 RAG 생태계 - Mission 1 시작\\n")
    
    setup = HomeImacSetup()
    setup.setup_central_controller()

if __name__ == "__main__":
    main() 