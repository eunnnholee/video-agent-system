import json
import os
from pathlib import Path
from typing import Tuple, Optional, List
from openai import OpenAI
from dotenv import load_dotenv
import logging
from modules.vector_store import find_similar_prompt, update_collection_from_json_files

# 환경 변수 로드
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DATA_DIR = Path("data")

# 로깅 설정
logger = logging.getLogger(__name__)

def load_all_histories() -> List[dict]:
    """모든 프롬프트 히스토리 JSON 파일 로드"""
    histories = []
    for file in DATA_DIR.glob("prompt_*.json"):
        with open(file, encoding="utf-8") as f:
            try:
                histories.append(json.load(f))
            except json.JSONDecodeError:
                continue
    return histories

def get_latest_history(histories: List[dict]) -> Optional[dict]:
    """최신 프롬프트 히스토리 가져오기"""
    # 최신 timestamp 기준으로 정렬 후 가장 최근 항목 반환
    if not histories:
        return None
    sorted_histories = sorted(histories, key=lambda h: h.get("timestamp", ""), reverse=True)
    return sorted_histories[0]

def find_most_similar_prompt(user_input: str) -> Optional[Tuple[str, str, dict, List[str], bool]]:
    """사용자 입력과 가장 유사한 프롬프트 찾기 (Chroma DB 사용)"""
    user_input = user_input.strip()
    if not user_input:
        logger.warning("find_most_similar_prompt() - user_input 비어 있음")
        return None

    # Chroma DB에서(1) 유사한 프롬프트 검색
    similar_prompt = find_similar_prompt(user_input)
    if similar_prompt:
        logger.info("Chroma DB에서 유사한 프롬프트 찾음")
        return similar_prompt

    # (2) 유사한 프롬프트가 없으면 컬렉션 업데이트 시도
    logger.info("유사한 프롬프트가 없어 컬렉션 업데이트 시도")
    count = update_collection_from_json_files()
    
    if count > 0:
        # 업데이트 후 다시 검색
        similar_prompt = find_similar_prompt(user_input)
        if similar_prompt:
            logger.info(f"컬렉션 업데이트 후 유사한 프롬프트 찾음 (추가된 항목: {count}개)")
            return similar_prompt
    
    # (3) 그래도 없으면 최신 히스토리 반환 (fallback)
    logger.info("유사한 프롬프트를 찾지 못함, 최신 히스토리로 fallback")
    histories = load_all_histories()
    latest = get_latest_history(histories)
    
    if latest:
        logger.info("최신 히스토리 반환 (fallback)")
        return (
            latest["original"],
            latest["edited"],
            latest["diff_json"],
            latest["intentions"],
            True  # fallback 여부 표시
        )
    
    logger.warning("히스토리가 전혀 없음")
    return None

