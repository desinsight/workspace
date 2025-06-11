#!/usr/bin/env python3
"""
Desinsight 분산형 RAG 시스템 - 환경별 설정 관리자
"""

import os
import platform
import subprocess
import psutil
from dataclasses import dataclass
from typing import Dict, List, Optional
import json

@dataclass
class SystemSpec:
    """시스템 사양"""
    model_name: str
    cpu_cores: int
    memory_gb: float
    gpu_info: str
    role: str  # 'embedding', 'inference', 'hybrid'

class DistributedRAGConfig:
    def __init__(self):
        self.system_spec = self.detect_system()
        self.config = self.generate_config()
        
    def detect_system(self) -> SystemSpec:
        """현재 시스템 사양 감지"""
        print("🔍 시스템 환경 감지 중...")
        
        # CPU 정보
        cpu_cores = psutil.cpu_count()
        memory_gb = psutil.virtual_memory().total / (1024**3)
        
        # Mac 모델 감지
        model_name = "Unknown"
        if platform.system() == "Darwin":
            try:
                result = subprocess.run(['system_profiler', 'SPHardwareDataType'], 
                                      capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Model Name:' in line:
                        model_name = line.split(':')[1].strip()
                        break
                    elif 'Model Identifier:' in line:
                        model_name = line.split(':')[1].strip()
                        break
            except:
                pass
        
        # GPU 정보 (간단하게)
        gpu_info = "Integrated"
        if "M4 Max" in model_name or "Mac Studio" in model_name:
            gpu_info = "M4 Max GPU"
        elif "M2" in model_name or "Mac Mini" in model_name:
            gpu_info = "M2 GPU"
        elif "iMac" in model_name:
            gpu_info = "Intel Integrated"
            
        # 역할 결정
        role = self.determine_role(model_name, memory_gb, cpu_cores)
        
        spec = SystemSpec(
            model_name=model_name,
            cpu_cores=cpu_cores,
            memory_gb=memory_gb,
            gpu_info=gpu_info,
            role=role
        )
        
        print(f"✅ 시스템 감지 완료:")
        print(f"  • 모델: {spec.model_name}")
        print(f"  • CPU: {spec.cpu_cores}코어")
        print(f"  • 메모리: {spec.memory_gb:.1f}GB")
        print(f"  • GPU: {spec.gpu_info}")
        print(f"  • 역할: {spec.role}")
        
        return spec
    
    def determine_role(self, model_name: str, memory_gb: float, cpu_cores: int) -> str:
        """하드웨어 기반 역할 결정"""
        if "Mac Studio" in model_name and "M4 Max" in model_name:
            return "inference"  # 고성능 추론 서버
        elif "Mac Mini" in model_name and "M2" in model_name:
            return "embedding"  # 임베딩 생성 서버
        elif memory_gb >= 32:
            return "hybrid"     # 복합 처리 가능
        else:
            return "embedding"  # 기본적으로 임베딩 처리
    
    def generate_config(self) -> Dict:
        """역할별 최적화 설정 생성"""
        base_config = {
            'system': {
                'role': self.system_spec.role,
                'model_name': self.system_spec.model_name,
                'cpu_cores': self.system_spec.cpu_cores,
                'memory_gb': self.system_spec.memory_gb
            },
            'ollama': {},
            'rag': {},
            'network': {},
            'storage': {}
        }
        
        if self.system_spec.role == "inference":
            # 사무실 Mac Studio M4 Max - 고성능 추론 최적화
            base_config.update({
                'ollama': {
                    'models': ['llama3.1:70b', 'codellama:34b', 'mistral:7b'],
                    'concurrent_requests': 4,
                    'context_length': 8192,
                    'gpu_layers': -1  # 모든 레이어 GPU 사용
                },
                'rag': {
                    'search_k': 5,
                    'max_context_length': 4000,
                    'temperature': 0.3,
                    'enable_caching': True
                },
                'network': {
                    'listen_port': 8000,
                    'enable_api': True,
                    'cors_origins': ['*']
                }
            })
            
        elif self.system_spec.role == "embedding":
            # 집 Mac Mini M2 Pro - 임베딩 생성 최적화
            base_config.update({
                'ollama': {
                    'models': ['llama3.2:3b', 'nomic-embed-text'],
                    'concurrent_requests': 2,
                    'context_length': 4096
                },
                'rag': {
                    'embedding_batch_size': 32,
                    'vector_dimensions': 384,
                    'similarity_threshold': 0.7,
                    'enable_preprocessing': True
                },
                'storage': {
                    'vector_db_path': './vector_store',
                    'backup_enabled': True,
                    'sync_to_cloud': True
                }
            })
            
        else:  # hybrid
            # 균형잡힌 설정
            base_config.update({
                'ollama': {
                    'models': ['llama3.2:3b', 'llama3.1:8b'],
                    'concurrent_requests': 2,
                    'context_length': 4096
                },
                'rag': {
                    'search_k': 3,
                    'max_context_length': 2000,
                    'temperature': 0.5
                }
            })
            
        return base_config
    
    def save_config(self, filename: str = "rag_config.json"):
        """설정 파일 저장"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
        print(f"💾 설정 저장됨: {filename}")
    
    def print_deployment_guide(self):
        """배포 가이드 출력"""
        print("\n🚀 분산 RAG 시스템 배포 가이드")
        print("="*50)
        
        if self.system_spec.role == "inference":
            print("📍 현재 환경: 추론 서버 (사무실)")
            print("\n🎯 권장 작업:")
            print("1. 대형 LLM 모델 설치:")
            print("   ollama pull llama3.1:70b")
            print("   ollama pull codellama:34b")
            print("\n2. API 서버 시작:")
            print("   python3 inference_server.py")
            print("\n3. 네트워크 설정:")
            print("   - 포트 8000 개방")
            print("   - 집 환경에서 접근 가능하도록 설정")
            
        elif self.system_spec.role == "embedding":
            print("📍 현재 환경: 임베딩 서버 (집)")
            print("\n🎯 권장 작업:")
            print("1. 임베딩 모델 설치:")
            print("   ollama pull nomic-embed-text")
            print("\n2. 데이터 수집 시작:")
            print("   python3 nas_data_collector.py")
            print("\n3. 벡터 DB 구축:")
            print("   python3 build_vector_store.py")
            
        else:  # hybrid
            print("📍 현재 환경: 하이브리드 (개발/테스트)")
            print("\n🎯 권장 작업:")
            print("1. 기본 모델 확인:")
            print("   ollama list")
            print("\n2. 로컬 테스트:")
            print("   python3 simple_rag_basic.py")
        
        print(f"\n💡 현재 시스템 리소스:")
        print(f"   • CPU 활용도: {psutil.cpu_percent()}%")
        print(f"   • 메모리 사용량: {psutil.virtual_memory().percent}%")
        print(f"   • 디스크 여유 공간: {psutil.disk_usage('/').free / (1024**3):.1f}GB")

def main():
    """설정 관리자 실행"""
    print("🎯 Desinsight 분산형 RAG 시스템 설정 관리자\n")
    
    config_manager = DistributedRAGConfig()
    config_manager.save_config()
    config_manager.print_deployment_guide()
    
    print("\n🔥 다음 단계:")
    print("1. NAS 데이터 수집기 실행")
    print("2. 환경별 최적화 설정 적용") 
    print("3. 분산 네트워크 연결 테스트")

if __name__ == "__main__":
    main() 