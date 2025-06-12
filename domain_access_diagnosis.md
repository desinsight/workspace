# 🔍 nas.snapcodex.com 도메인 접속 실패 진단 보고서

## 📊 **진단 결과 요약**

### ✅ **정상 작동 항목**
- ✅ 로컬 NAS 연결 (192.168.219.175) - 정상
- ✅ 도메인 DNS 해석 (nas.snapcodex.com → 116.32.88.17) - 정상
- ✅ NAS 서버 실행 상태 - 포트 5005에서 정상 실행 중
- ✅ 로컬 네트워크 내 접속 - http://192.168.219.175:5005 정상

### ❌ **문제 항목**
- ❌ 외부 도메인 접속 - http://nas.snapcodex.com:5005 타임아웃
- ❌ 포트포워딩 미설정 - 외부에서 내부 서버 접근 불가

---

## 🔍 **상세 진단 분석**

### **1. 네트워크 구조 분석**

```
인터넷 (외부)
    ↓
공인 IP: 116.32.88.17 (nas.snapcodex.com)
    ↓
라우터/방화벽 (포트포워딩 필요)
    ↓
사설 IP: 192.168.219.175 (NAS 서버)
    ↓
포트 5005 (모니터링 대시보드)
```

### **2. 문제 원인**

**주요 원인: 포트포워딩 미설정**
- 도메인 `nas.snapcodex.com`은 공인 IP `116.32.88.17`로 해석됨
- 하지만 라우터에서 포트 5005를 내부 NAS로 포워딩하지 않음
- 외부 요청이 NAS 서버에 도달하지 못함

### **3. 현재 서버 상태**

```bash
# NAS 서버 실행 상태
Process: python3 enhanced_realtime_domain_5005.py (PID: 354)
Port: 5005 (LISTENING)
Local Access: ✅ http://192.168.219.175:5005
External Access: ❌ http://nas.snapcodex.com:5005
```

---

## 🛠️ **해결 방안**

### **방안 1: 포트포워딩 설정 (권장)**

**라우터 설정:**
1. 라우터 관리 페이지 접속: http://192.168.219.1
2. 포트포워딩 설정:
   - 외부 포트: 5005
   - 내부 IP: 192.168.219.175
   - 내부 포트: 5005
   - 프로토콜: TCP

**설정 후 접속 URL:**
```
http://nas.snapcodex.com:5005
```

### **방안 2: 리버스 프록시 설정**

**Nginx 설정 (포트 80 사용):**
```nginx
server {
    listen 80;
    server_name nas.snapcodex.com;
    
    location / {
        proxy_pass http://192.168.219.175:5005;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**설정 후 접속 URL:**
```
http://nas.snapcodex.com (포트 없이 접속)
```

### **방안 3: 표준 포트 사용**

**포트 80 또는 443 사용:**
- 포트 80: HTTP (기본 웹 포트)
- 포트 443: HTTPS (SSL 포트)
- 대부분의 방화벽에서 기본 허용

---

## ⚡ **즉시 적용 가능한 해결책**

### **임시 해결책: SSH 터널링**

```bash
# 로컬에서 SSH 터널 생성
ssh -L 5005:192.168.219.175:5005 nas

# 브라우저에서 접속
http://localhost:5005
```

### **영구 해결책: 포트포워딩**

**1단계: 라우터 접속**
```bash
# 게이트웨이 IP 확인
route -n get default | grep gateway

# 일반적인 라우터 IP
http://192.168.219.1
http://192.168.1.1
http://10.0.0.1
```

**2단계: 포트포워딩 규칙 추가**
```
Service Name: NAS Monitoring
External Port: 5005
Internal IP: 192.168.219.175
Internal Port: 5005
Protocol: TCP
```

---

## 🧪 **테스트 명령어**

### **로컬 테스트**
```bash
curl -s "http://192.168.219.175:5005" | head -5
```

### **도메인 테스트 (포트포워딩 설정 후)**
```bash
curl -s "http://nas.snapcodex.com:5005" | head -5
```

### **포트 연결 테스트**
```bash
telnet nas.snapcodex.com 5005
```

---

## 📋 **체크리스트**

### **설정 전 확인사항**
- [ ] NAS 서버 실행 상태 확인
- [ ] 로컬 네트워크 접속 테스트
- [ ] 라우터 관리자 권한 확보

### **포트포워딩 설정 후 확인사항**
- [ ] 외부에서 도메인 접속 테스트
- [ ] 방화벽 설정 확인
- [ ] SSL 인증서 설정 (선택사항)

---

## 🔧 **추가 최적화**

### **보안 강화**
```bash
# 방화벽 설정
sudo ufw allow 5005/tcp

# SSL 인증서 설정
sudo certbot --nginx -d nas.snapcodex.com
```

### **성능 최적화**
```bash
# Nginx 캐싱 설정
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

---

## 📞 **지원 정보**

**현재 접속 가능한 URL:**
- 로컬: http://192.168.219.175:5005
- SSH 터널: http://localhost:5005 (터널 설정 후)

**목표 URL:**
- 도메인: http://nas.snapcodex.com:5005 (포트포워딩 설정 후)
- 리버스 프록시: http://nas.snapcodex.com (Nginx 설정 후)

**문제 해결 우선순위:**
1. 포트포워딩 설정 (가장 간단)
2. 리버스 프록시 설정 (포트 없이 접속)
3. SSL 인증서 설정 (HTTPS 지원) 