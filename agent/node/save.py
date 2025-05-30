from modules.history_manager import save_prompt_history
from modules.prompt_editor import get_diff_html
import logging
from agent.state import VideoAgentState

logger = logging.getLogger(__name__)

def save_prompt_node(state: VideoAgentState) -> VideoAgentState:
    original = state.get("original_prompt", "").strip()
    edited = state.get("edited_prompt", "").strip()
    final = edited if edited else original

    state["final_prompt"] = final

    # diff 생성 또는 검증
    if "diff_html" not in state or not isinstance(state["diff_html"], list) or not state["diff_html"]:
        diff_html = get_diff_html(original, final)
        state["diff_html"] = diff_html
        logger.debug("[Save Node] Diff auto-generated due to missing or invalid diff.")

    # 무조건 저장
    filename = save_prompt_history(
        original,
        final,
        state["diff_html"]
    )
    state["saved_filename"] = filename

    logger.info(f"[Save Node] Prompt history saved to {filename}")
    logger.debug(f"[Save Node] Original: {original}")
    logger.debug(f"[Save Node] Final: {final}")
    logger.debug(f"[Save Node] diff_html: {state['diff_html']}")

    return state

