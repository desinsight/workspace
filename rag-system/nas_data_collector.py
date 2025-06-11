"""
Desinsight NAS 데이터 수집기
기존 회사 NAS (desinsight.synology.me:5001)에서 프로젝트 데이터를 수집하여 RAG 시스템에 학습시킵니다.
"""

import os
import json
import asyncio
import aiohttp
import aiofiles
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import logging
import hashlib

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NASDataCollector:
    """기존 NAS에서 데이터를 수집하는 클래스"""
    
    def __init__(self):
        self.nas_host = "desinsight.synology.me"
        self.nas_port = 5001
        self.nas_protocol = "https"
        self.base_url = f"{self.nas_protocol}://{self.nas_host}:{self.nas_port}"
        
        # 인증 정보 (환경 변수에서 로드)
        self.username = os.getenv('NAS_USERNAME')
        self.password = os.getenv('NAS_PASSWORD')
        
        # 수집 대상 디렉토리
        self.target_directories = [
            "/projects/",           # 프로젝트 파일들
            "/documents/",          # 문서들
            "/drawings/",           # 도면 파일들
            "/cost_calculations/",  # 원가 계산서들
            "/reports/",            # 보고서들
            "/templates/"           # 템플릿들
        ]
        
        # 수집 대상 파일 확장자
        self.target_extensions = {
            'documents': ['.pdf', '.docx', '.doc', '.txt', '.md'],
            'drawings': ['.dwg', '.dxf', '.pdf'],
            'spreadsheets': ['.xlsx', '.xls', '.csv'],
            'images': ['.png', '.jpg', '.jpeg', '.tiff'],
            'cad': ['.dwg', '.dxf', '.ifc', '.rvt']
        }
        
        # 로컬 저장 경로
        self.local_storage = Path.home() / "rag_data" / "nas_collected"
        self.local_storage.mkdir(parents=True, exist_ok=True)
        
        # 메타데이터 저장
        self.metadata_db = self.local_storage / "metadata.json"
        self.collected_files = self.load_metadata()
    
    def load_metadata(self) -> Dict:
        """기존 수집 메타데이터 로드"""
        if self.metadata_db.exists():
            with open(self.metadata_db, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"last_update": None, "files": {}}
    
    def save_metadata(self):
        """메타데이터 저장"""
        with open(self.metadata_db, 'w', encoding='utf-8') as f:
            json.dump(self.collected_files, f, indent=2, ensure_ascii=False)
    
    async def authenticate(self, session: aiohttp.ClientSession) -> Optional[str]:
        """NAS 인증"""
        try:
            # Synology API 인증 엔드포인트
            auth_url = f"{self.base_url}/webapi/auth.cgi"
            auth_params = {
                'api': 'SYNO.API.Auth',
                'version': '2',
                'method': 'login',
                'account': self.username,
                'passwd': self.password,
                'session': 'FileStation',
                'format': 'sid'
            }
            
            async with session.get(auth_url, params=auth_params, ssl=False) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get('success'):
                        sid = result['data']['sid']
                        logger.info("NAS 인증 성공")
                        return sid
                    else:
                        logger.error(f"인증 실패: {result.get('error')}")
                        return None
                else:
                    logger.error(f"인증 요청 실패: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"인증 중 오류: {str(e)}")
            return None
    
    async def list_files(self, session: aiohttp.ClientSession, sid: str, folder_path: str) -> List[Dict]:
        """디렉토리의 파일 목록 조회"""
        try:
            list_url = f"{self.base_url}/webapi/entry.cgi"
            list_params = {
                'api': 'SYNO.FileStation.List',
                'version': '2',
                'method': 'list',
                'folder_path': folder_path,
                'additional': 'real_path,size,time,perm,type',
                '_sid': sid
            }
            
            async with session.get(list_url, params=list_params, ssl=False) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get('success'):
                        return result['data']['files']
                    else:
                        logger.warning(f"폴더 조회 실패: {folder_path} - {result.get('error')}")
                        return []
                else:
                    logger.warning(f"폴더 조회 요청 실패: {folder_path} - {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"파일 목록 조회 중 오류: {str(e)}")
            return []
    
    def is_target_file(self, file_info: Dict) -> bool:
        """수집 대상 파일인지 확인"""
        if file_info.get('isdir', False):
            return False
        
        file_name = file_info.get('name', '')
        file_ext = Path(file_name).suffix.lower()
        
        # 모든 대상 확장자 확인
        for category, extensions in self.target_extensions.items():
            if file_ext in extensions:
                return True
        
        return False
    
    def get_file_hash(self, file_path: str, file_size: int, modify_time: int) -> str:
        """파일 고유 해시 생성 (경로 + 크기 + 수정시간)"""
        hash_input = f"{file_path}:{file_size}:{modify_time}"
        return hashlib.md5(hash_input.encode()).hexdigest()
    
    async def download_file(self, session: aiohttp.ClientSession, sid: str, file_info: Dict) -> Optional[Path]:
        """파일 다운로드"""
        try:
            file_path = file_info['path']
            file_name = file_info['name']
            file_size = file_info.get('additional', {}).get('size', 0)
            modify_time = file_info.get('additional', {}).get('time', {}).get('mtime', 0)
            
            # 파일 해시로 중복 확인
            file_hash = self.get_file_hash(file_path, file_size, modify_time)
            
            # 이미 수집된 파일인지 확인
            if file_hash in self.collected_files.get('files', {}):
                logger.info(f"이미 수집된 파일 건너뛰기: {file_name}")
                return None
            
            # 로컬 저장 경로 생성
            # 디렉토리 구조 유지
            relative_path = file_path.lstrip('/')
            local_file_path = self.local_storage / relative_path
            local_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 다운로드 URL
            download_url = f"{self.base_url}/webapi/entry.cgi"
            download_params = {
                'api': 'SYNO.FileStation.Download',
                'version': '2',
                'method': 'download',
                'path': file_path,
                'mode': 'download',
                '_sid': sid
            }
            
            # 파일 다운로드
            async with session.get(download_url, params=download_params, ssl=False) as response:
                if response.status == 200:
                    async with aiofiles.open(local_file_path, 'wb') as f:
                        async for chunk in response.content.iter_chunked(8192):
                            await f.write(chunk)
                    
                    # 메타데이터 업데이트
                    self.collected_files['files'][file_hash] = {
                        'original_path': file_path,
                        'local_path': str(local_file_path),
                        'file_name': file_name,
                        'file_size': file_size,
                        'modify_time': modify_time,
                        'collected_at': datetime.now().isoformat(),
                        'file_type': self.categorize_file(file_name)
                    }
                    
                    logger.info(f"파일 다운로드 완료: {file_name} ({file_size} bytes)")
                    return local_file_path
                    
                else:
                    logger.error(f"파일 다운로드 실패: {file_name} - {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"파일 다운로드 중 오류: {str(e)}")
            return None
    
    def categorize_file(self, file_name: str) -> str:
        """파일 카테고리 분류"""
        file_ext = Path(file_name).suffix.lower()
        
        for category, extensions in self.target_extensions.items():
            if file_ext in extensions:
                return category
        
        return 'unknown'
    
    async def collect_from_directory(self, session: aiohttp.ClientSession, sid: str, directory: str) -> int:
        """특정 디렉토리에서 파일 수집"""
        logger.info(f"디렉토리 수집 시작: {directory}")
        collected_count = 0
        
        # 파일 목록 조회
        files = await self.list_files(session, sid, directory)
        
        for file_info in files:
            if file_info.get('isdir', False):
                # 서브디렉토리 재귀 처리
                subdir_path = file_info['path']
                sub_count = await self.collect_from_directory(session, sid, subdir_path)
                collected_count += sub_count
            else:
                # 파일 처리
                if self.is_target_file(file_info):
                    downloaded_file = await self.download_file(session, sid, file_info)
                    if downloaded_file:
                        collected_count += 1
        
        logger.info(f"디렉토리 수집 완료: {directory} ({collected_count}개 파일)")
        return collected_count
    
    async def collect_all_data(self) -> Dict:
        """모든 대상 디렉토리에서 데이터 수집"""
        logger.info("NAS 데이터 수집 시작")
        start_time = datetime.now()
        total_collected = 0
        
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            # NAS 인증
            sid = await self.authenticate(session)
            if not sid:
                logger.error("NAS 인증 실패")
                return {"success": False, "error": "Authentication failed"}
            
            # 각 디렉토리에서 데이터 수집
            for directory in self.target_directories:
                try:
                    count = await self.collect_from_directory(session, sid, directory)
                    total_collected += count
                except Exception as e:
                    logger.error(f"디렉토리 수집 실패: {directory} - {str(e)}")
                    continue
        
        # 메타데이터 업데이트 및 저장
        self.collected_files['last_update'] = datetime.now().isoformat()
        self.save_metadata()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        result = {
            "success": True,
            "total_collected": total_collected,
            "duration_seconds": duration,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "storage_path": str(self.local_storage)
        }
        
        logger.info(f"데이터 수집 완료: {total_collected}개 파일, {duration:.2f}초 소요")
        return result

# 사용 예시
async def main():
    """메인 실행 함수"""
    # 환경 변수 확인
    if not os.getenv('NAS_USERNAME') or not os.getenv('NAS_PASSWORD'):
        logger.error("NAS 인증 정보가 설정되지 않았습니다.")
        logger.info("다음 환경 변수를 설정하세요:")
        logger.info("export NAS_USERNAME='your_username'")
        logger.info("export NAS_PASSWORD='your_password'")
        return
    
    # 데이터 수집 실행
    collector = NASDataCollector()
    result = await collector.collect_all_data()
    
    if result["success"]:
        print(f"✅ 데이터 수집 성공!")
        print(f"   📁 수집된 파일: {result['total_collected']}개")
        print(f"   ⏰ 소요 시간: {result['duration_seconds']:.2f}초")
        print(f"   💾 저장 위치: {result['storage_path']}")
    else:
        print(f"❌ 데이터 수집 실패: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    asyncio.run(main())
