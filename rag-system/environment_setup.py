"""
환경별 설정 자동화 스크립트
집 환경(Mac Mini M2 Pro)와 사무실 환경(Mac Studio M4 Max)에 맞는 RAG 시스템을 자동 설정합니다.
"""

import subprocess
import sys
import os
import json
import platform
import psutil
from pathlib import Path
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnvironmentDetector:
    """환경 감지 및 최적화 설정 클래스"""
    
    def __init__(self):
        self.system_info = self.get_system_info()
        self.environment_type = self.detect_environment()
        self.role = self.determine_role()
        
    def get_system_info(self) -> dict:
        """시스템 정보 수집"""
        try:
            # CPU 정보
            cpu_info = platform.processor()
            
            # 메모리 정보
            memory_gb = round(psutil.virtual_memory().total / (1024**3))
            
            # CPU 코어 수
            cpu_cores = psutil.cpu_count()
            
            # macOS에서 칩 정보 확인
            try:
                chip_result = subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'], 
                                           capture_output=True, text=True)
                chip_name = chip_result.stdout.strip()
            except:
                chip_name = cpu_info
            
            return {
                'platform': platform.system(),
                'chip': chip_name,
                'memory_gb': memory_gb,
                'cpu_cores': cpu_cores,
                'architecture': platform.machine()
            }
        except Exception as e:
            logger.error(f"시스템 정보 수집 실패: {e}")
            return {}
    
    def detect_environment(self) -> str:
        """환경 감지 (집/사무실)"""
        chip = self.system_info.get('chip', '').lower()
        memory = self.system_info.get('memory_gb', 0)
        
        if 'm4' in chip and memory >= 60:
            return 'office'  # Mac Studio M4 Max 64GB
        elif 'm2' in chip and memory >= 30:
            return 'home'    # Mac Mini M2 Pro 32GB
        else:
            return 'unknown'
    
    def determine_role(self) -> str:
        """환경에 따른 역할 결정"""
        if self.environment_type == 'office':
            return 'inference'  # 고성능 추론 서버
        elif self.environment_type == 'home':
            return 'embedding'  # 임베딩 생성 서버
        else:
            return 'general'

