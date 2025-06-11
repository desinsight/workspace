        
        dashboard_path = self.control_center / 'dashboard' / 'index.html'
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(dashboard_html)
        
        logger.info(f"✅ 모니터링 대시보드 생성: {dashboard_path}")
        return dashboard_path
    
    def create_device_setup_scripts(self):
        """다른 디바이스들을 위한 설정 스크립트 생성"""
        logger.info("📜 디바이스별 설정 스크립트 생성 중...")
        
        # Mac Mini M2 Pro 설정 스크립트
        mini_script = """#!/bin/bash
echo "⚡ HOME Mac Mini M2 Pro 임베딩 서버 설정 시작"

# 환경 감지
DEVICE_TYPE="mac_mini_m2pro"
ROLE="embedding_server"
MEMORY_GB=32

# 디렉토리 생성
mkdir -p ~/rag-embedding-server
cd ~/rag-embedding-server

# Python 환경 설정
python3 -m venv venv
source venv/bin/activate

# 임베딩 전용 패키지 설치
pip install sentence-transformers chromadb torch torchvision

# Ollama 경량 모델 설치
ollama pull llama3.1:7b
ollama pull mistral:7b

# 임베딩 서버 설정
cat > embedding_server_config.json << EOF
{
  "device": "mac_mini_m2pro_32gb",
  "role": "embedding_server",
  "batch_size": 64,
  "max_memory_gb": 24,
  "models": {
    "general": "all-minilm-l6-v2",
    "korean": "ko-sroberta-multitask",
    "technical": "all-mpnet-base-v2"
  },
  "schedule": {
    "nas_sync": "0 2 * * *",
    "embedding_batch": "0 3 * * *"
  }
}
EOF

echo "✅ Mac Mini M2 Pro 설정 완료"
"""
        
        # Office Mac Studio 설정 스크립트
        studio_script = """#!/bin/bash
echo "🚀 OFFICE Mac Studio M4 Pro 추론 서버 설정 시작"

# 환경 감지
DEVICE_TYPE="mac_studio_m4pro"
ROLE="inference_server"
MEMORY_GB=64

# 디렉토리 생성
mkdir -p ~/rag-inference-server
cd ~/rag-inference-server

# Python 환경 설정
python3 -m venv venv
source venv/bin/activate

# 고성능 추론 패키지 설치
pip install ollama fastapi uvicorn chromadb

# Ollama 고성능 모델 설치
ollama pull llama3.1:70b
ollama pull codellama:34b

# 추론 서버 설정
cat > inference_server_config.json << EOF
{
  "device": "mac_studio_m4pro_64gb",
  "role": "inference_server",
  "max_memory_gb": 50,
  "concurrent_requests": 50,
  "models": {
    "primary": "llama3.1:70b",
    "code": "codellama:34b",
    "fast": "mistral:7b"
  },
  "performance": {
    "gpu_acceleration": true,
    "parallel_inference": true,
    "cache_size": "10GB"
  }
}
EOF

echo "✅ Mac Studio M4 Pro 설정 완료"
"""
        
        # Office iMac UI 서버 설정 스크립트
        ui_script = """#!/bin/bash
echo "🏢 OFFICE iMac i7 UI 서버 설정 시작"

# 환경 감지
DEVICE_TYPE="office_imac_i7"
ROLE="ui_server"
MEMORY_GB=40

# 디렉토리 생성
mkdir -p ~/rag-ui-server
cd ~/rag-ui-server

# Node.js & Python 환경 설정
python3 -m venv venv
source venv/bin/activate

# UI 서버 패키지 설치
pip install fastapi uvicorn jinja2 websockets

# 웹 UI 설정
cat > ui_server_config.json << EOF
{
  "device": "office_imac_i7_40gb",
  "role": "ui_server",
  "services": {
    "web_portal": "http://localhost:8003",
    "search_api": "http://localhost:8004",
    "websocket": "ws://localhost:8005"
  },
  "features": {
    "real_time_search": true,
    "collaboration": true,
    "session_management": true,
    "mobile_responsive": true
  }
}
EOF

echo "✅ Office iMac UI 서버 설정 완료"
"""
        
        # 스크립트 파일들 저장
        scripts = {
            'setup_mac_mini.sh': mini_script,
            'setup_office_studio.sh': studio_script,
            'setup_office_imac.sh': ui_script
        }
        
        script_paths = []
        for script_name, script_content in scripts.items():
            script_path = self.workspace / 'device-configs' / script_name
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            # 실행 권한 부여
            os.chmod(script_path, 0o755)
            script_paths.append(script_path)
            logger.info(f"  ✅ {script_name}")
        
        return script_paths
    
    def create_central_api_server(self):
        """중앙 제어 API 서버 생성"""
        logger.info("🌐 중앙 제어 API 서버 생성 중...")
        
        api_server_code = '''"""
Desinsight 중앙 제어 API 서버
5-Device 분산 RAG 시스템의 중앙 조율 API
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import json
import asyncio
from pathlib import Path
import uvicorn

app = FastAPI(title="Desinsight Central Control API")

# 정적 파일 서빙 (대시보드)
app.mount("/static", StaticFiles(directory="dashboard"), name="static")

# 디바이스 상태 저장
device_status = {}
connected_clients = []

@app.get("/")
async def dashboard():
    """메인 대시보드 페이지"""
    with open("dashboard/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/devices")
async def get_devices():
    """모든 디바이스 상태 조회"""
    with open("configs/device_registry.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/api/devices/{device_id}/status")
async def get_device_status(device_id: str):
    """특정 디바이스 상태 조회"""
    return device_status.get(device_id, {"status": "unknown"})

@app.post("/api/devices/{device_id}/status")
async def update_device_status(device_id: str, status: dict):
    """디바이스 상태 업데이트"""
    device_status[device_id] = status
    
    # 연결된 클라이언트들에게 브로드캐스트
    for client in connected_clients:
        try:
            await client.send_json({
                "type": "device_status_update",
                "device_id": device_id,
                "status": status
            })
        except:
            connected_clients.remove(client)
    
    return {"message": "Status updated successfully"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """실시간 상태 업데이트용 WebSocket"""
    await websocket.accept()
    connected_clients.append(websocket)
    
    try:
        # 초기 상태 전송
        await websocket.send_json({
            "type": "initial_status",
            "devices": device_status
        })
        
        # 연결 유지
        while True:
            await websocket.receive_text()
            
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

@app.post("/api/orchestrate/start")
async def start_orchestration():
    """RAG 시스템 전체 시작"""
    # TODO: 실제 오케스트레이션 로직 구현
    return {"message": "Orchestration started", "status": "success"}

@app.post("/api/orchestrate/stop")
async def stop_orchestration():
    """RAG 시스템 전체 중지"""
    # TODO: 실제 오케스트레이션 로직 구현
    return {"message": "Orchestration stopped", "status": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        
        api_path = self.control_center / 'central_api.py'
        with open(api_path, 'w', encoding='utf-8') as f:
            f.write(api_server_code)
        
        logger.info(f"✅ 중앙 제어 API 서버 생성: {api_path}")
        return api_path
    
    def create_startup_script(self):
        """중앙 제어 서버 시작 스크립트"""
        logger.info("🚀 시작 스크립트 생성 중...")
        
        startup_script = f'''#!/bin/bash

