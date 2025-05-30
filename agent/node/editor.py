from modules.prompt_editor import get_diff_html
from agent.state import VideoAgentState
import logging

logger = logging.getLogger(__name__)

def edit_prompt_node(state: VideoAgentState) -> VideoAgentState:
    original = state.get("original_prompt", "").strip()
    edited = state.get("edited_prompt", "").strip()

    if not original:
        raise ValueError("original_prompt is missing")

    logger.debug(f"[Edit Node] original: {original}")
    logger.debug(f"[Edit Node] edited: {edited}")

    diff_html = get_diff_html(original, edited)
    logger.debug(f"[Edit Node] diff_html: {diff_html}")

    # 수정이 실제로 이루어졌는지 판단
    final_prompt = edited if edited and edited != original else original

    return {
        "diff_html": diff_html,
        "final_prompt": final_prompt,
        "edited_prompt": edited
    }