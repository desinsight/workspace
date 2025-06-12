# 🔐 NAS SSH 키 인증 설정 완벽 가이드

## 🎯 목표
- **비밀번호 없이 NAS 접근**
- **rsync, scp 자동화**
- **보안 강화 및 편의성 증대**

## 1️⃣ SSH 키 생성 (로컬 PC)

### 🔑 새 SSH 키 생성
```bash
# SSH 키 생성 (RSA 4096비트)
ssh-keygen -t rsa -b 4096 -C "desinsight-nas-access" -f ~/.ssh/nas_key

# 또는 ED25519 (더 안전)
ssh-keygen -t ed25519 -C "desinsight-nas-access" -f ~/.ssh/nas_key
```

### 📋 키 생성 옵션
- **패스프레이즈**: 빈 값 입력 (자동화용) 또는 강력한 패스프레이즈 설정
- **파일명**: `nas_key` (개인키), `nas_key.pub` (공개키)

### ✅ 생성 확인
```bash
ls -la ~/.ssh/nas_key*
# 결과:
# -rw-------  1 user  staff  3381 nas_key      (개인키)
# -rw-r--r--  1 user  staff   743 nas_key.pub  (공개키)
```

## 2️⃣ NAS SSH 서비스 활성화

### 🌐 DSM 웹 관리 설정
1. **http://192.168.219.175:5000** 접속
2. **제어판** → **터미널 및 SNMP**
3. **SSH 서비스 사용** 체크
4. **포트**: 22 (기본값) 또는 사용자 정의
5. **적용** 클릭

### 🔧 고급 SSH 설정 (선택사항)
- **SSH 키 인증만 허용**: 보안 강화
- **루트 로그인 비활성화**: 권장
- **포트 변경**: 22 → 2222 등 (보안 강화)

## 3️⃣ 공개키 NAS에 등록

### 🚀 방법 A: ssh-copy-id 사용 (가장 쉬움)
```bash
# 공개키 자동 복사
ssh-copy-id -i ~/.ssh/nas_key.pub admin@192.168.219.175

# 포트가 다를 경우
ssh-copy-id -i ~/.ssh/nas_key.pub -p 2222 admin@192.168.219.175
```

### 📋 방법 B: 수동 등록
```bash
# 1. 공개키 내용 복사
cat ~/.ssh/nas_key.pub

# 2. NAS SSH 접속 (비밀번호 입력)
ssh admin@192.168.219.175

# 3. NAS에서 authorized_keys 파일 생성
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2E... 복사한내용" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
exit
```

### 🌐 방법 C: DSM 웹 인터페이스
1. **제어판** → **사용자 계정**
2. **admin 계정 편집**
3. **SSH 공개키** 탭
4. **가져오기** → `nas_key.pub` 파일 업로드

## 4️⃣ SSH 키 인증 테스트

### ✅ 연결 테스트
```bash
# 키 인증으로 접속 (비밀번호 없이)
ssh -i ~/.ssh/nas_key admin@192.168.219.175

# 성공 시 NAS 터미널 접속됨
# 실패 시 아래 디버그 섹션 참고
```

### 🔍 연결 디버그
```bash
# 상세 로그로 문제 진단
ssh -v -i ~/.ssh/nas_key admin@192.168.219.175

# 더 자세한 로그
ssh -vvv -i ~/.ssh/nas_key admin@192.168.219.175
```

## 5️⃣ SSH Config 설정 (편의성)

### 📝 ~/.ssh/config 파일 생성
```bash
cat << EOF >> ~/.ssh/config
# Desinsight NAS 접속 설정
Host desinsight-nas
    HostName 192.168.219.175
    User admin
    IdentityFile ~/.ssh/nas_key
    IdentitiesOnly yes
    Port 22
    ServerAliveInterval 60
    ServerAliveCountMax 3

# 단축 별칭
Host nas
    HostName 192.168.219.175
    User admin
    IdentityFile ~/.ssh/nas_key
    IdentitiesOnly yes
EOF
```

### 🚀 간편 접속
```bash
# 이제 이렇게 간단하게 접속
ssh nas
ssh desinsight-nas

# rsync도 간편하게
rsync -avz ./docker-images-export/ nas:/volume1/docker-images/
```

## 6️⃣ 자동화 스크립트 활용

### 📤 키 인증 기반 업로드 스크립트
```bash
#!/bin/bash
# upload_to_nas_keyauth.sh

NAS_HOST="nas"  # SSH config 별칭 사용
SOURCE_DIR="./docker-images-export/"
TARGET_DIR="/volume1/docker-images/"

echo "🔐 SSH 키 인증으로 NAS 업로드"
echo "=============================="

# SSH 연결 테스트
if ssh $NAS_HOST "echo 'SSH 연결 성공'" 2>/dev/null; then
    echo "✅ SSH 키 인증 성공"
else
    echo "❌ SSH 키 인증 실패"
    exit 1
fi

# 디렉토리 생성
ssh $NAS_HOST "mkdir -p $TARGET_DIR"

# rsync 업로드
echo "📤 파일 업로드 시작..."
rsync -avz --progress $SOURCE_DIR $NAS_HOST:$TARGET_DIR

if [ $? -eq 0 ]; then
    echo "✅ 업로드 완료!"
else
    echo "❌ 업로드 실패"
    exit 1
fi
```

## 7️⃣ 보안 강화 설정

### 🔒 NAS SSH 보안 설정
```bash
# NAS SSH 접속 후 설정 파일 편집
ssh nas
sudo vi /etc/ssh/sshd_config

# 권장 설정:
PasswordAuthentication no           # 비밀번호 인증 비활성화
PubkeyAuthentication yes           # 키 인증만 허용
PermitRootLogin no                 # 루트 로그인 금지
Port 2222                         # 기본 포트 변경
MaxAuthTries 3                    # 인증 시도 제한

# SSH 서비스 재시작
sudo systemctl restart ssh
```

### 🛡️ 방화벽 설정 (선택사항)
```bash
# 특정 IP만 SSH 접근 허용
# DSM → 제어판 → 보안 → 방화벽
# 규칙: SSH(22) → 특정 IP 대역만 허용
```

## 8️⃣ 트러블슈팅

### ❌ 자주 발생하는 문제들

#### 🔐 권한 문제
```bash
# SSH 키 권한 수정
chmod 700 ~/.ssh
chmod 600 ~/.ssh/nas_key
chmod 644 ~/.ssh/nas_key.pub
chmod 600 ~/.ssh/config
```

#### 🔍 NAS SSH 서비스 확인
```bash
# SSH 서비스 상태 확인
ssh nas "sudo systemctl status ssh"

# SSH 설정 파일 검증
ssh nas "sudo sshd -t"
```

#### 📋 공개키 등록 확인
```bash
# NAS authorized_keys 파일 확인
ssh nas "cat ~/.ssh/authorized_keys"
```

## 9️⃣ 완성된 워크플로우

### 🎯 최종 사용법
```bash
# 1. Docker 이미지 저장
./save_docker_images.sh

# 2. NAS 업로드 (키 인증)
rsync -avz ./docker-images-export/ nas:/volume1/docker-images/

# 3. 다른 PC에서 다운로드
scp nas:/volume1/docker-images/desinsight_*.tar.gz .

# 4. Docker 이미지 로드
docker load -i desinsight_*.tar.gz
```

## 🏆 성공 지표
- ✅ **비밀번호 입력 없이 SSH 접속**
- ✅ **rsync 자동 업로드**
- ✅ **다른 PC에서 원클릭 다운로드**
- ✅ **보안 강화 (키 인증만 허용)** 