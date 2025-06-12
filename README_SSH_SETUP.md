# 🔐 NAS SSH 키 인증 설정 스크립트 모음

## 📋 **스크립트 종류**

### **1. 🚀 원클릭 자동 설정 (권장)**
```bash
./nas_ssh_auto.sh
```
- **특징**: 완전 자동화, 비밀번호 1회 입력만 필요
- **시간**: 약 30초
- **난이도**: ⭐ (가장 쉬움)

### **2. 📝 간단 수동 설정**
```bash
./nas_ssh_simple.sh
```
- **특징**: 공개키 복사 후 수동 붙여넣기
- **시간**: 약 2분
- **난이도**: ⭐⭐ (쉬움)

### **3. 🔧 상세 가이드 설정**
```bash
./nas_ssh_key_setup.sh
```
- **특징**: 단계별 상세 안내, 대화형 설정
- **시간**: 약 3-5분
- **난이도**: ⭐⭐⭐ (보통)

## 🎯 **권장 사용 순서**

### **처음 설정하는 경우**
```bash
# 1. 원클릭 자동 설정 시도
./nas_ssh_auto.sh

# 2. 실패 시 간단 수동 설정
./nas_ssh_simple.sh

# 3. 문제 발생 시 상세 가이드
./nas_ssh_key_setup.sh
```

### **이미 SSH 키가 있는 경우**
```bash
# 기존 키 확인
ls -la ~/.ssh/nas_key*

# 있으면 바로 자동 설정
./nas_ssh_auto.sh
```

## 📊 **설정 완료 후 확인**

### **SSH 키 인증 테스트**
```bash
# 비밀번호 없이 접속되면 성공
ssh nas

# 원격 명령 실행 테스트
ssh nas "echo 'SSH 키 인증 성공!'"
```

### **설정 상태 확인**
```bash
# SSH 키 파일 확인
ls -la ~/.ssh/nas_key*

# SSH config 확인
cat ~/.ssh/config

# NAS authorized_keys 확인
ssh nas "cat ~/.ssh/authorized_keys"
```

## 🔧 **문제 해결**

### **자주 발생하는 문제들**

#### **1. "Permission denied" 오류**
```bash
# 홈 디렉토리 권한 확인
ssh admin@192.168.219.175 "ls -la /volume1/homes/admin"

# 권한 수정
ssh admin@192.168.219.175 "chmod 755 /volume1/homes/admin"
```

#### **2. "Connection refused" 오류**
```bash
# NAS SSH 서비스 확인
# DSM 웹 → 제어판 → 터미널 및 SNMP → SSH 서비스 활성화
```

#### **3. SSH 키 파일 권한 문제**
```bash
# 권한 수정
chmod 700 ~/.ssh
chmod 600 ~/.ssh/nas_key
chmod 644 ~/.ssh/nas_key.pub
chmod 600 ~/.ssh/config
```

## 🚀 **설정 완료 후 활용법**

### **기본 사용법**
```bash
# NAS 접속
ssh nas

# 원격 명령 실행
ssh nas "docker ps"
ssh nas "ls -la"
ssh nas "df -h"
```

### **파일 전송 (향후 SFTP 활성화 시)**
```bash
# 파일 업로드
scp file.txt nas:~/

# 파일 다운로드
scp nas:~/file.txt ./

# 디렉토리 동기화
rsync -avz ./local_dir/ nas:~/remote_dir/
```

### **포트 포워딩**
```bash
# NAS 웹 인터페이스 로컬 접속
ssh -L 8080:localhost:5000 nas

# Docker 컨테이너 포트 포워딩
ssh -L 8888:localhost:8888 nas
```

## 📁 **생성되는 파일들**

### **로컬 PC**
- `~/.ssh/nas_key` - 개인키 (600 권한)
- `~/.ssh/nas_key.pub` - 공개키 (644 권한)
- `~/.ssh/config` - SSH 설정 (600 권한)

### **NAS**
- `~/.ssh/authorized_keys` - 인증된 공개키 목록 (600 권한)
- `/volume1/homes/admin/` - 홈 디렉토리 (755 권한)

## 🎉 **성공 지표**

### **✅ 설정 완료 확인**
- [ ] `ssh nas` 명령어로 비밀번호 없이 접속
- [ ] `ssh nas "echo test"` 원격 명령 실행 성공
- [ ] SSH config 별칭 작동
- [ ] 홈 디렉토리 권한 755
- [ ] authorized_keys 파일 존재 및 권한 600

### **🎯 최종 목표 달성**
- ✅ **비밀번호 없는 SSH 접속**
- ✅ **원격 명령 자동화 가능**
- ✅ **향후 스크립트 자동화 준비**
- ✅ **보안 강화 (키 기반 인증)**

## 💡 **추가 팁**

### **여러 PC에서 동일한 키 사용**
```bash
# 키 파일 복사
scp ~/.ssh/nas_key* other-pc:~/.ssh/
scp ~/.ssh/config other-pc:~/.ssh/
```

### **키 백업**
```bash
# 안전한 곳에 키 백업
cp ~/.ssh/nas_key* ~/Dropbox/ssh-keys/
```

### **보안 강화**
```bash
# 패스프레이즈 추가 (선택사항)
ssh-keygen -p -f ~/.ssh/nas_key
``` 