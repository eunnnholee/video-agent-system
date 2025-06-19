import os
import json
import logging
import chromadb
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from openai import OpenAI
from dotenv import load_dotenv
import numpy as np
from chromadb.utils import embedding_functions

# 환경 변수 로드
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 로깅 설정
logger = logging.getLogger(__name__)

# 상수 정의
DATA_DIR = Path("data")
CHROMA_DIR = Path("chroma_db")
COLLECTION_NAME = "prompt_embeddings"

# Chroma 클라이언트 초기화
def get_chroma_client():
    CHROMA_DIR.mkdir(exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_DIR))

# OpenAI 임베딩 함수 정의
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)

def init_collection():
    """Chroma 컬렉션 초기화 또는 가져오기"""
    client = get_chroma_client()
    try:
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=openai_ef
        )
        logger.info(f"기존 컬렉션 '{COLLECTION_NAME}' 로드 완료")
    except Exception:
        collection = client.create_collection(
            name=COLLECTION_NAME,
            embedding_function=openai_ef
        )
        logger.info(f"새 컬렉션 '{COLLECTION_NAME}' 생성 완료")
    
    return collection

def add_prompt_to_collection(prompt_id: str, original_prompt: str, edited_prompt: str, 
                            diff_json: dict, intentions: List[str]):
    """프롬프트를 Chroma 컬렉션에 추가"""
    collection = init_collection()
    
    # 메타데이터 준비
    metadata = {
        "edited_prompt": edited_prompt,
        "diff_json": json.dumps(diff_json),
        "intentions": json.dumps(intentions)
    }
    
    # 컬렉션에 추가
    collection.add(
        ids=[prompt_id],
        documents=[original_prompt],
        metadatas=[metadata]
    )
    
    logger.info(f"프롬프트 '{prompt_id}' 컬렉션에 추가 완료")

def update_collection_from_json_files():
    """기존 JSON 파일들을 읽어서 Chroma 컬렉션 업데이트"""
    collection = init_collection()
    
    # 이미 저장된 ID 목록 가져오기
    existing_ids = set(collection.get()["ids"]) if collection.count() > 0 else set()
    
    # JSON 파일들 로드
    count = 0
    for file in DATA_DIR.glob("prompt_*.json"):
        try:
            prompt_id = file.stem  # prompt_XXXXX.json -> prompt_XXXXX
            
            # 이미 저장된 ID면 건너뛰기
            if prompt_id in existing_ids:
                continue
                
            with open(file, encoding="utf-8") as f:
                data = json.load(f)
                
            # 컬렉션에 추가
            add_prompt_to_collection(
                prompt_id=prompt_id,
                original_prompt=data["original"],
                edited_prompt=data["edited"],
                diff_json=data["diff_json"],
                intentions=data["intentions"]
            )
            count += 1
            
        except Exception as e:
            logger.error(f"파일 '{file}' 처리 중 오류 발생: {e}")
    
    logger.info(f"총 {count}개의 새 프롬프트를 컬렉션에 추가함")
    return count

def find_similar_prompt(query_text: str, similarity_threshold: float = 0.65) -> Optional[Tuple[str, str, dict, List[str], bool]]:
    """쿼리 텍스트와 가장 유사한 프롬프트 찾기"""
    collection = init_collection()
    
    # 컬렉션이 비어있으면 업데이트
    if collection.count() == 0:
        update_collection_from_json_files()
        # 업데이트 후에도 비어있으면 None 반환
        if collection.count() == 0:
            logger.warning("컬렉션이 비어있어 유사한 프롬프트를 찾을 수 없음")
            return None
    
    # 쿼리 실행
    results = collection.query(
        query_texts=[query_text],
        n_results=1,
        include=["documents", "metadatas", "distances"]
    )
    
    # 결과가 없으면 None 반환
    if not results["ids"] or not results["ids"][0]:
        logger.warning("유사한 프롬프트를 찾을 수 없음")
        return None
    
    # 유사도 점수 확인 (Chroma는 거리를 반환하므로 1-거리로 유사도 계산)
    distance = results["distances"][0][0]
    similarity = 1 - distance
    
    if similarity < similarity_threshold:
        logger.info(f"유사도({similarity:.4f})가 임계값({similarity_threshold})보다 낮음")
        return None
    
    # 결과 파싱
    original_prompt = results["documents"][0][0]
    metadata = results["metadatas"][0][0]
    edited_prompt = metadata["edited_prompt"]
    diff_json = json.loads(metadata["diff_json"])
    intentions = json.loads(metadata["intentions"])
    
    logger.info(f"유사한 프롬프트 찾음 (유사도: {similarity:.4f})")
    return (original_prompt, edited_prompt, diff_json, intentions, False) 