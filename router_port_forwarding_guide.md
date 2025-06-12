# 🌐 라우터 포트포워딩 설정 가이드

## 📋 **설정 정보**

### **기본 정보**
- **라우터 IP**: 192.168.219.1
- **NAS IP**: 192.168.219.175
- **서비스 포트**: 5005
- **목표 도메인**: nas.snapcodex.com

### **포트포워딩 설정값**
```
서비스 이름: NAS Monitoring Dashboard
외부 포트: 5005
내부 IP: 192.168.219.175
내부 포트: 5005
프로토콜: TCP
상태: 활성화
```

---

## 🔧 **단계별 설정 방법**

### **1단계: 라우터 관리 페이지 접속**

**브라우저에서 접속:**
```
http://192.168.219.1
```

**일반적인 기본 로그인 정보:**
- 사용자명: `admin`
- 비밀번호: `admin` 또는 `password` 또는 라우터 뒷면 스티커 확인

### **2단계: 포트포워딩 메뉴 찾기**

**메뉴 위치 (브랜드별):**

**🔹 공통 메뉴명:**
- Port Forwarding
- Virtual Server
- NAT Forwarding
- Application & Gaming
- 고급 설정 > 포트포워딩

**🔹 브랜드별 메뉴:**
- **ASUS**: 고급 설정 > WAN > Virtual Server/Port Forwarding
- **TP-Link**: 고급 > NAT Forwarding > Virtual Servers
- **Netgear**: Dynamic DNS > Port Forwarding/Port Triggering
- **D-Link**: 고급 > Port Forwarding
- **Linksys**: Smart Wi-Fi Tools > Port Range Forwarding

### **3단계: 새 규칙 추가**

**설정 항목:**

| 항목 | 값 | 설명 |
|------|-----|------|
| **Service Name** | `NAS Monitoring` | 규칙 이름 |
| **External Port** | `5005` | 외부에서 접속할 포트 |
| **Internal IP** | `192.168.219.175` | NAS 서버 IP |
| **Internal Port** | `5005` | NAS 서버 포트 |
| **Protocol** | `TCP` | 프로토콜 유형 |
| **Status** | `Enabled` | 활성화 |

### **4단계: 설정 저장 및 재시작**

1. **저장**: "Save" 또는 "Apply" 버튼 클릭
2. **재시작**: 라우터 재시작 (필요시)
3. **확인**: 설정이 저장되었는지 확인

---

## 📱 **브랜드별 상세 설정**

### **🔸 ASUS 라우터**

**경로:** 고급 설정 > WAN > Virtual Server/Port Forwarding

**설정 화면:**
```
Service Name: NAS Monitoring
Port Range: 5005
Local IP: 192.168.219.175
Local Port: 5005
Protocol: TCP
```

### **🔸 TP-Link 라우터**

**경로:** 고급 > NAT Forwarding > Virtual Servers

**설정 화면:**
```
Service Type: Custom
External Port: 5005
Internal IP: 192.168.219.175
Internal Port: 5005
Protocol: TCP
Status: Enabled
```

### **🔸 Netgear 라우터**

**경로:** Dynamic DNS > Port Forwarding/Port Triggering

**설정 화면:**
```
Service Name: NAS_Monitoring
Service Type: TCP
External Starting Port: 5005
External Ending Port: 5005
Internal Starting Port: 5005
Internal Ending Port: 5005
Internal IP Address: 192.168.219.175
```

### **🔸 공유기 웹 인터페이스 예시**

**일반적인 설정 화면:**
```
┌─────────────────────────────────────────────────────────┐
│                Port Forwarding Rules                    │
├─────────────────────────────────────────────────────────┤
│ Service Name: [NAS Monitoring              ]            │
│ Protocol:     [TCP ▼]                                   │
│ External Port:[5005    ] ~ [5005    ]                   │
│ Internal IP:  [192.168.219.175]                         │
│ Internal Port:[5005    ] ~ [5005    ]                   │
│ Status:       [☑] Enable                                │
│                                                         │
│ [Add Rule] [Delete] [Save] [Cancel]                     │
└─────────────────────────────────────────────────────────┘
```

---

## 🧪 **설정 후 테스트**

### **1. 내부 네트워크 테스트**

<function_calls>
<invoke name="run_terminal_cmd">
<parameter name="command">curl -s --connect-timeout 5 "http://192.168.219.175:5005" | head -3
</invoke>
</function_calls> 