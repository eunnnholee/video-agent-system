import json
import os
from pathlib import Path
from typing import Tuple, Optional, List
from openai import OpenAI
from dotenv import load_dotenv
import numpy as np

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DATA_DIR = Path("data")


def load_all_histories() -> List[dict]:
    histories = []
    for file in DATA_DIR.glob("prompt_*.json"):
        with open(file, encoding="utf-8") as f:
            try:
                histories.append(json.load(f))
            except json.JSONDecodeError:
                continue
    return histories


def get_latest_history(histories: List[dict]) -> Optional[dict]:
    # 최신 timestamp 기준으로 정렬 후 가장 최근 항목 반환
    if not histories:
        return None
    sorted_histories = sorted(histories, key=lambda h: h.get("timestamp", ""), reverse=True)
    return sorted_histories[0]


def get_openai_embedding(text: str) -> List[float]:
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("get_openai_embedding() - 입력이 비어 있음")

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=cleaned
    )
    return response.data[0].embedding


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    a = np.array(vec1)
    b = np.array(vec2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def find_most_similar_prompt(user_input: str) -> Optional[Tuple[str, str, dict, List[str], bool]]:
    user_input = user_input.strip()
    if not user_input:
        print("find_most_similar_prompt() - user_input 비어 있음")
        return None

    histories = load_all_histories()
    if not histories:
        print("find_most_similar_prompt() - 히스토리 없음")
        return None

    user_emb = get_openai_embedding(user_input)

    best_score = 0.0
    best_result = None

    for h in histories:
        try:
            orig_emb = get_openai_embedding(h["original"])
            score = cosine_similarity(user_emb, orig_emb)
            if score > best_score:
                best_score = score
                best_result = (
                    h["original"],
                    h["edited"],
                    h["diff_json"],
                    h["intentions"],
                    False  # fallback 아님
                )
        except Exception as e:
            print(f"[Error comparing with history]: {e}")
            continue

    if best_score >= 0.65 and best_result:
        return best_result
    else:
        latest = get_latest_history(histories)
        if latest:
            print(f"[유사도 낮음] (best_score={best_score:.4f}). 최신 기록으로 fallback.")
            return (
                latest["original"],
                latest["edited"],
                latest["diff_json"],
                latest["intentions"],
                True  # fallback 여부 표시
            )
        return None

