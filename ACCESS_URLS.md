# 🌐 Desinsight 실시간 모니터링 대시보드 접속 주소

## ✅ **현재 접속 가능한 URL**

### **🏠 로컬 네트워크 접속**
```
http://192.168.219.175:9090
```
- **용도**: 같은 네트워크 내에서 접속
- **대상**: 집/사무실 내부 디바이스
- **상태**: ✅ 정상 작동

### **🌍 외부 도메인 접속**
```
http://nas.snapcodex.com:9090
```
- **용도**: 인터넷을 통한 외부 접속
- **대상**: 어디서든 접속 가능
- **상태**: ✅ 포트포워딩 설정 완료

---

## 📱 **접속 방법별 안내**

### **💻 PC/Mac에서 접속**
1. 웹 브라우저 열기 (Chrome, Safari, Firefox 등)
2. 주소창에 입력:
   - 내부: `http://192.168.219.175:9090`
   - 외부: `http://nas.snapcodex.com:9090`
3. Enter 키 입력

### **📱 모바일에서 접속**
1. 모바일 브라우저 열기
2. 주소창에 입력: `http://nas.snapcodex.com:9090`
3. 반응형 디자인으로 모바일 최적화됨

### **🏢 오피스에서 접속**
- **같은 네트워크**: `http://192.168.219.175:9090`
- **다른 네트워크**: `http://nas.snapcodex.com:9090`

---

## 🔧 **포트포워딩 설정 정보**

### **라우터 설정값**
```
서비스 이름: NAS Monitoring Dashboard
외부 포트: 9090
내부 IP: 192.168.219.175
내부 포트: 9090
프로토콜: TCP
상태: 활성화 (ON)
```

### **네트워크 구조**
```
인터넷 → nas.snapcodex.com (116.32.88.17) 
       → 라우터 (192.168.219.1) 
       → NAS (192.168.219.175:9090)
```

---

## 📊 **대시보드 기능**

### **실시간 모니터링**
- **5대 디바이스** 상태 모니터링
- **3대 NAS** 시스템 모니터링
- **5초마다** 자동 새로고침
- **하트비트** 수신 기능

### **모니터링 대상**
**디바이스:**
1. HOME iMac i7 64GB (192.168.219.100)
2. Mac Mini M2 Pro 32GB (192.168.219.101)
3. Office iMac i7 40GB (192.168.219.102)
4. Mac Studio M4 Pro 64GB (192.168.219.103)
5. Mobile Ecosystem (mobile)

**NAS 시스템:**
1. SnapCodex NAS (192.168.219.175)
2. Desinsight2 NAS (desinsight2.local)
3. Office NAS (desinsight.synology.me)

---

## 🔌 **API 엔드포인트**

### **REST API 접속**
```
기본 URL: http://nas.snapcodex.com:9090/api
```

**주요 엔드포인트:**
- `GET /api/devices` - 디바이스 상태 조회
- `GET /api/nas` - NAS 상태 조회
- `POST /api/heartbeat` - 하트비트 전송
- `POST /api/register` - 디바이스 등록

### **API 사용 예시**
```bash
# 디바이스 상태 조회
curl http://nas.snapcodex.com:9090/api/devices

# NAS 상태 조회
curl http://nas.snapcodex.com:9090/api/nas

# 하트비트 전송
curl -X POST -H "Content-Type: application/json" \
  -d '{"device_name":"test","cpu":"50%"}' \
  http://nas.snapcodex.com:9090/api/heartbeat
```

---

## 🧪 **접속 테스트**

### **연결 테스트 명령어**
```bash
# 로컬 테스트
curl -s "http://192.168.219.175:9090" | head -5

# 도메인 테스트
curl -s "http://nas.snapcodex.com:9090" | head -5

# 포트 연결 테스트
telnet nas.snapcodex.com 9090
```

### **브라우저 테스트**
1. 브라우저에서 URL 접속
2. "Desinsight 분산 RAG 생태계" 제목 확인
3. 디바이스 카드들이 표시되는지 확인
4. 실시간 데이터 업데이트 확인

---

## 🔒 **보안 및 접근 제어**

### **방화벽 설정**
- 포트 9090 TCP 허용
- CORS 헤더 설정 완료
- 도메인 접속 지원

### **접속 로그**
```bash
# 서버 로그 확인
ssh nas "tail -f ~/desinsight-dashboard/server_9090.log"
```

---

## 🆘 **문제 해결**

### **접속이 안 될 때**
1. **네트워크 확인**: 인터넷 연결 상태
2. **포트 확인**: 9090 포트 차단 여부
3. **서버 상태**: NAS 서버 실행 상태
4. **방화벽**: 라우터/PC 방화벽 설정

### **대안 접속 방법**
```bash
# SSH 터널링 (임시)
ssh -L 9090:192.168.219.175:9090 nas
# 브라우저에서 http://localhost:9090 접속
```

---

## 📞 **지원 정보**

**GitHub 저장소**: https://github.com/desinsight/workspace

**주요 접속 URL 요약:**
- **메인 대시보드**: http://nas.snapcodex.com:9090
- **로컬 접속**: http://192.168.219.175:9090
- **API 베이스**: http://nas.snapcodex.com:9090/api

---

## 🎉 **접속 성공!**

포트포워딩 설정이 완료되어 **어디서든** 다음 주소로 접속 가능합니다:

### **🌟 메인 접속 주소**
```
http://nas.snapcodex.com:9090
```

**✅ 실시간 모니터링 대시보드가 정상 작동 중입니다!** 