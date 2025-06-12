#!/bin/bash

# 🏢 오피스 디바이스 모니터링 설정 가이드
# Office iMac i7 40GB (192.168.219.102)에서 실행

echo "🏢 오피스 디바이스 모니터링 설정을 시작합니다..."

# 색상 코드
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}1️⃣ 필수 패키지 설치${NC}"
echo "pip3 install psutil requests"

echo -e "\n${BLUE}2️⃣ 모니터링 에이전트 다운로드${NC}"
echo "curl -O https://raw.githubusercontent.com/desinsight/workspace/main/device_monitoring_agent.py"

echo -e "\n${BLUE}3️⃣ 에이전트 실행${NC}"
echo "python3 device_monitoring_agent.py \\"
echo "  --name \"Office iMac i7 40GB\" \\"
echo "  --dashboard \"http://192.168.219.175:5004\" \\"
echo "  --interval 5"

echo -e "\n${BLUE}4️⃣ 백그라운드 실행 (선택사항)${NC}"
echo "nohup python3 device_monitoring_agent.py \\"
echo "  --name \"Office iMac i7 40GB\" \\"
echo "  --dashboard \"http://192.168.219.175:5004\" \\"
echo "  --interval 5 > monitoring.log 2>&1 &"

echo -e "\n${BLUE}5️⃣ 대시보드 접속 확인${NC}"
echo "브라우저에서 http://192.168.219.175:5004 접속"

echo -e "\n${GREEN}✅ 설정 완료 후 대시보드에서 'Office iMac i7 40GB'가 온라인으로 표시됩니다${NC}"

echo -e "\n${YELLOW}📱 모바일에서도 같은 URL로 접속 가능합니다${NC}"
echo -e "${YELLOW}🌐 외부에서 접속하려면 포트포워딩 설정이 필요합니다${NC}" 