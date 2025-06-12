# 🔧 포트 충돌 해결 및 포트포워딩 설정

## ⚠️ **문제 상황**
- 포트 5005가 이미 사용 중
- 포트 8080도 nginx에서 사용 중
- 대안 포트 필요

## 📊 **현재 사용 중인 포트**

```bash
# NAS에서 사용 중인 포트들
5000 - 사용 중
5001 - 사용 중  
5005 - 사용 중 (우리 서버)
5006 - 사용 중
8080 - nginx 사용 중
```

## ✅ **해결 방안: 포트 9090 사용**

### **1️⃣ 새로운 포트포워딩 설정값**

```
서비스 이름: NAS Monitoring Dashboard
외부 포트: 9090
내부 IP: 192.168.219.175
내부 포트: 9090
프로토콜: TCP
상태: 활성화
```

### **2️⃣ 라우터 설정 단계**

**브라우저에서 라우터 접속:**
```
http://192.168.219.1
```

**포트포워딩 설정:**

| 항목 | 기존값 | 새로운 값 |
|------|--------|-----------|
| **Service Name** | `NAS Monitoring` | `NAS Monitoring 9090` |
| **External Port** | `5005` | `9090` |
| **Internal IP** | `192.168.219.175` | `192.168.219.175` |
| **Internal Port** | `5005` | `9090` |
| **Protocol** | `TCP` | `TCP` |

### **3️⃣ 브랜드별 설정 예시**

**🔸 ASUS 라우터:**
```
Service Name: NAS Monitoring 9090
Port Range: 9090
Local IP: 192.168.219.175
Local Port: 9090
Protocol: TCP
```

**🔸 TP-Link 라우터:**
```
Service Type: Custom
External Port: 9090
Internal IP: 192.168.219.175
Internal Port: 9090
Protocol: TCP
Status: Enabled
```

**🔸 Netgear 라우터:**
```
Service Name: NAS_Monitoring_9090
Service Type: TCP
External Starting Port: 9090
External Ending Port: 9090
Internal Starting Port: 9090
Internal Ending Port: 9090
Internal IP Address: 192.168.219.175
```

### **4️⃣ 설정 후 접속 URL**

**로컬 네트워크:**
```
http://192.168.219.175:9090
```

**외부 도메인 (포트포워딩 설정 후):**
```
http://nas.snapcodex.com:9090
```

## 🧪 **테스트 명령어**

### **로컬 테스트:**
```bash
curl -s "http://192.168.219.175:9090" | head -5
```

### **도메인 테스트 (포트포워딩 설정 후):**
```bash
curl -s "http://nas.snapcodex.com:9090" | head -5
```

### **포트 연결 테스트:**
```bash
telnet nas.snapcodex.com 9090
```

## 🔄 **대안 포트 목록**

포트 9090이 안 될 경우 다음 포트들을 시도:

| 포트 | 용도 | 추천도 |
|------|------|--------|
| **9090** | 일반 웹 서비스 | ⭐⭐⭐⭐⭐ |
| **8888** | 대안 웹 포트 | ⭐⭐⭐⭐ |
| **3000** | Node.js 기본 | ⭐⭐⭐ |
| **4000** | 개발 서버 | ⭐⭐⭐ |
| **7777** | 사용자 정의 | ⭐⭐ |

## 📱 **모바일 접속**

포트포워딩 설정 후 모바일에서도 접속 가능:
```
http://nas.snapcodex.com:9090
```

## 🔒 **보안 고려사항**

**방화벽 설정:**
```bash
# NAS에서 포트 9090 허용
sudo ufw allow 9090/tcp
```

**접속 로그 모니터링:**
```bash
# 접속 로그 확인
ssh nas "tail -f ~/desinsight-dashboard/domain_server_9090.log"
```

## ⚡ **즉시 적용 가능한 임시 해결책**

**SSH 터널링:**
```bash
# 로컬에서 실행
ssh -L 9090:192.168.219.175:9090 nas

# 브라우저에서 접속
http://localhost:9090
```

## 📋 **설정 체크리스트**

- [ ] 라우터 관리 페이지 접속 (http://192.168.219.1)
- [ ] 포트포워딩 메뉴 찾기
- [ ] 새 규칙 추가 (포트 9090)
- [ ] 설정 저장 및 적용
- [ ] 라우터 재시작 (필요시)
- [ ] 로컬 테스트 (http://192.168.219.175:9090)
- [ ] 외부 테스트 (http://nas.snapcodex.com:9090)

## 🎯 **최종 목표**

**설정 완료 후 접속 가능한 URL:**
- ✅ 로컬: http://192.168.219.175:9090
- ✅ 도메인: http://nas.snapcodex.com:9090
- ✅ 모바일: http://nas.snapcodex.com:9090

**포트 9090을 사용하여 포트포워딩을 설정하시면 됩니다!** 