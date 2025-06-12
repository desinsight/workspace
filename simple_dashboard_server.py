#!/usr/bin/env python3
# simple_dashboard_server.py - NAS용 간단한 대시보드 서버

import http.server
import socketserver
import json
import os
import subprocess
import threading
import time
from urllib.parse import urlparse, parse_qs

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/dashboard.html'
        elif self.path == '/api/status':
            self.send_api_response()
            return
        elif self.path == '/api/system':
            self.send_system_info()
            return
        
        return super().do_GET()
    
    def send_api_response(self):
        """시스템 상태 API 응답"""
        try:
            # 시스템 정보 수집
            status = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "hostname": os.uname().nodename,
                "uptime": self.get_uptime(),
                "cpu_usage": self.get_cpu_usage(),
                "memory": self.get_memory_info(),
                "disk": self.get_disk_info(),
                "network": self.get_network_info()
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(status, indent=2).encode())
            
        except Exception as e:
            self.send_error(500, f"Error: {str(e)}")
    
    def send_system_info(self):
        """시스템 정보 API"""
        try:
            info = {
                "system": os.uname().sysname,
                "release": os.uname().release,
                "machine": os.uname().machine,
                "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}"
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(info, indent=2).encode())
            
        except Exception as e:
            self.send_error(500, f"Error: {str(e)}")
    
    def get_uptime(self):
        """시스템 업타임 조회"""
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                days = int(uptime_seconds // 86400)
                hours = int((uptime_seconds % 86400) // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                return f"{days}일 {hours}시간 {minutes}분"
        except:
            return "알 수 없음"
    
    def get_cpu_usage(self):
        """CPU 사용률 조회"""
        try:
            result = subprocess.run(['top', '-bn1'], capture_output=True, text=True, timeout=5)
            for line in result.stdout.split('\n'):
                if 'Cpu(s)' in line or '%Cpu' in line:
                    # CPU 사용률 파싱
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if 'us' in part or 'user' in part:
                            return f"{parts[i-1]}%"
            return "0%"
        except:
            return "알 수 없음"
    
    def get_memory_info(self):
        """메모리 정보 조회"""
        try:
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
                
            total = 0
            available = 0
            for line in meminfo.split('\n'):
                if line.startswith('MemTotal:'):
                    total = int(line.split()[1]) * 1024  # KB to bytes
                elif line.startswith('MemAvailable:'):
                    available = int(line.split()[1]) * 1024
            
            used = total - available
            usage_percent = (used / total * 100) if total > 0 else 0
            
            return {
                "total": f"{total // (1024**3):.1f}GB",
                "used": f"{used // (1024**3):.1f}GB",
                "available": f"{available // (1024**3):.1f}GB",
                "usage_percent": f"{usage_percent:.1f}%"
            }
        except:
            return {"total": "알 수 없음", "used": "알 수 없음", "available": "알 수 없음", "usage_percent": "0%"}
    
    def get_disk_info(self):
        """디스크 정보 조회"""
        try:
            result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True, timeout=5)
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                parts = lines[1].split()
                return {
                    "total": parts[1],
                    "used": parts[2],
                    "available": parts[3],
                    "usage_percent": parts[4]
                }
            return {"total": "알 수 없음", "used": "알 수 없음", "available": "알 수 없음", "usage_percent": "0%"}
        except:
            return {"total": "알 수 없음", "used": "알 수 없음", "available": "알 수 없음", "usage_percent": "0%"}
    
    def get_network_info(self):
        """네트워크 정보 조회"""
        try:
            result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True, timeout=5)
            interfaces = []
            current_interface = None
            
            for line in result.stdout.split('\n'):
                if ': ' in line and 'inet ' not in line:
                    parts = line.split(': ')
                    if len(parts) >= 2:
                        current_interface = parts[1].split('@')[0]
                elif 'inet ' in line and current_interface:
                    ip = line.strip().split()[1].split('/')[0]
                    if ip != '127.0.0.1':
                        interfaces.append(f"{current_interface}: {ip}")
            
            return interfaces if interfaces else ["네트워크 정보 없음"]
        except:
            return ["네트워크 정보 조회 실패"]

