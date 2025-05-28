from modules.prompt_editor import get_diff 
from agent.state import VideoAgentState
import logging

logger = logging.getLogger(__name__)


def edit_prompt_node(state: VideoAgentState) -> VideoAgentState:
    """
    사용자가 수정한 프롬프트와 원본 프롬프트를 비교하고,
    수정된 프롬프트와 diff 결과를 state에 저장한다.
    """
    original = state.get("original_prompt", "").strip()
    edited = state.get("edited_prompt", "").strip()

    if not original:
        raise ValueError("original_prompt is required")

    # 수정본이 없으면 원본 그대로 사용
    if not edited:
        edited = original

    diff = get_diff(original, edited)

    state["edited_prompt"] = edited
    state["diff"] = diff

    logger.info("[Edit Node] Prompt comparison completed.")
    logger.debug(f"[Edit Node] Original Prompt: {original}")
    logger.debug(f"[Edit Node] Edited Prompt: {edited}")
    logger.debug(f"[Edit Node] Diff Result: {diff}")

    return state
