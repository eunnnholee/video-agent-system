import json
import uuid
from datetime import datetime
from pathlib import Path
import logging
from modules.vector_store import add_prompt_to_collection

logger = logging.getLogger(__name__)
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def save_prompt_history(original: str, edited: str, diff_json: dict, intentions: list[str]) -> str:
    """
    의미 기반 Diff와 편집 의도를 포함한 프롬프트 히스토리를 저장합니다.
    JSON 파일과 Chroma DB에 모두 저장합니다.
    """
    timestamp = datetime.now().isoformat()
    unique_id = uuid.uuid4().hex[:8]
    prompt_id = f"prompt_{unique_id}"

    history = {
        "id": unique_id,
        "timestamp": timestamp,
        "original": original,
        "edited": edited,
        "diff_json": diff_json,
        "intentions": intentions
    }

    # JSON 파일로 저장
    filename = DATA_DIR / f"{prompt_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    
    # Chroma DB에도 저장
    try:
        add_prompt_to_collection(
            prompt_id=prompt_id,
            original_prompt=original,
            edited_prompt=edited,
            diff_json=diff_json,
            intentions=intentions
        )
        logger.info(f"프롬프트 '{prompt_id}'를 Chroma DB에 저장 완료")
    except Exception as e:
        logger.error(f"Chroma DB 저장 중 오류 발생: {e}")

    return filename.name  # 저장된 파일 이름 반환
