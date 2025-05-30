import json
import uuid
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def save_prompt_history(original: str, edited: str, diff_json: dict, intentions: list[str]) -> str:
    """
    의미 기반 Diff와 편집 의도를 포함한 프롬프트 히스토리를 저장합니다.
    diff_html은 저장하지 않습니다.
    """
    timestamp = datetime.now().isoformat()
    unique_id = uuid.uuid4().hex[:8]

    history = {
        "id": unique_id,
        "timestamp": timestamp,
        "original": original,
        "edited": edited,
        "diff_json": diff_json,
        "intentions": intentions
    }

    filename = DATA_DIR / f"prompt_{unique_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

    return filename.name  # 저장된 파일 이름 반환
