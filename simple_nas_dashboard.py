#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import time

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Desinsight NAS 대시보드</title>
<style>
body{{font-family:Arial;margin:20px;background:#f5f5f5}}
.container{{max-width:800px;margin:0 auto}}
.header{{background:#2c3e50;color:white;padding:20px;border-radius:8px;margin-bottom:20px}}
.card{{background:white;padding:20px;border-radius:8px;margin-bottom:20px;box-shadow:0 2px 4px rgba(0,0,0,0.1)}}
.metric{{display:flex;justify-content:space-between;margin:10px 0}}
.metric-label{{font-weight:bold}}
.metric-value{{color:#27ae60}}
.status-online{{color:#27ae60}}
</style></head>
<body>
<div class="container">
    <div class="header">
        <h1>🖥️ Desinsight NAS 대시보드</h1>
        <p>실시간 시스템 모니터링 - {time.strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    <div class="card">
        <h3>📊 시스템 상태</h3>
        <div class="metric">
            <span class="metric-label">상태:</span>
            <span class="metric-value status-online">🟢 온라인</span>
        </div>
        <div class="metric">
            <span class="metric-label">호스트명:</span>
            <span class="metric-value">{os.uname().nodename}</span>
        </div>
        <div class="metric">
            <span class="metric-label">시스템:</span>
            <span class="metric-value">{os.uname().sysname} {os.uname().release}</span>
        </div>
        <div class="metric">
            <span class="metric-label">아키텍처:</span>
            <span class="metric-value">{os.uname().machine}</span>
        </div>
    </div>
    <div class="card">
        <h3>🔗 접속 정보</h3>
        <div class="metric">
            <span class="metric-label">대시보드 URL:</span>
            <span class="metric-value">http://192.168.219.175:5001</span>
        </div>
        <div class="metric">
            <span class="metric-label">SSH 접속:</span>
            <span class="metric-value">ssh admin@192.168.219.175</span>
        </div>
        <div class="metric">
            <span class="metric-label">웹 관리:</span>
            <span class="metric-value">http://192.168.219.175:5000</span>
        </div>
    </div>
</div>
<script>
setTimeout(function(){{location.reload()}}, 30000);
</script>
</body></html>'''
            self.wfile.write(html.encode())
        elif self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            status = {
                'hostname': os.uname().nodename,
                'time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'system': os.uname().sysname,
                'status': 'online'
            }
            self.wfile.write(json.dumps(status).encode())

if __name__ == "__main__":
    PORT = 5001
    print(f'🚀 Desinsight NAS 대시보드 서버 시작')
    print(f'📡 포트: {PORT}')
    print(f'🌐 접속 URL: http://192.168.219.175:{PORT}')
    print(f'🔄 30초마다 자동 새로고침')
    
    try:
        with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        print(f'❌ 서버 오류: {e}') 