class RAGSystemSetup:
    """RAG 시스템 자동 설정 클래스"""
    
    def __init__(self):
        self.detector = EnvironmentDetector()
        self.workspace_path = Path.home() / 'workspace'
        self.rag_path = self.workspace_path / 'rag-system'
        self.venv_path = self.rag_path / 'venv'
        
    def run_command(self, command: list, cwd=None) -> bool:
        """명령어 실행"""
        try:
            result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"명령 실행 성공: {' '.join(command)}")
                if result.stdout:
                    logger.info(f"출력: {result.stdout.strip()}")
                return True
            else:
                logger.error(f"명령 실행 실패: {' '.join(command)}")
                logger.error(f"오류: {result.stderr.strip()}")
                return False
        except Exception as e:
            logger.error(f"명령 실행 중 예외: {e}")
            return False
    
    def setup_python_environment(self) -> bool:
        """Python 가상환경 설정"""
        logger.info("Python 가상환경 설정 중...")
        
        # 가상환경 생성
        if not self.venv_path.exists():
            if not self.run_command([sys.executable, '-m', 'venv', str(self.venv_path)]):
                return False
        
        # pip 업그레이드
        pip_path = self.venv_path / 'bin' / 'pip'
        if not self.run_command([str(pip_path), 'install', '--upgrade', 'pip']):
            return False
        
        # 의존성 설치
        requirements_path = self.rag_path / 'requirements.txt'
        if requirements_path.exists():
            if not self.run_command([str(pip_path), 'install', '-r', str(requirements_path)]):
                return False
        
        logger.info("Python 환경 설정 완료")
        return True
    
    def setup_ollama_models(self) -> bool:
        """환경별 Ollama 모델 설정"""
        logger.info(f"{self.detector.environment_type} 환경용 Ollama 모델 설정 중...")
        
        models_to_install = []
        
        if self.detector.environment_type == 'office':
            # 사무실: 고성능 추론 모델
            models_to_install = [
                'llama3.1:70b',    # 고성능 추론
                'codellama:34b',   # 코드 분석
                'mistral:7b'       # 빠른 응답
            ]
        elif self.detector.environment_type == 'home':
            # 집: 경량 모델
            models_to_install = [
                'llama3.1:7b',     # 경량 모델
                'mistral:7b'       # 빠른 처리
            ]
        
        for model in models_to_install:
            logger.info(f"모델 설치 중: {model}")
            if not self.run_command(['ollama', 'pull', model]):
                logger.warning(f"모델 설치 실패: {model}")
                continue
        
        logger.info("Ollama 모델 설정 완료")
        return True
    
    def setup_environment_config(self) -> bool:
        """환경별 설정 파일 생성"""
        logger.info("환경 설정 파일 생성 중...")
        
        config = {
            'environment': {
                'type': self.detector.environment_type,
                'role': self.detector.role,
                'system_info': self.detector.system_info
            },
            'nas': {
                'host': 'desinsight.synology.me',
                'port': 5001,
                'protocol': 'https'
            },
            'local_llm': {
                'host': 'localhost',
                'port': 11434,
                'models': self.get_recommended_models()
            },
            'vector_db': {
                'local_path': str(Path.home() / 'rag_data' / 'vector_db'),
                'cloud_project': 'desinsight-rag-system',
                'cloud_region': 'asia-northeast3'
            },
            'performance': self.get_performance_config()
        }
        
        config_path = self.rag_path / 'config.json'
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        logger.info(f"설정 파일 생성 완료: {config_path}")
        return True
    
    def get_recommended_models(self) -> dict:
        """환경별 권장 모델 반환"""
        if self.detector.environment_type == 'office':
            return {
                'primary': 'llama3.1:70b',
                'code': 'codellama:34b',
                'fast': 'mistral:7b',
                'embedding': 'all-minilm-l6-v2'
            }
        elif self.detector.environment_type == 'home':
            return {
                'primary': 'llama3.1:7b',
                'fast': 'mistral:7b',
                'embedding': 'all-minilm-l6-v2'
            }
        else:
            return {
                'primary': 'llama3.1:7b',
                'embedding': 'all-minilm-l6-v2'
            }
    
    def get_performance_config(self) -> dict:
        """성능 최적화 설정"""
        memory_gb = self.detector.system_info.get('memory_gb', 8)
        cpu_cores = self.detector.system_info.get('cpu_cores', 4)
        
        if self.detector.environment_type == 'office':
            # Mac Studio M4 Max 최적화
            return {
                'max_workers': min(cpu_cores, 16),
                'batch_size': 64,
                'max_memory_gb': min(memory_gb * 0.7, 45),
                'gpu_acceleration': True,
                'parallel_inference': True
            }
        elif self.detector.environment_type == 'home':
            # Mac Mini M2 Pro 최적화
            return {
                'max_workers': min(cpu_cores, 8),
                'batch_size': 32,
                'max_memory_gb': min(memory_gb * 0.6, 20),
                'gpu_acceleration': True,
                'parallel_embedding': True
            }
        else:
            return {
                'max_workers': min(cpu_cores, 4),
                'batch_size': 16,
                'max_memory_gb': min(memory_gb * 0.5, 8),
                'gpu_acceleration': False
            }
    
    def setup_directories(self) -> bool:
        """필요한 디렉토리 생성"""
        logger.info("디렉토리 구조 생성 중...")
        
        directories = [
            self.rag_path,
            self.rag_path / 'data',
            self.rag_path / 'models',
            self.rag_path / 'logs',
            Path.home() / 'rag_data',
            Path.home() / 'rag_data' / 'nas_collected',
            Path.home() / 'rag_data' / 'vector_db',
            Path.home() / 'rag_data' / 'processed'
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"디렉토리 생성: {directory}")
        
        return True
    
    def create_startup_scripts(self) -> bool:
        """시작 스크립트 생성"""
        logger.info("시작 스크립트 생성 중...")
        
        # 공통 시작 스크립트
        startup_script = f"""#!/bin/bash

echo "🚀 Desinsight RAG 시스템 시작 ({self.detector.environment_type} 환경)"

# 가상환경 활성화
source {self.venv_path}/bin/activate

# 환경 변수 로드
export PYTHONPATH="{self.rag_path}:$PYTHONPATH"
export RAG_ENVIRONMENT="{self.detector.environment_type}"
export RAG_ROLE="{self.detector.role}"

# Ollama 서비스 확인
if ! pgrep -f ollama > /dev/null; then
    echo "Ollama 서비스 시작 중..."
    ollama serve &
    sleep 5
fi

# 환경별 서비스 시작
"""
        
        if self.detector.environment_type == 'office':
            startup_script += """
# 사무실 환경: 추론 서버 시작
echo "🏢 추론 서버 시작 중..."
python inference_server.py &

# 클라우드 동기화 서비스
echo "☁️ 클라우드 동기화 서비스 시작 중..."
python cloud_sync_service.py &
"""
        elif self.detector.environment_type == 'home':
            startup_script += """
# 집 환경: 임베딩 서버 시작
echo "🏠 임베딩 서버 시작 중..."
python embedding_server.py &

# NAS 데이터 수집 스케줄러
echo "📁 NAS 데이터 수집 스케줄러 시작 중..."
python nas_scheduler.py &
"""
        
        startup_script += """
echo "✅ RAG 시스템 시작 완료!"
echo "📊 모니터링: http://localhost:8080"
echo "📚 API 문서: http://localhost:8000/docs"
"""
        
        script_path = self.rag_path / 'start_rag_system.sh'
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(startup_script)
        
        # 실행 권한 부여
        os.chmod(script_path, 0o755)
        
        logger.info(f"시작 스크립트 생성 완료: {script_path}")
        return True
    
    def run_setup(self) -> bool:
        """전체 설정 실행"""
        logger.info(f"🎯 {self.detector.environment_type} 환경 RAG 시스템 설정 시작")
        logger.info(f"시스템 정보: {self.detector.system_info}")
        
        steps = [
            ("디렉토리 생성", self.setup_directories),
            ("Python 환경 설정", self.setup_python_environment),
            ("Ollama 모델 설정", self.setup_ollama_models),
            ("환경 설정 파일 생성", self.setup_environment_config),
            ("시작 스크립트 생성", self.create_startup_scripts)
        ]
        
        for step_name, step_func in steps:
            logger.info(f"📋 {step_name} 시작...")
            try:
                if not step_func():
                    logger.error(f"❌ {step_name} 실패")
                    return False
                logger.info(f"✅ {step_name} 완료")
            except Exception as e:
                logger.error(f"❌ {step_name} 중 오류: {e}")
                return False
        
        self.print_completion_message()
        return True
    
    def print_completion_message(self):
        """완료 메시지 출력"""
        print("\n🎉 RAG 시스템 설정 완료!")
        print(f"\n📊 환경 정보:")
        print(f"   🏷️  환경: {self.detector.environment_type}")
        print(f"   🎯 역할: {self.detector.role}")
        print(f"   🖥️  칩: {self.detector.system_info.get('chip')}")
        print(f"   💾 메모리: {self.detector.system_info.get('memory_gb')}GB")
        
        print(f"\n🚀 시작 방법:")
        print(f"   cd {self.rag_path}")
        print(f"   ./start_rag_system.sh")
        
        print(f"\n📁 주요 경로:")
        print(f"   설정 파일: {self.rag_path}/config.json")
        print(f"   데이터 저장: {Path.home()}/rag_data/")
        print(f"   로그 파일: {self.rag_path}/logs/")
        
        if self.detector.environment_type == 'home':
            print(f"\n🏠 집 환경 다음 단계:")
            print(f"   1. NAS 인증 정보 설정:")
            print(f"      export NAS_USERNAME='your_username'")
            print(f"      export NAS_PASSWORD='your_password'")
            print(f"   2. 데이터 수집 시작:")
            print(f"      python nas_data_collector.py")
            
        elif self.detector.environment_type == 'office':
            print(f"\n🏢 사무실 환경 다음 단계:")
            print(f"   1. Google Cloud 인증:")
            print(f"      gcloud auth login")
            print(f"   2. 집 환경과 연결 테스트")
            print(f"   3. RAG 질의응답 테스트")

def main():
    """메인 함수"""
    try:
        setup = RAGSystemSetup()
        success = setup.run_setup()
        
        if success:
            print("\n✅ 모든 설정이 성공적으로 완료되었습니다!")
            sys.exit(0)
        else:
            print("\n❌ 설정 중 오류가 발생했습니다.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️ 사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"예기치 못한 오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