echo "🏠 Desinsight 중앙 제어 서버 시작"
echo "디바이스: HOME iMac i7 64GB"
echo "역할: Central Controller"

cd {self.control_center}

# Python 가상환경 활성화
if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install fastapi uvicorn websockets jinja2
else
    source venv/bin/activate
fi

# 환경 변수 설정
export DEVICE_NAME="HOME-iMac-i7-64GB"
export DEVICE_ROLE="central_controller"
export PYTHONPATH="{self.control_center}:$PYTHONPATH"

# 로그 디렉토리 생성
mkdir -p logs

# 중앙 제어 API 서버 시작
echo "🌐 중앙 제어 API 서버 시작 중..."
python central_api.py &
API_PID=$!

# 웹 대시보드 접근 정보
echo ""
echo "✅ 중앙 제어 서버 시작 완료!"
echo "📊 대시보드: http://localhost:8000"
echo "🔗 API 문서: http://localhost:8000/docs"
echo "📋 디바이스 상태: http://localhost:8000/api/devices"
echo ""
echo "🎯 다음 단계:"
echo "1. 브라우저에서 http://localhost:8000 접속"
echo "2. 다른 디바이스들 설정 시작"
echo "3. NAS 연결 테스트"
echo ""

# 종료 시그널 처리
trap 'kill $API_PID; exit' INT TERM

