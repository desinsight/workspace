#!/bin/bash
# manage_nas_dashboard.sh - NAS 대시보드 관리 스크립트

DASHBOARD_URL="http://192.168.219.175:5003"
DASHBOARD_API="$DASHBOARD_URL/api/devices"

show_help() {
    echo "🖥️  Desinsight NAS 대시보드 관리 도구"
    echo ""
    echo "사용법: $0 [명령어]"
    echo ""
    echo "명령어:"
    echo "  start     - 대시보드 시작"
    echo "  stop      - 대시보드 중지"
    echo "  restart   - 대시보드 재시작"
    echo "  status    - 대시보드 상태 확인"
    echo "  open      - 브라우저에서 대시보드 열기"
    echo "  log       - 대시보드 로그 확인"
    echo "  help      - 도움말 표시"
    echo ""
    echo "접속 정보:"
    echo "  🌐 대시보드 URL: $DASHBOARD_URL"
    echo "  📡 API 엔드포인트: $DASHBOARD_API"
    echo "  🔑 SSH 접속: ssh nas"
}

start_dashboard() {
    echo "🚀 통합 대시보드 시작 중..."
    ssh nas "cd ~/desinsight-dashboard && nohup python3 integrated_dashboard_5003.py > integrated_dashboard.log 2>&1 &"
    sleep 3
    check_status
}

stop_dashboard() {
    echo "🛑 통합 대시보드 중지 중..."
    ssh nas "pkill -f integrated_dashboard_5003.py"
    sleep 2
    echo "✅ 대시보드가 중지되었습니다."
}

restart_dashboard() {
    echo "🔄 NAS 대시보드 재시작 중..."
    stop_dashboard
    sleep 2
    start_dashboard
}

check_status() {
    echo "📊 대시보드 상태 확인 중..."
    
    # 프로세스 확인
    if ssh nas "ps aux | grep integrated_dashboard_5003 | grep -v grep" > /dev/null; then
        echo "✅ 대시보드 프로세스: 실행 중"
        
        # HTTP 응답 확인
        if curl -s --connect-timeout 5 "$DASHBOARD_URL" > /dev/null; then
            echo "✅ HTTP 서비스: 정상"
            echo "🌐 접속 URL: $DASHBOARD_URL"
            
            # API 응답 확인
            echo "📡 API 응답:"
            curl -s "$DASHBOARD_API" | python3 -m json.tool 2>/dev/null || echo "  API 응답 파싱 실패"
        else
            echo "❌ HTTP 서비스: 응답 없음"
        fi
    else
        echo "❌ 대시보드 프로세스: 실행되지 않음"
    fi
}

open_dashboard() {
    echo "🔗 브라우저에서 대시보드 열기..."
    if command -v open > /dev/null; then
        open "$DASHBOARD_URL"
        echo "✅ 브라우저에서 대시보드를 열었습니다."
    else
        echo "❌ 브라우저 열기 명령을 찾을 수 없습니다."
        echo "🌐 수동으로 접속하세요: $DASHBOARD_URL"
    fi
}

show_log() {
    echo "📋 통합 대시보드 로그 확인..."
    ssh nas "tail -20 ~/desinsight-dashboard/integrated_dashboard.log"
}

# 메인 로직
case "$1" in
    start)
        start_dashboard
        ;;
    stop)
        stop_dashboard
        ;;
    restart)
        restart_dashboard
        ;;
    status)
        check_status
        ;;
    open)
        open_dashboard
        ;;
    log)
        show_log
        ;;
    help|--help|-h)
        show_help
        ;;
    "")
        echo "❓ 명령어를 지정해주세요. 도움말: $0 help"
        ;;
    *)
        echo "❌ 알 수 없는 명령어: $1"
        echo "💡 사용 가능한 명령어: start, stop, restart, status, open, log, help"
        ;;
esac 