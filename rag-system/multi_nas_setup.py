        
        dashboard_path = self.control_center / 'dashboard' / 'multi_nas_index.html'
        dashboard_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(dashboard_html)
        
        logger.info(f"✅ 3-NAS 통합 대시보드 생성: {dashboard_path}")
        return dashboard_path
    
    def create_snapcodex_nas_collector(self):
        """SnapCodex 전용 NAS 데이터 수집기"""
        logger.info("⚡ SnapCodex NAS 전용 수집기 생성 중...")
        
        collector_code = '''"""
SnapCodex 전용 NAS 데이터 수집기
건축 도면, 원가 계산서 등 SnapCodex 프로젝트 전용 데이터 실시간 처리
"""

import asyncio
import aiofiles
import json
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SnapCodexNASCollector:
    """SnapCodex 전용 NAS 데이터 수집기"""
    
    def __init__(self):
        self.nas_host = "snapcodx-nas.local"
        self.nas_port = 5000
        self.target_directories = [
            "/snapcodx/drawings/",      # 건축 도면
            "/snapcodx/calculations/",  # 원가 계산서  
            "/snapcodx/projects/",      # 프로젝트 파일
            "/snapcodx/templates/",     # 템플릿
            "/snapcodx/reports/"        # 보고서
        ]
        
        self.file_types = {
            'cad_files': ['.dwg', '.dxf', '.ifc'],
            'documents': ['.pdf', '.docx', '.xlsx'],
            'images': ['.png', '.jpg', '.jpeg', '.tiff'],
            'data_files': ['.json', '.csv', '.xml']
        }
        
        self.processing_queue = []
        
    async def scan_snapcodx_directories(self):
        """SnapCodex NAS 디렉토리 스캔"""
        logger.info("📁 SnapCodex NAS 디렉토리 스캔 시작...")
        
        discovered_files = []
        
        for directory in self.target_directories:
            try:
                # TODO: 실제 NAS API 연동
                logger.info(f"   스캔 중: {directory}")
                
                # 시뮬레이션된 파일 목록
                mock_files = [
                    f"{directory}project_001.dwg",
                    f"{directory}cost_calc_001.xlsx", 
                    f"{directory}floor_plan.pdf"
                ]
                
                for file_path in mock_files:
                    file_info = {
                        'path': file_path,
                        'type': self.classify_file_type(file_path),
                        'priority': self.calculate_priority(file_path),
                        'discovered_at': datetime.now().isoformat()
                    }
                    discovered_files.append(file_info)
                    
            except Exception as e:
                logger.error(f"디렉토리 스캔 실패 {directory}: {e}")
                continue
        
        logger.info(f"✅ 총 {len(discovered_files)}개 파일 발견")
        return discovered_files
    
    def classify_file_type(self, file_path: str) -> str:
        """파일 타입 분류"""
        file_ext = Path(file_path).suffix.lower()
        
        for category, extensions in self.file_types.items():
            if file_ext in extensions:
                return category
        
        return 'unknown'
    
    def calculate_priority(self, file_path: str) -> int:
        """처리 우선순위 계산"""
        if 'urgent' in file_path.lower():
            return 1
        elif 'project' in file_path.lower():
            return 2
        elif 'template' in file_path.lower():
            return 3
        else:
            return 4
    
    async def queue_for_embedding(self, files: list):
        """임베딩 처리를 위한 큐 추가"""
        logger.info(f"⚡ {len(files)}개 파일을 임베딩 큐에 추가...")
        
        for file_info in files:
            processing_item = {
                'file_info': file_info,
                'status': 'queued',
                'target_device': 'home_mini_m2pro_32gb',
                'queued_at': datetime.now().isoformat()
            }
            
            self.processing_queue.append(processing_item)
        
        # 우선순위별 정렬
        self.processing_queue.sort(key=lambda x: x['file_info']['priority'])
        
        logger.info("✅ 임베딩 큐 업데이트 완료")
        return self.processing_queue

if __name__ == "__main__":
    async def main():
        collector = SnapCodexNASCollector()
        files = await collector.scan_snapcodx_directories()
        queue = await collector.queue_for_embedding(files)
        
        print(f"📊 SnapCodex NAS 수집 결과:")
        print(f"   발견된 파일: {len(files)}개")
        print(f"   처리 대기: {len(queue)}개")
    
    asyncio.run(main())
'''
        
        collector_path = self.control_center / 'snapcodx_nas_collector.py'
        with open(collector_path, 'w', encoding='utf-8') as f:
            f.write(collector_code)
        
        logger.info(f"✅ SnapCodex NAS 수집기 생성: {collector_path}")
        return collector_path
    
    def create_synology_sync_monitor(self):
        """Synology Sync 모니터링 시스템"""
        logger.info("🔄 Synology Sync 모니터 생성 중...")
        
        sync_monitor_code = '''"""
Synology Sync 모니터링 시스템
Desinsight2 NAS ↔ Office NAS 동기화 상태 실시간 모니터링
"""

import asyncio
import json
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class SynologySyncMonitor:
    """Synology Sync 상태 모니터링"""
    
    def __init__(self):
        self.source_nas = "desinsight2.local"
        self.target_nas = "desinsight.synology.me"
        self.sync_status = {}
        self.sync_history = []
        
    async def check_sync_status(self):
        """동기화 상태 확인"""
        logger.info("🔍 Synology Sync 상태 확인 중...")
        
        try:
            # TODO: 실제 Synology API 연동
            
            # 시뮬레이션된 동기화 상태
            sync_info = {
                'sync_id': 'desinsight_backup_001',
                'source': self.source_nas,
                'target': self.target_nas,
                'status': 'active',  # active, paused, error, completed
                'progress': 87.5,
                'files_synced': 2847,
                'total_files': 3267,
                'data_transferred': '245.7 GB',
                'last_sync': datetime.now().isoformat(),
                'next_sync': (datetime.now() + timedelta(hours=1)).isoformat(),
                'sync_speed': '45.2 MB/s'
            }
            
            self.sync_status = sync_info
            self.sync_history.append({
                'timestamp': datetime.now().isoformat(),
                'status': sync_info['status'],
                'progress': sync_info['progress']
            })
            
            # 히스토리는 최근 100개만 유지
            if len(self.sync_history) > 100:
                self.sync_history = self.sync_history[-100:]
            
            return sync_info
            
        except Exception as e:
            logger.error(f"동기화 상태 확인 실패: {e}")
            return None
    
    async def monitor_continuous(self):
        """연속 모니터링"""
        logger.info("📊 연속 동기화 모니터링 시작...")
        
        while True:
            try:
                status = await self.check_sync_status()
                
                if status:
                    if status['status'] == 'error':
                        logger.warning(f"⚠️ 동기화 오류 감지: {status}")
                        await self.handle_sync_error(status)
                    elif status['status'] == 'completed':
                        logger.info(f"✅ 동기화 완료: {status['files_synced']}개 파일")
                    
                # 30초마다 확인
                await asyncio.sleep(30)
                
            except Exception as e:
                logger.error(f"모니터링 중 오류: {e}")
                await asyncio.sleep(60)  # 오류 시 1분 대기
    
    async def handle_sync_error(self, status):
        """동기화 오류 처리"""
        logger.error("🚨 Synology Sync 오류 처리 중...")
        
        error_report = {
            'error_time': datetime.now().isoformat(),
            'sync_id': status.get('sync_id'),
            'error_details': status,
            'recommended_action': 'check_network_and_retry'
        }
        
        # TODO: 슬랙 알림, 이메일 발송 등
        logger.info("📧 관리자에게 오류 알림 발송")
        
        return error_report
    
    def get_sync_summary(self) -> dict:
        """동기화 요약 정보"""
        if not self.sync_status:
            return {"status": "no_data"}
        
        recent_history = self.sync_history[-10:] if self.sync_history else []
        
        summary = {
            'current_status': self.sync_status.get('status'),
            'progress': self.sync_status.get('progress'),
            'files_remaining': (
                self.sync_status.get('total_files', 0) - 
                self.sync_status.get('files_synced', 0)
            ),
            'estimated_completion': self.calculate_eta(),
            'recent_performance': recent_history,
            'health_score': self.calculate_health_score()
        }
        
        return summary
    
    def calculate_eta(self) -> str:
        """완료 예상 시간 계산"""
        if not self.sync_status:
            return "unknown"
        
        progress = self.sync_status.get('progress', 0)
        if progress >= 100:
            return "completed"
        
        # 간단한 ETA 계산 (실제로는 더 복잡한 로직 필요)
        remaining = 100 - progress
        speed = self.sync_status.get('sync_speed', '0 MB/s')
        
        # TODO: 실제 속도 기반 계산
        estimated_minutes = int(remaining * 2)  # 대략적 추정
        
        return f"{estimated_minutes}분 후"
    
    def calculate_health_score(self) -> int:
        """동기화 건강도 점수 (0-100)"""
        if not self.sync_status:
            return 0
        
        status = self.sync_status.get('status')
        progress = self.sync_status.get('progress', 0)
        
        if status == 'error':
            return 25
        elif status == 'paused':
            return 50
        elif status == 'active':
            return min(90, 60 + int(progress * 0.3))
        elif status == 'completed':
            return 100
        
        return 70

if __name__ == "__main__":
    async def main():
        monitor = SynologySyncMonitor()
        status = await monitor.check_sync_status()
        summary = monitor.get_sync_summary()
        
        print("🔄 Synology Sync 상태:")
        print(f"   상태: {summary.get('current_status')}")
        print(f"   진행률: {summary.get('progress')}%")
        print(f"   예상 완료: {summary.get('estimated_completion')}")
        print(f"   건강도: {summary.get('health_score')}/100")
    
    asyncio.run(main())
'''
        
        monitor_path = self.control_center / 'synology_sync_monitor.py'
        with open(monitor_path, 'w', encoding='utf-8') as f:
            f.write(sync_monitor_code)
        
        logger.info(f"✅ Synology Sync 모니터 생성: {monitor_path}")
        return monitor_path
    
    def create_multi_nas_startup_script(self):
        """3-NAS 통합 시작 스크립트"""
        logger.info("🚀 3-NAS 통합 시작 스크립트 생성 중...")
        
        startup_script = f'''#!/bin/bash

echo "🏗️ Desinsight 3-NAS + 5-Device RAG 시스템 시작"
echo "디바이스: HOME iMac i7 64GB (중앙 제어)"

cd {self.control_center}

# Python 가상환경 설정
if [ ! -d "venv" ]; then
    echo "🐍 Python 가상환경 생성 중..."
    python3 -m venv venv
    source venv/bin/activate
    pip install fastapi uvicorn aiohttp aiofiles websockets
else
    source venv/bin/activate
fi

# 환경 변수 설정
export DEVICE_NAME="HOME-iMac-i7-64GB"
export DEVICE_ROLE="central_controller"
export PYTHONPATH="{self.control_center}:$PYTHONPATH"

# 로그 디렉토리
mkdir -p logs

echo ""
echo "🗄️ NAS 연결 테스트 중..."
python3 -c "
import asyncio
import sys
sys.path.append('{self.control_center}')

async def test_nas():
    try:
        from nas_connection_manager import MultiNASConnectionManager
        manager = MultiNASConnectionManager()
        status = await manager.check_all_nas_systems()
        
        print('📊 NAS 시스템 상태:')
        for nas_key, nas_status in status.items():
            icon = '🟢' if nas_status['status'] == 'healthy' else '🟡' if nas_status['status'] == 'degraded' else '🔴'
            print(f'   {{icon}} {{nas_key}}: {{nas_status[\"status\"]}}')
    except Exception as e:
        print(f'⚠️ NAS 연결 테스트 실패: {{e}}')

asyncio.run(test_nas())
"

echo ""
echo "🔄 Synology Sync 상태 확인 중..."
python3 -c "
import asyncio
import sys
sys.path.append('{self.control_center}')

async def test_sync():
    try:
        from synology_sync_monitor import SynologySyncMonitor
        monitor = SynologySyncMonitor()
        summary = monitor.get_sync_summary()
        
        print('🔄 Synology Sync 상태:')
        print(f'   상태: {{summary.get(\"current_status\", \"확인중\")}}')
        print(f'   건강도: {{summary.get(\"health_score\", 0)}}/100')
    except Exception as e:
        print(f'⚠️ Sync 상태 확인 실패: {{e}}')

asyncio.run(test_sync())
"

echo ""
echo "🚀 중앙 제어 서버 시작 중..."

# 백그라운드 서비스들 시작
echo "📊 NAS 모니터링 서비스 시작..."
python nas_connection_manager.py &
NAS_MONITOR_PID=$!

echo "🔄 Sync 모니터링 서비스 시작..."
python synology_sync_monitor.py &
SYNC_MONITOR_PID=$!

echo "⚡ SnapCodex 데이터 수집기 시작..."
python snapcodx_nas_collector.py &
COLLECTOR_PID=$!

echo "🌐 웹 대시보드 서버 시작..."
python multi_nas_api.py &
API_PID=$!

# 시작 완료 메시지
echo ""
echo "✅ 3-NAS + 5-Device RAG 시스템 시작 완료!"
echo ""
echo "🌐 접속 정보:"
echo "   📊 통합 대시보드: http://localhost:8000"
echo "   🔗 API 문서: http://localhost:8000/docs"
echo "   📋 NAS 상태: http://localhost:8000/api/nas/status"
echo "   🔄 Sync 상태: http://localhost:8000/api/sync/status"
echo ""
echo "🎯 다음 단계:"
echo "   1. 브라우저에서 대시보드 접속"
echo "   2. Mac Mini M2 Pro 설정: ./setup_mac_mini.sh"
echo "   3. Office 디바이스 설정: ./setup_office_devices.sh"
echo ""

# 종료 시그널 처리
trap 'echo "🛑 시스템 종료 중..."; kill $NAS_MONITOR_PID $SYNC_MONITOR_PID $COLLECTOR_PID $API_PID; exit' INT TERM

# 서비스들 대기
wait $API_PID
'''
        
        script_path = self.control_center / 'start_multi_nas_system.sh'
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(startup_script)
        
        os.chmod(script_path, 0o755)
        
        logger.info(f"✅ 3-NAS 통합 시작 스크립트 생성: {script_path}")
        return script_path
    
    def run_setup(self):
        """전체 설정 실행"""
        logger.info("🎯 3-NAS + 5-Device 분산 시스템 설정 시작")
        
        try:
            # 디렉토리 생성
            self.control_center.mkdir(parents=True, exist_ok=True)
            (self.control_center / 'configs').mkdir(exist_ok=True)
            (self.control_center / 'logs').mkdir(exist_ok=True)
            
            # 1. 멀티 NAS 레지스트리 생성
            registry = self.create_multi_nas_registry()
            
            # 2. NAS 연결 관리자 생성
            manager_path = self.create_nas_connection_manager()
            
            # 3. 통합 대시보드 생성
            dashboard_path = self.create_multi_nas_dashboard()
            
            # 4. SnapCodex NAS 수집기 생성
            collector_path = self.create_snapcodx_nas_collector()
            
            # 5. Synology Sync 모니터 생성
            monitor_path = self.create_synology_sync_monitor()
            
            # 6. 통합 시작 스크립트 생성
            startup_path = self.create_multi_nas_startup_script()
            
            self.print_completion_message()
            return True
            
        except Exception as e:
            logger.error(f"❌ 설정 중 오류 발생: {e}")
            return False
    
    def print_completion_message(self):
        """완료 메시지 출력"""
        print("\n" + "="*70)
        print("🎉 3-NAS + 5-Device 분산 RAG 시스템 설정 완료!")
        print("="*70)
        
        print(f"\n🗄️ NAS 시스템 구성:")
        print(f"   ⚡ SnapCodex 전용 NAS: 실시간 데이터 처리")
        print(f"   🏠 Desinsight2 NAS: 중앙 데이터 허브") 
        print(f"   🏢 Office NAS: Synology Sync 백업")
        
        print(f"\n🖥️ 디바이스 역할:")
        print(f"   🏠 HOME iMac i7 64GB: 중앙 제어 서버")
        print(f"   ⚡ HOME Mac Mini M2 Pro: SnapCodex 임베딩 처리")
        print(f"   🏢 OFFICE iMac i7 40GB: UI 서버 + 백업 모니터링")
        print(f"   🚀 OFFICE Mac Studio M4 Pro: 고성능 추론")
        print(f"   📱 Mobile: 클라이언트 접근")
        
        print(f"\n🚀 시스템 시작:")
        print(f"   cd {self.control_center}")
        print(f"   ./start_multi_nas_system.sh")
        
        print(f"\n🌐 접속 정보:")
        print(f"   📊 통합 대시보드: http://localhost:8000")
        print(f"   🗄️ NAS 상태 API: http://localhost:8000/api/nas/status")
        print(f"   🔄 Sync 상태 API: http://localhost:8000/api/sync/status")
        
        print(f"\n📁 주요 경로:")
        print(f"   🎛️ 제어센터: {self.control_center}")
        print(f"   📊 대시보드: {self.control_center}/dashboard/")
        print(f"   ⚙️ 설정파일: {self.control_center}/configs/")
        
        print("\n" + "="*70)
        print("🎯 3-NAS 통합 분산 RAG 생태계가 준비되었습니다!")
        print("="*70)

def main():
    """메인 함수"""
    try:
        setup = MultiNASEnvironmentSetup()
        success = setup.run_setup()
        
        if success:
            print("\n✅ 모든 설정이 완료되었습니다!")
            print("💡 './start_multi_nas_system.sh' 실행으로 시스템을 시작하세요!")
        else:
            print("\n❌ 설정 중 오류가 발생했습니다.")
            
    except Exception as e:
        logger.error(f"예기치 못한 오류: {e}")

if __name__ == "__main__":
    main()