# 대기
wait $API_PID
'''
        
        script_path = self.control_center / 'start_central_control.sh'
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(startup_script)
        
        # 실행 권한 부여
        os.chmod(script_path, 0o755)
        
        logger.info(f"✅ 시작 스크립트 생성: {script_path}")
        return script_path
    
    def run_setup(self):
        """전체 설정 실행"""
        logger.info("🎯 HOME iMac 중앙 제어 서버 설정 시작")
        
        try:
            # 1. 디렉토리 구조 생성
            self.create_directory_structure()
            
            # 2. 디바이스 레지스트리 생성
            device_registry = self.create_device_registry()
            
            # 3. 오케스트레이터 설정
            orchestrator_config = self.create_orchestrator_config()
            
            # 4. 모니터링 대시보드 생성
            dashboard_path = self.create_monitoring_dashboard()
            
            # 5. 다른 디바이스 설정 스크립트 생성
            script_paths = self.create_device_setup_scripts()
            
            # 6. 중앙 API 서버 생성
            api_path = self.create_central_api_server()
            
            # 7. 시작 스크립트 생성
            startup_path = self.create_startup_script()
            
            self.print_completion_message()
            return True
            
        except Exception as e:
            logger.error(f"❌ 설정 중 오류 발생: {e}")
            return False
    
    def print_completion_message(self):
        """완료 메시지 출력"""
        print("\n" + "="*60)
        print("🎉 HOME iMac 중앙 제어 서버 설정 완료!")
        print("="*60)
        
        print(f"\n📊 디바이스 정보:")
        print(f"   🏷️  이름: {self.device_name}")
        print(f"   🎯 역할: 중앙 제어 서버 (Central Controller)")
        print(f"   💾 메모리: 64GB")
        print(f"   🖥️  CPU: Intel i7")
        
        print(f"\n🚀 즉시 실행:")
        print(f"   cd {self.control_center}")
        print(f"   ./start_central_control.sh")
        
        print(f"\n🌐 접속 정보:")
        print(f"   📊 대시보드: http://localhost:8000")
        print(f"   🔗 API 문서: http://localhost:8000/docs")
        print(f"   📋 디바이스 API: http://localhost:8000/api/devices")
        
        print(f"\n📁 주요 경로:")
        print(f"   🎛️  제어센터: {self.control_center}")
        print(f"   📊 대시보드: {self.control_center}/dashboard/")
        print(f"   ⚙️  설정파일: {self.control_center}/configs/")
        print(f"   📜 스크립트: {self.workspace}/device-configs/")
        
        print(f"\n🔧 다음 단계:")
        print(f"   1. 중앙 제어 서버 시작")
        print(f"   2. 웹 대시보드 접속 확인")
        print(f"   3. Mac Mini M2 Pro 설정:")
        print(f"      scp {self.workspace}/device-configs/setup_mac_mini.sh user@mac-mini:~/")
        print(f"   4. Office 디바이스들 설정:")
        print(f"      scp {self.workspace}/device-configs/setup_office_*.sh user@office-mac:~/")
        
        print("\n" + "="*60)
        print("🎯 5-Device 분산 RAG 시스템의 중앙 허브가 준비되었습니다!")
        print("="*60)

def main():
    """메인 함수"""
    try:
        controller = HomeImacCentralController()
        success = controller.run_setup()
        
        if success:
            print("\n✅ 모든 설정이 완료되었습니다!")
            print("💡 './start_central_control.sh' 실행으로 시스템을 시작하세요!")
        else:
            print("\n❌ 설정 중 오류가 발생했습니다.")
            
    except Exception as e:
        logger.error(f"예기치 못한 오류: {e}")

if __name__ == "__main__":
    main()
