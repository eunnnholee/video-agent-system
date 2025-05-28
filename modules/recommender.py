# modules/recommender.py
import json
from pathlib import Path

def load_all_histories():
    files = Path("data").glob("prompt_*.json")
    histories = []
    for file in files:
        with open(file, encoding="utf-8") as f:
            histories.append(json.load(f))
    return histories

def jaccard_similarity(a: str, b: str) -> float:
    a_set, b_set = set(a.lower().split()), set(b.lower().split())
    return len(a_set & b_set) / len(a_set | b_set) if a_set | b_set else 0.0

def get_most_similar_history(user_input: str) -> dict | None:
    histories = load_all_histories()
    best_score, best = 0.0, None
    for h in histories:
        score = jaccard_similarity(user_input, h["original"])
        if score > best_score:
            best_score = score
            best = h
    return best
