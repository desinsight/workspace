#!/bin/bash
# nas_ssh_key_setup.sh - NAS SSH 공개키 붙여넣기 설정 스크립트

echo "🔐 NAS SSH 공개키 붙여넣기 설정"
echo "=============================="

NAS_IP="192.168.219.175"
NAS_USER="admin"

echo ""
echo "📋 1단계: SSH 키 생성 (이미 있으면 건너뛰기)"
echo "==========================================="

if [ ! -f ~/.ssh/nas_key ]; then
    echo "🔑 SSH 키가 없습니다. 새로 생성합니다..."
    ssh-keygen -t ed25519 -C "desinsight-nas-access" -f ~/.ssh/nas_key -N ""
    echo "✅ SSH 키 생성 완료!"
else
    echo "✅ SSH 키가 이미 존재합니다."
fi

echo ""
echo "📋 2단계: 공개키 내용 복사"
echo "========================"
echo "다음 공개키를 클립보드에 복사하세요:"
echo ""
echo "🔑 공개키 내용:"
echo "=============="
cat ~/.ssh/nas_key.pub
echo ""

# 클립보드에 자동 복사 (macOS)
if command -v pbcopy >/dev/null 2>&1; then
    cat ~/.ssh/nas_key.pub | pbcopy
    echo "✅ 공개키가 클립보드에 자동 복사되었습니다!"
else
    echo "💡 위 공개키를 수동으로 복사하세요 (Ctrl+C)"
fi

echo ""
echo "📋 3단계: NAS SSH 접속 및 공개키 등록"
echo "=================================="
echo "이제 NAS에 SSH로 접속해서 공개키를 등록합니다."
echo ""

read -p "🔐 NAS에 SSH 접속을 시작하시겠습니까? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🔗 NAS SSH 접속 중..."
    echo "비밀번호를 입력하세요:"
    
    # NAS SSH 접속 후 공개키 등록 명령어들을 실행
    ssh $NAS_USER@$NAS_IP << 'EOF'
echo ""
echo "🏠 NAS에 접속되었습니다!"
echo "📁 .ssh 디렉토리 생성 중..."
mkdir -p ~/.ssh
chmod 700 ~/.ssh

echo ""
echo "📝 authorized_keys 파일 편집을 시작합니다."
echo "다음 단계를 따라하세요:"
echo ""
echo "1. nano 에디터가 열립니다"
echo "2. 클립보드의 공개키를 붙여넣으세요 (Cmd+V 또는 Ctrl+V)"
echo "3. Ctrl+O 눌러서 저장"
echo "4. Enter 눌러서 확인"
echo "5. Ctrl+X 눌러서 종료"
echo ""
read -p "준비되셨으면 Enter를 누르세요..."

nano ~/.ssh/authorized_keys

echo ""
echo "🔧 파일 권한 설정 중..."
chmod 600 ~/.ssh/authorized_keys

echo ""
echo "✅ authorized_keys 파일 설정 완료!"
echo "📋 등록된 키 확인:"
cat ~/.ssh/authorized_keys

echo ""
echo "🚪 NAS SSH 세션을 종료합니다..."
exit
EOF

    echo ""
    echo "📋 4단계: 홈 디렉토리 권한 수정"
    echo "============================="
    echo "SSH 키 인증이 작동하려면 홈 디렉토리 권한을 수정해야 합니다."
    
    ssh $NAS_USER@$NAS_IP "chmod 755 /volume1/homes/$NAS_USER && ls -la /volume1/homes/$NAS_USER"
    
    echo ""
    echo "📋 5단계: SSH Config 설정"
    echo "======================="
    
    # SSH config 파일 생성/업데이트
    cat > ~/.ssh/config << EOF
# Desinsight NAS 접속 설정
Host desinsight-nas
    HostName $NAS_IP
    User $NAS_USER
    IdentityFile ~/.ssh/nas_key
    IdentitiesOnly yes
    Port 22
    ServerAliveInterval 60
    ServerAliveCountMax 3

# 단축 별칭
Host nas
    HostName $NAS_IP
    User $NAS_USER
    IdentityFile ~/.ssh/nas_key
    IdentitiesOnly yes
EOF
    
    chmod 600 ~/.ssh/config
    echo "✅ SSH config 설정 완료!"
    
    echo ""
    echo "📋 6단계: SSH 키 인증 테스트"
    echo "=========================="
    
    echo "🔍 SSH 키 인증 테스트 중..."
    if ssh -o ConnectTimeout=10 -o BatchMode=yes nas "echo 'SSH 키 인증 성공!'" 2>/dev/null; then
        echo "🎉 SSH 키 인증 완전 성공!"
        echo "✅ 비밀번호 없이 NAS 접속 가능합니다!"
        
        echo ""
        echo "🚀 사용 방법:"
        echo "==========="
        echo "# 간편 접속"
        echo "ssh nas"
        echo ""
        echo "# 원격 명령 실행"
        echo "ssh nas 'docker ps'"
        echo "ssh nas 'ls -la'"
        
    else
        echo "❌ SSH 키 인증 실패"
        echo "💡 문제 해결:"
        echo "1. 공개키가 올바르게 붙여넣어졌는지 확인"
        echo "2. authorized_keys 파일 권한 확인 (600)"
        echo "3. 홈 디렉토리 권한 확인 (755)"
    fi
    
else
    echo ""
    echo "💡 수동 설정 방법:"
    echo "================"
    echo "1. ssh $NAS_USER@$NAS_IP"
    echo "2. mkdir -p ~/.ssh && chmod 700 ~/.ssh"
    echo "3. nano ~/.ssh/authorized_keys"
    echo "4. 공개키 붙여넣기 후 저장"
    echo "5. chmod 600 ~/.ssh/authorized_keys"
    echo "6. chmod 755 /volume1/homes/$NAS_USER"
    echo "7. exit"
fi

echo ""
echo "🎯 설정 완료!"
echo "============"
echo "SSH 키 인증이 설정되었습니다."
echo "이제 'ssh nas' 명령어로 비밀번호 없이 접속할 수 있습니다!" 