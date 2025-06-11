#!/usr/bin/env python3
"""
Desinsight 분산형 RAG 시스템 - 기본 테스트
"""

import os
import ollama
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
import json
from datetime import datetime

class SimpleRAGSystem:
    def __init__(self):
        print("🎯 Desinsight RAG 시스템 초기화...")
        
        # Ollama 연결
        self.ollama_client = ollama.Client()
        
        # 임베딩 모델 로드 (가벼운 버전)
        print("📦 임베딩 모델 로드 중...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # 메모리 벡터 저장소 (임시)
        self.vector_store = []
        self.documents = []
        
        print("✅ RAG 시스템 초기화 완료!")
    
    def add_document(self, text: str, metadata: Dict = None):
        """문서를 벡터 저장소에 추가"""
        print(f"📄 문서 추가: {text[:50]}...")
        
        # 텍스트 임베딩 생성
        embedding = self.embedding_model.encode(text)
        
        # 메타데이터 설정
        if metadata is None:
            metadata = {}
        metadata['added_at'] = datetime.now().isoformat()
        
        # 저장
        doc_entry = {
            'text': text,
            'embedding': embedding,
            'metadata': metadata
        }
        
        self.documents.append(doc_entry)
        self.vector_store.append(embedding)
        
        print(f"✅ 문서 추가 완료 (총 {len(self.documents)}개)")
    
    def similarity_search(self, query: str, k: int = 3) -> List[Dict]:
        """유사도 검색"""
        if not self.documents:
            return []
        
        print(f"🔍 검색 쿼리: {query}")
        
        # 쿼리 임베딩
        query_embedding = self.embedding_model.encode(query)
        
        # 코사인 유사도 계산
        similarities = []
        for i, doc_embedding in enumerate(self.vector_store):
            similarity = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )
            similarities.append((similarity, i))
        
        # 상위 k개 문서 반환
        similarities.sort(reverse=True)
        results = []
        
        for sim_score, doc_idx in similarities[:k]:
            doc = self.documents[doc_idx]
            results.append({
                'text': doc['text'],
                'similarity': float(sim_score),
                'metadata': doc['metadata']
            })
            print(f"  📌 유사도 {sim_score:.3f}: {doc['text'][:50]}...")
        
        return results
    
    def ask_question(self, question: str) -> str:
        """RAG 기반 질의응답"""
        print(f"\n❓ 질문: {question}")
        
        # 1. 관련 문서 검색
        relevant_docs = self.similarity_search(question, k=3)
        
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

답변:"""
        
        print("🤖 LLM 답변 생성 중...")
        
        # 4. Ollama로 답변 생성
        try:
            response = self.ollama_client.chat(
                model='llama3.2:3b',
                messages=[
                    {
                        'role': 'system',
                        'content': '당신은 건축 및 건설 전문가입니다. 주어진 정보를 바탕으로 정확하고 도움이 되는 답변을 해주세요.'
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

def main():
    """RAG 시스템 테스트"""
    print("🚀 Desinsight 분산형 RAG 시스템 테스트 시작\n")
    
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
        }
    ]
    
    for doc in documents:
        rag.add_document(doc['text'], doc['metadata'])
    
    # 테스트 질문들
    print("\n🧪 RAG 시스템 테스트 질문들:")
    
    test_questions = [
        "아파트 건설에 적합한 구조는 무엇인가요?",
        "건물 단열재 두께는 어떻게 정해야 하나요?",
        "건설현장 안전관리 방법을 알려주세요.",
        "건축도면 축척에 대해 설명해주세요."
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*60}")
        print(f"🔸 테스트 {i}/4")
        answer = rag.ask_question(question)
        print(f"{'='*60}")
    
    print("\n🎯 RAG 시스템 테스트 완료!")
    print("\n📊 결과 요약:")
    print(f"  • 문서 수: {len(rag.documents)}개")
    print(f"  • 임베딩 모델: {rag.embedding_model.model_name}")
    print(f"  • LLM 모델: llama3.2:3b")
    print(f"  • 벡터 차원: {len(rag.vector_store[0]) if rag.vector_store else 0}")

if __name__ == "__main__":
    main() 