def create_dashboard_html():
    """대시보드 HTML 파일 생성"""
    html_content = '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Desinsight NAS 대시보드</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .card { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .metric { display: flex; justify-content: space-between; margin: 10px 0; }
        .metric-label { font-weight: bold; }
        .metric-value { color: #27ae60; }
        .status-indicator { width: 12px; height: 12px; border-radius: 50%; display: inline-block; margin-right: 8px; }
        .status-online { background: #27ae60; }
        .status-offline { background: #e74c3c; }
        .refresh-btn { background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
        .refresh-btn:hover { background: #2980b9; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🖥️ Desinsight NAS 대시보드</h1>
            <p>실시간 시스템 모니터링 - <span id="timestamp">로딩 중...</span></p>
            <button class="refresh-btn" onclick="refreshData()">🔄 새로고침</button>
        </div>
        
        <div class="grid">
            <div class="card">
                <h3>📊 시스템 상태</h3>
                <div class="metric">
                    <span class="metric-label">상태:</span>
                    <span class="metric-value"><span class="status-indicator status-online"></span>온라인</span>
                </div>
                <div class="metric">
                    <span class="metric-label">호스트명:</span>
                    <span class="metric-value" id="hostname">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">업타임:</span>
                    <span class="metric-value" id="uptime">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">CPU 사용률:</span>
                    <span class="metric-value" id="cpu">-</span>
                </div>
            </div>
            
            <div class="card">
                <h3>💾 메모리 정보</h3>
                <div class="metric">
                    <span class="metric-label">총 메모리:</span>
                    <span class="metric-value" id="memory-total">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">사용 중:</span>
                    <span class="metric-value" id="memory-used">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">사용 가능:</span>
                    <span class="metric-value" id="memory-available">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">사용률:</span>
                    <span class="metric-value" id="memory-usage">-</span>
                </div>
            </div>
            
            <div class="card">
                <h3>💿 디스크 정보</h3>
                <div class="metric">
                    <span class="metric-label">총 용량:</span>
                    <span class="metric-value" id="disk-total">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">사용 중:</span>
                    <span class="metric-value" id="disk-used">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">사용 가능:</span>
                    <span class="metric-value" id="disk-available">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">사용률:</span>
                    <span class="metric-value" id="disk-usage">-</span>
                </div>
            </div>
            
            <div class="card">
                <h3>🌐 네트워크 정보</h3>
                <div id="network-info">로딩 중...</div>
            </div>
        </div>
    </div>
    
    <script>
        function refreshData() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('timestamp').textContent = data.timestamp;
                    document.getElementById('hostname').textContent = data.hostname;
                    document.getElementById('uptime').textContent = data.uptime;
                    document.getElementById('cpu').textContent = data.cpu_usage;
                    
                    document.getElementById('memory-total').textContent = data.memory.total;
                    document.getElementById('memory-used').textContent = data.memory.used;
                    document.getElementById('memory-available').textContent = data.memory.available;
                    document.getElementById('memory-usage').textContent = data.memory.usage_percent;
                    
                    document.getElementById('disk-total').textContent = data.disk.total;
                    document.getElementById('disk-used').textContent = data.disk.used;
                    document.getElementById('disk-available').textContent = data.disk.available;
                    document.getElementById('disk-usage').textContent = data.disk.usage_percent;
                    
                    const networkDiv = document.getElementById('network-info');
                    networkDiv.innerHTML = data.network.map(info => 
                        `<div class="metric"><span class="metric-label">${info}</span></div>`
                    ).join('');
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('timestamp').textContent = '데이터 로드 실패';
                });
        }
        
        // 페이지 로드 시 데이터 로드
        refreshData();
        
        // 30초마다 자동 새로고침
        setInterval(refreshData, 30000);
    </script>
</body>
</html>'''
    
    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    PORT = 8080
    
    # 대시보드 HTML 파일 생성
    create_dashboard_html()
    
    print(f"🚀 Desinsight NAS 대시보드 서버 시작")
    print(f"📡 포트: {PORT}")
    print(f"🌐 접속 URL: http://192.168.219.175:{PORT}")
    print(f"🔄 Ctrl+C로 종료")
    
    try:
        with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 서버 종료")
    except Exception as e:
        print(f"❌ 서버 오류: {e}") 