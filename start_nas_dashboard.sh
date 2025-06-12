#!/bin/bash
# start_nas_dashboard.sh - NAS 대시보드 자동 시작 스크립트

echo "🚀 Desinsight NAS 대시보드 시작 중..."

# SSH를 통해 NAS에서 대시보드 실행
ssh nas "cd ~/desinsight-dashboard && nohup python3 dashboard_5002.py > dashboard.log 2>&1 &"

# 잠시 대기
sleep 3

# 실행 상태 확인
if ssh nas "ps aux | grep dashboard_5002 | grep -v grep" > /dev/null; then
    echo "✅ 대시보드 서버가 성공적으로 시작되었습니다!"
    echo "🌐 접속 URL: http://192.168.219.175:5002"
    echo "📊 대시보드에 접속하여 NAS 상태를 확인하세요."
    
    # 브라우저에서 열기 (macOS)
    if command -v open > /dev/null; then
        echo "🔗 브라우저에서 대시보드를 여는 중..."
        open "http://192.168.219.175:5002"
    fi
else
    echo "❌ 대시보드 서버 시작에 실패했습니다."
    echo "📋 로그 확인: ssh nas 'cat ~/desinsight-dashboard/dashboard.log'"
fi 