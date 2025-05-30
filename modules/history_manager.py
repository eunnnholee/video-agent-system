import json
import uuid
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def save_prompt_history(original: str, edited: str, diff_html: list[str]):
    """
    수정된 프롬프트 및 diff를 JSON 파일로 저장
    """
    timestamp = datetime.now().isoformat()
    unique_id = uuid.uuid4().hex[:8]

    history = {
        "id": unique_id,
        "timestamp": timestamp,
        "original": original,
        "edited": edited,
        "diff_html": diff_html
    }

    filename = DATA_DIR / f"prompt_{unique_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

    return filename.name  # 저장된 파일 이름 반환
