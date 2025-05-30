import spacy
import json
from sentence_transformers import SentenceTransformer, util
from difflib import SequenceMatcher
from transformers import pipeline

# 모델 로딩
nlp = spacy.load("en_core_web_sm")
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
emotion_classifier = pipeline(
    "text-classification",
    model="bhadresh-savani/distilbert-base-uncased-emotion",
    top_k=3,
)


# 감정 분포 추출
def get_top_emotions(text: str) -> list[str]:
    try:
        result = emotion_classifier(text)
        return [r["label"] for r in result[0]]
    except Exception:
        return ["neutral"]


# 구조 변화 감지용 문장 임베딩 유사도
def get_sim_score(text1, text2) -> float:
    try:
        emb1 = embedder.encode(text1, convert_to_tensor=True)
        emb2 = embedder.encode(text2, convert_to_tensor=True)
        return float(util.cos_sim(emb1, emb2)[0][0])
    except Exception:
        return 0.0


# 명사 추출 및 변경 감지
def extract_nouns(doc):
    return [token.text for token in doc if token.pos_ in {"NOUN", "PROPN"}]


def get_noun_diff(doc_orig, doc_edit):
    nouns_o = extract_nouns(doc_orig)
    nouns_e = extract_nouns(doc_edit)
    matcher = SequenceMatcher(None, nouns_o, nouns_e)
    diffs = []
    seen_pairs = set()  # 중복 필터링용 추가

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "replace":
            orig = " ".join(nouns_o[i1:i2])
            edit = " ".join(nouns_e[j1:j2])
            if (orig, edit) not in seen_pairs:  # 중복 체크
                seen_pairs.add((orig, edit))
                diffs.append({"original": orig, "edited": edit})
    return diffs


# token diff
def get_token_diff(orig_tokens, edit_tokens):
    matcher = SequenceMatcher(None, orig_tokens, edit_tokens)
    return [
        (tag, orig_tokens[i1:i2], edit_tokens[j1:j2])
        for tag, i1, i2, j1, j2 in matcher.get_opcodes()
    ]


# 전체 의미 기반 diff 분석
def classify_diff(original_text: str, edited_text: str) -> dict:
    doc_orig = nlp(original_text)
    doc_edit = nlp(edited_text)

    orig_tokens = [token.text for token in doc_orig]
    edit_tokens = [token.text for token in doc_edit]

    diff_json = {
        "noun_diff": [],
        "structure_change": [],
        "tone_change": [],
        "action_addition": [],
    }

    # 1. 명사 변화 탐지
    diff_json["noun_diff"] = get_noun_diff(doc_orig, doc_edit)

    # 2. 구조 변화 감지
    sim_score = get_sim_score(original_text, edited_text)
    if sim_score >= 0.85:
        diff_json["structure_change"].append(
            {
                "original": original_text,
                "edited": edited_text,
                "change": "sentence_rephrased",
            }
        )

    # 3. 감성 톤 변화 감지 (top emotion 변경)
    emotions_o = get_top_emotions(original_text)
    emotions_e = get_top_emotions(edited_text)

    if emotions_o and emotions_e and emotions_o[0] != emotions_e[0]:
        diff_json["tone_change"].append(
            {
                "original": f"{original_text} ({emotions_o[0]})",
                "edited": f"{edited_text} ({emotions_e[0]})",
                "change": f"{emotions_o[0]} → {emotions_e[0]}",
            }
        )

    # 4. 동작 추가 감지
    verbs_o = {t.lemma_ for t in doc_orig if t.pos_ == "VERB"}
    verbs_e = {t.lemma_ for t in doc_edit if t.pos_ == "VERB"}
    new_verbs = verbs_e - verbs_o

    for token in doc_edit:
        if token.lemma_ in new_verbs and token.pos_ == "VERB":
            phrase = " ".join([t.text for t in token.subtree])
            if len(phrase.split()) > 1:
                diff_json["action_addition"].append(
                    {"added": phrase, "context": edited_text}
                )
            new_verbs.discard(token.lemma_)

    return diff_json


# # 테스트
# if __name__ == "__main__":
#     orig = "A man in a dress"
#     edit = "A man in a T-shirt"

#     result = classify_diff(orig, edit)
#     print(json.dumps(result, indent=2, ensure_ascii=False))
