#!/usr/bin/env python3
"""
Desinsight 분산형 RAG 시스템 - 기본 버전 (의존성 최소화)
"""

import os
import ollama
import json
from datetime import datetime
from typing import List, Dict
import hashlib

class SimpleRAGSystem:
    def __init__(self):
        print("🎯 Desinsight RAG 시스템 초기화...")
        
        # Ollama 연결
        self.ollama_client = ollama.Client()
        
        # 문서 저장소 (간단한 텍스트 매칭 사용)
        self.documents = []
        
        print("✅ RAG 시스템 초기화 완료!")
    
    def add_document(self, text: str, metadata: Dict = None):
        """문서를 저장소에 추가"""
        print(f"📄 문서 추가: {text[:50]}...")
        
        # 메타데이터 설정
        if metadata is None:
            metadata = {}
        metadata['added_at'] = datetime.now().isoformat()
        metadata['doc_id'] = hashlib.md5(text.encode()).hexdigest()[:8]
        
        # 저장
        doc_entry = {
            'text': text,
            'metadata': metadata,
            'keywords': self._extract_keywords(text)
        }
        
        self.documents.append(doc_entry)
        print(f"✅ 문서 추가 완료 (총 {len(self.documents)}개)")
    
    def _extract_keywords(self, text: str) -> List[str]:
        """간단한 키워드 추출"""
        # 한글과 영문 키워드 추출
        words = text.replace(',', ' ').replace('.', ' ').split()
        keywords = []
        
        for word in words:
            word = word.strip('()[]{}:;,.')
            if len(word) > 1:  # 2글자 이상만
                keywords.append(word.lower())
        
        return list(set(keywords))  # 중복 제거
    
    def search_documents(self, query: str, k: int = 3) -> List[Dict]:
        """키워드 기반 문서 검색"""
        if not self.documents:
            return []
        
        print(f"🔍 검색 쿼리: {query}")
        
        query_keywords = self._extract_keywords(query)
        scores = []
        
        for i, doc in enumerate(self.documents):
            # 키워드 매칭 점수 계산
            doc_keywords = doc['keywords']
            common_keywords = set(query_keywords) & set(doc_keywords)
            
            # 텍스트 직접 포함 확인
            text_matches = sum(1 for keyword in query_keywords if keyword in doc['text'].lower())
            
            score = len(common_keywords) * 2 + text_matches
            if score > 0:
                scores.append((score, i))
        
        # 점수순 정렬
        scores.sort(reverse=True)
        results = []
        
        for score, doc_idx in scores[:k]:
            doc = self.documents[doc_idx]
            results.append({
                'text': doc['text'],
                'score': score,
                'metadata': doc['metadata']
            })
            print(f"  📌 점수 {score}: {doc['text'][:50]}...")
        
        return results
    
    def ask_question(self, question: str) -> str:
        """RAG 기반 질의응답"""
        print(f"\n❓ 질문: {question}")
        
        # 1. 관련 문서 검색
        relevant_docs = self.search_documents(question, k=3)
        
        if not relevant_docs:
            return "죄송합니다. 관련 정보를 찾을 수 없습니다."
        
        # 2. 컨텍스트 구성
        context = "\n".join([doc['text'] for doc in relevant_docs])
        
        # 3. 프롬프트 구성
        prompt = f"""
다음 정보를 바탕으로 질문에 답변해주세요:

정보:
{context}

질문: {question}

답변을 한국어로 정확하고 자세하게 해주세요."""
        
        print("🤖 LLM 답변 생성 중...")
        
        # 4. Ollama로 답변 생성
        try:
            response = self.ollama_client.chat(
                model='llama3.2:3b',
                messages=[
                    {
                        'role': 'system',
                        'content': '당신은 건축 및 건설 전문가입니다. 주어진 정보를 바탕으로 정확하고 도움이 되는 답변을 한국어로 해주세요.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )
            
            answer = response['message']['content']
            print(f"💡 답변: {answer}")
            return answer
            
        except Exception as e:
            print(f"❌ LLM 오류: {e}")
            return f"답변 생성 중 오류가 발생했습니다: {e}"
    
    def save_knowledge_base(self, filename: str = "knowledge_base.json"):
        """지식베이스 저장"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.documents, f, ensure_ascii=False, indent=2)
        print(f"💾 지식베이스 저장됨: {filename}")
    
    def load_knowledge_base(self, filename: str = "knowledge_base.json"):
        """지식베이스 로드"""
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                self.documents = json.load(f)
            print(f"📂 지식베이스 로드됨: {filename} ({len(self.documents)}개 문서)")
        else:
            print(f"⚠️ 지식베이스 파일이 없습니다: {filename}")

def main():
    """RAG 시스템 테스트"""
    print("🚀 Desinsight 분산형 RAG 시스템 기본 테스트 시작\n")
    
    # RAG 시스템 초기화
    rag = SimpleRAGSystem()
    
    # 샘플 건축 문서들 추가
    print("\n📚 샘플 문서 추가 중...")
    
    documents = [
        {
            'text': '아파트 건설에서 철근콘크리트 구조는 내구성과 경제성을 동시에 확보할 수 있는 최적의 구조 방식입니다. 일반적으로 25~30층 건물에 적합하며, 압축강도 24~30MPa의 콘크리트를 사용합니다.',
            'metadata': {'type': 'structural', 'category': 'concrete'}
        },
        {
            'text': '건축물의 단열성능은 외벽 단열재의 두께와 직결됩니다. 중부지역 기준으로 외벽 단열재는 최소 100mm 이상, 지붕은 200mm 이상 시공해야 에너지 효율 1등급을 달성할 수 있습니다.',
            'metadata': {'type': 'insulation', 'category': 'energy_efficiency'}
        },
        {
            'text': '건설현장에서 안전관리는 최우선 과제입니다. 헬멧, 안전벨트, 안전화 착용은 기본이며, 고소작업 시에는 반드시 안전난간과 추락방지망을 설치해야 합니다.',
            'metadata': {'type': 'safety', 'category': 'construction_safety'}
        },
        {
            'text': '건축 도면에서 1:100 축척은 평면도와 입면도 작성에 가장 많이 사용됩니다. 이 축척에서는 벽체 두께, 문창호 위치, 구조체 배치가 명확하게 표현되어 시공자가 이해하기 쉽습니다.',
            'metadata': {'type': 'drawing', 'category': 'architectural_plan'}
        },
        {
            'text': '건축 비용 산정에서 평방미터당 건축비는 구조, 마감재, 지역에 따라 크게 달라집니다. 일반적으로 아파트는 평방미터당 120-150만원, 단독주택은 150-200만원 정도입니다.',
            'metadata': {'type': 'cost', 'category': 'construction_cost'}
        }
    ]
    
    for doc in documents:
        rag.add_document(doc['text'], doc['metadata'])
    
    # 지식베이스 저장
    rag.save_knowledge_base()
    
    # 테스트 질문들
    print("\n🧪 RAG 시스템 테스트 질문들:")
    
    test_questions = [
        "아파트 건설에 적합한 구조는 무엇인가요?",
        "건물 단열재 두께는 어떻게 정해야 하나요?",
        "건설현장 안전관리 방법을 알려주세요.",
        "건축도면 축척에 대해 설명해주세요.",
        "아파트 건축비용은 얼마나 되나요?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*60}")
        print(f"🔸 테스트 {i}/{len(test_questions)}")
        answer = rag.ask_question(question)
        print(f"{'='*60}")
        if i < len(test_questions):  # 마지막이 아니면 잠시 대기
            import time
            time.sleep(1)
    
    print("\n🎯 RAG 시스템 테스트 완료!")
    print("\n📊 결과 요약:")
    print(f"  • 문서 수: {len(rag.documents)}개")
    print(f"  • 검색 방식: 키워드 기반 매칭")
    print(f"  • LLM 모델: llama3.2:3b")
    print("  • 지식베이스: knowledge_base.json 저장됨")

if __name__ == "__main__":
    main() 