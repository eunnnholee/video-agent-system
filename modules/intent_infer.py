from typing import List, Dict

def infer_intent_from_diff(diff_json: Dict) -> List[str]:
    intentions = []

    if diff_json.get("noun_diff"):
        intentions.append("대상을 변경하고자 함")

    if diff_json.get("structure_change"):
        intentions.append("문장의 표현을 다듬고자 함")

    if diff_json.get("tone_change"):
        tone_change = diff_json["tone_change"][0]["change"]
        if "positive" in tone_change or "joy" in tone_change or "love" in tone_change:
            intentions.append("분위기를 더 밝게 만들고자 함")
        elif "negative" in tone_change or "anger" in tone_change or "sadness" in tone_change:
            intentions.append("분위기를 더 차분하거나 진지하게 만들고자 함")
        else:
            intentions.append("분위기를 변화시키고자 함")

    if diff_json.get("action_addition"):
        intentions.append("동작을 추가하여 생동감을 부여하고자 함")

    if not intentions:
        intentions.append("단순한 표현 수정 또는 문법 변경")

    return intentions

# # 테스트
# if __name__ == "__main__":
#     sample_diff = {
#         "noun_diff": [{"original": "dress", "edited": "T-shirt"}],
#         "structure_change": [],
#         "tone_change": [{"change": "neutral → joy"}],
#         "action_addition": []
#     }

#     result = infer_intent_from_diff(sample_diff)
#     print("추론된 편집 의도:", result)
