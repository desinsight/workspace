"""
SnapCodex - Notion 통합 관리자
Desinsight 건축 자동화 시스템의 핵심 Notion API 연동 모듈
"""
import os
from typing import Dict, List, Optional, Any
from notion_client import Client
from dotenv import load_dotenv
import logging

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotionManager:
    """Notion API 통합 관리 클래스"""
    
    def __init__(self):
        """Notion 클라이언트 초기화"""
        self.notion_token = os.getenv('NOTION_TOKEN')
        if not self.notion_token:
            raise ValueError("NOTION_TOKEN이 설정되지 않았습니다. .env 파일을 확인하세요.")
        
        self.client = Client(auth=self.notion_token)
        
        # 데이터베이스 ID 설정
        self.db_ids = {
            'cost_report': os.getenv('NOTION_DB_ID_COST_REPORT'),
            'cost_db': os.getenv('NOTION_DB_ID_COST_DB'),
            'floor_summary': os.getenv('NOTION_DB_ID_FLOOR_SUMMARY'),
            'room_summary': os.getenv('NOTION_DB_ID_ROOM_SUMMARY'),
            'expense_detail': os.getenv('NOTION_DB_ID_EXPENSE_DETAIL'),
            'unit_price_db': os.getenv('NOTION_DB_ID_UNIT_PRICE_DB'),
            'drawing_db': os.getenv('NOTION_DB_ID_DRAWING_DB')
        }
        
        logger.info("NotionManager 초기화 완료")
    
    def test_connection(self) -> bool:
        """Notion API 연결 테스트"""
        try:
            # 사용자 정보 조회로 연결 테스트
            response = self.client.users.me()
            logger.info(f"Notion 연결 성공: {response.get('name', 'Unknown User')}")
            return True
        except Exception as e:
            logger.error(f"Notion 연결 실패: {str(e)}")
            return False
    
    def get_database_info(self, db_key: str) -> Optional[Dict]:
        """데이터베이스 정보 조회"""
        db_id = self.db_ids.get(db_key)
        if not db_id:
            logger.error(f"데이터베이스 키 '{db_key}'를 찾을 수 없습니다.")
            return None
        
        try:
            # DB ID에서 접두사 제거 (만약 있다면)
            clean_db_id = db_id.replace('DB-', '').replace('-', '')
            
            response = self.client.databases.retrieve(database_id=clean_db_id)
            logger.info(f"데이터베이스 '{db_key}' 정보 조회 성공")
            return response
        except Exception as e:
            logger.error(f"데이터베이스 '{db_key}' 조회 실패: {str(e)}")
            return None
    
    def query_database(self, db_key: str, filter_conditions: Optional[Dict] = None, 
                      sorts: Optional[List] = None, page_size: int = 100) -> List[Dict]:
        """데이터베이스 쿼리 실행"""
        db_id = self.db_ids.get(db_key)
        if not db_id:
            logger.error(f"데이터베이스 키 '{db_key}'를 찾을 수 없습니다.")
            return []
        
        try:
            # DB ID 정리
            clean_db_id = db_id.replace('DB-', '').replace('-', '')
            
            query_params = {
                "database_id": clean_db_id,
                "page_size": page_size
            }
            
            if filter_conditions:
                query_params["filter"] = filter_conditions
            
            if sorts:
                query_params["sorts"] = sorts
            
            response = self.client.databases.query(**query_params)
            results = response.get('results', [])
            
            logger.info(f"데이터베이스 '{db_key}'에서 {len(results)}개 레코드 조회")
            return results
        
        except Exception as e:
            logger.error(f"데이터베이스 '{db_key}' 쿼리 실패: {str(e)}")
            return []
    
    def get_cost_reports(self, project_name: Optional[str] = None) -> List[Dict]:
        """공사비 보고서 데이터 조회"""
        filter_conditions = None
        if project_name:
            filter_conditions = {
                "property": "프로젝트명",
                "title": {
                    "contains": project_name
                }
            }
        
        return self.query_database('cost_report', filter_conditions)
    
    def get_room_summary(self, project_id: Optional[str] = None) -> List[Dict]:
        """실별 집계표 데이터 조회"""
        filter_conditions = None
        if project_id:
            filter_conditions = {
                "property": "프로젝트ID",
                "rich_text": {
                    "equals": project_id
                }
            }
        
        return self.query_database('room_summary', filter_conditions)
    
    def get_unit_prices(self, material_type: Optional[str] = None) -> List[Dict]:
        """단가 DB 조회"""
        filter_conditions = None
        if material_type:
            filter_conditions = {
                "property": "자재구분",
                "select": {
                    "equals": material_type
                }
            }
        
        return self.query_database('unit_price_db', filter_conditions)
    
    def update_room_quantities(self, page_id: str, quantities: Dict[str, Any]) -> bool:
        """실별 수량 정보 업데이트"""
        try:
            properties = {}
            
            # 수량 정보를 Notion 프로퍼티 형식으로 변환
            for key, value in quantities.items():
                if isinstance(value, (int, float)):
                    properties[key] = {"number": value}
                elif isinstance(value, str):
                    properties[key] = {"rich_text": [{"text": {"content": value}}]}
            
            self.client.pages.update(
                page_id=page_id,
                properties=properties
            )
            
            logger.info(f"페이지 {page_id} 수량 정보 업데이트 완료")
            return True
            
        except Exception as e:
            logger.error(f"수량 정보 업데이트 실패: {str(e)}")
            return False
    
    def create_expense_record(self, expense_data: Dict[str, Any]) -> Optional[str]:
        """내역서 레코드 생성"""
        try:
            db_id = self.db_ids.get('expense_detail')
            if not db_id:
                logger.error("내역서 데이터베이스 ID를 찾을 수 없습니다.")
                return None
            
            clean_db_id = db_id.replace('DB-', '').replace('-', '')
            
            # 기본 프로퍼티 구성
            properties = {
                "항목명": {"title": [{"text": {"content": expense_data.get('item_name', '')}}]},
                "수량": {"number": expense_data.get('quantity', 0)},
                "단가": {"number": expense_data.get('unit_price', 0)},
                "금액": {"number": expense_data.get('amount', 0)}
            }
            
            # 추가 프로퍼티 처리
            for key, value in expense_data.items():
                if key not in ['item_name', 'quantity', 'unit_price', 'amount']:
                    if isinstance(value, str):
                        properties[key] = {"rich_text": [{"text": {"content": value}}]}
                    elif isinstance(value, (int, float)):
                        properties[key] = {"number": value}
            
            response = self.client.pages.create(
                parent={"database_id": clean_db_id},
                properties=properties
            )
            
            page_id = response.get('id')
            logger.info(f"내역서 레코드 생성 완료: {page_id}")
            return page_id
            
        except Exception as e:
            logger.error(f"내역서 레코드 생성 실패: {str(e)}")
            return None
    
    def get_all_databases_status(self) -> Dict[str, bool]:
        """모든 데이터베이스 상태 확인"""
        status = {}
        
        for db_key in self.db_ids.keys():
            db_info = self.get_database_info(db_key)
            status[db_key] = db_info is not None
        
        return status

# 사용 예시 및 테스트 함수
def test_notion_connection():
    """Notion 연결 테스트 함수"""
    try:
        manager = NotionManager()
        
        # 연결 테스트
        if manager.test_connection():
            print("✅ Notion API 연결 성공!")
            
            # 모든 데이터베이스 상태 확인
            status = manager.get_all_databases_status()
            print("\n📊 데이터베이스 상태:")
            for db_name, is_accessible in status.items():
                status_icon = "✅" if is_accessible else "❌"
                print(f"{status_icon} {db_name}: {'접근 가능' if is_accessible else '접근 불가'}")
            
            return True
        else:
            print("❌ Notion API 연결 실패!")
            return False
            
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    test_notion_connection()
