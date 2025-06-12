#!/usr/bin/env python3
# device_monitoring_agent.py - 디바이스 모니터링 에이전트

import json
import time
import subprocess
import platform
import socket
import psutil
import requests
from datetime import datetime

class DeviceMonitoringAgent:
    def __init__(self, dashboard_url="http://192.168.219.175:5004", device_name=None):
        self.dashboard_url = dashboard_url
        self.device_name = device_name or self.get_device_name()
        self.device_ip = self.get_local_ip()
        self.system_info = self.get_system_info()
        
        print(f"🖥️  디바이스 모니터링 에이전트 시작")
        print(f"📱 디바이스명: {self.device_name}")
        print(f"🌐 IP 주소: {self.device_ip}")
        print(f"📡 대시보드: {self.dashboard_url}")
    
    def get_device_name(self):
        """디바이스 이름 자동 감지"""
        hostname = socket.gethostname()
        system = platform.system()
        
        # macOS에서 더 친숙한 이름 생성
        if system == "Darwin":
            try:
                # 시스템 정보 조회
                result = subprocess.run(['system_profiler', 'SPHardwareDataType'], 
                                      capture_output=True, text=True)
                if "iMac" in result.stdout:
                    return f"{hostname} (iMac)"
                elif "MacBook" in result.stdout:
                    return f"{hostname} (MacBook)"
                elif "Mac mini" in result.stdout:
                    return f"{hostname} (Mac Mini)"
                elif "Mac Studio" in result.stdout:
                    return f"{hostname} (Mac Studio)"
            except:
                pass
        
        return f"{hostname} ({system})"
    
    def get_local_ip(self):
        """로컬 IP 주소 조회"""
        try:
            # 외부 연결을 통해 로컬 IP 확인
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def get_system_info(self):
        """시스템 정보 수집"""
        try:
            cpu_count = psutil.cpu_count()
            memory = psutil.virtual_memory()
            memory_gb = round(memory.total / (1024**3))
            
            system_info = {
                "hostname": socket.gethostname(),
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
                "cpu_count": cpu_count,
                "memory_gb": memory_gb,
                "python_version": platform.python_version()
            }
            
            return system_info
        except Exception as e:
            print(f"❌ 시스템 정보 수집 실패: {e}")
            return {}
    
    def get_cpu_usage(self):
        """CPU 사용률 조회"""
        try:
            # 1초 간격으로 CPU 사용률 측정
            cpu_percent = psutil.cpu_percent(interval=1)
            return f"{cpu_percent:.0f}%"
        except Exception as e:
            print(f"❌ CPU 사용률 조회 실패: {e}")
            return "0%"
    
    def get_memory_usage(self):
        """메모리 사용률 조회"""
        try:
            memory = psutil.virtual_memory()
            return f"{memory.percent:.0f}%"
        except Exception as e:
            print(f"❌ 메모리 사용률 조회 실패: {e}")
            return "0%"
    
    def get_disk_usage(self):
        """디스크 사용률 조회"""
        try:
            disk = psutil.disk_usage('/')
            return f"{disk.percent:.0f}%"
        except Exception as e:
            print(f"❌ 디스크 사용률 조회 실패: {e}")
            return "0%"
    
    def get_network_info(self):
        """네트워크 정보 조회"""
        try:
            net_io = psutil.net_io_counters()
            return {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv
            }
        except Exception as e:
            print(f"❌ 네트워크 정보 조회 실패: {e}")
            return {}
    
    def collect_monitoring_data(self):
        """모니터링 데이터 수집"""
        try:
            data = {
                "device_name": self.device_name,
                "ip": self.device_ip,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "cpu": self.get_cpu_usage(),
                "memory": self.get_memory_usage(),
                "disk": self.get_disk_usage(),
                "network": self.get_network_info(),
                "system_info": self.system_info,
                "status": "online"
            }
            
            return data
        except Exception as e:
            print(f"❌ 모니터링 데이터 수집 실패: {e}")
            return None
    
    def send_heartbeat(self, data):
        """대시보드로 하트비트 전송"""
        try:
            response = requests.post(
                f"{self.dashboard_url}/api/heartbeat",
                json=data,
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✅ 하트비트 전송 성공: {data['timestamp']}")
                return True
            else:
                print(f"❌ 하트비트 전송 실패: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 대시보드 연결 실패: {e}")
            return False
        except Exception as e:
            print(f"❌ 하트비트 전송 오류: {e}")
            return False
    
    def register_device(self):
        """디바이스 등록"""
        try:
            registration_data = {
                "name": self.device_name,
                "ip": self.device_ip,
                "system_info": self.system_info,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            response = requests.post(
                f"{self.dashboard_url}/api/register",
                json=registration_data,
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✅ 디바이스 등록 성공")
                return True
            else:
                print(f"❌ 디바이스 등록 실패: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 디바이스 등록 오류: {e}")
            return False
    
    def run(self, interval=10):
        """모니터링 에이전트 실행"""
        print(f"🚀 모니터링 에이전트 시작 (간격: {interval}초)")
        
        # 디바이스 등록 시도
        self.register_device()
        
        try:
            while True:
                # 모니터링 데이터 수집
                data = self.collect_monitoring_data()
                
                if data:
                    # 대시보드로 전송
                    success = self.send_heartbeat(data)
                    
                    if success:
                        print(f"📊 CPU: {data['cpu']}, 메모리: {data['memory']}, 디스크: {data['disk']}")
                    else:
                        print(f"⚠️  대시보드 연결 실패 - 재시도 중...")
                
                # 대기
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n🛑 모니터링 에이전트 종료")
        except Exception as e:
            print(f"❌ 에이전트 실행 오류: {e}")

def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description="디바이스 모니터링 에이전트")
    parser.add_argument("--dashboard", default="http://192.168.219.175:5004", 
                       help="대시보드 URL")
    parser.add_argument("--name", help="디바이스 이름 (자동 감지)")
    parser.add_argument("--interval", type=int, default=10, 
                       help="모니터링 간격 (초)")
    
    args = parser.parse_args()
    
    # psutil 설치 확인
    try:
        import psutil
    except ImportError:
        print("❌ psutil 라이브러리가 필요합니다.")
        print("💡 설치 명령어: pip install psutil requests")
        return
    
    # 에이전트 시작
    agent = DeviceMonitoringAgent(
        dashboard_url=args.dashboard,
        device_name=args.name
    )
    
    agent.run(interval=args.interval)

if __name__ == "__main__":
    main() 