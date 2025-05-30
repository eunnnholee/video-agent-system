from typing import List

INTENT_QUESTION_MAP = {
    "대상을 변경하고자 함": "대상의 특징(색상, 소재 등)을 더 구체화해 볼까요?",
    "문장의 표현을 다듬고자 함": "문장을 더 간결하거나 자연스럽게 표현해볼까요?",
    "분위기를 더 밝게 만들고자 함": "더 따뜻하거나 활기찬 분위기로 바꿔볼까요?",
    "분위기를 더 차분하거나 진지하게 만들고자 함": "더 어두운 감성이나 현실적인 분위기로 조정해볼까요?",
    "분위기를 변화시키고자 함": "어떤 감정 톤을 원하시나요? (예: 몽환적, 차분한)",
    "동작을 추가하여 생동감을 부여하고자 함": "인물이나 사물의 동작을 더 추가해볼까요? (예: 걷기, 뛰기 등)",
    "단순한 표현 수정 또는 문법 변경": "문법 외에도 스타일이나 감정 톤을 조정해볼까요?"
}

def suggest_followup_questions(intentions: List[str]) -> List[str]:
    questions = []
    for intent in intentions:
        question = INTENT_QUESTION_MAP.get(intent)
        if question:
            questions.append(question)
    return questions

# # 테스트
# if __name__ == "__main__":
#     sample_intents = [
#         "대상을 변경하고자 함",
#         "분위기를 더 밝게 만들고자 함"
#     ]
#     result = suggest_followup_questions(sample_intents)
#     print("추천 질문:")
#     for q in result:
#         print("-", q)
