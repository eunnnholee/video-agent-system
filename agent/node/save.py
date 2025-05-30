from modules.history_manager import save_prompt_history
from modules.prompt_editor import get_diff_html
from modules.semantic_diff import classify_diff
from modules.intent_infer import infer_intent_from_diff
from agent.state import VideoAgentState
import logging

logger = logging.getLogger(__name__)

def save_prompt_node(state: VideoAgentState) -> VideoAgentState:
    original = state.get("original_prompt", "").strip()
    edited = state.get("edited_prompt", "").strip()
    final = edited if edited else original
    state["final_prompt"] = final

    # 시각용 HTML diff
    if "diff_html" not in state or not isinstance(state["diff_html"], list) or not state["diff_html"]:
        state["diff_html"] = get_diff_html(original, final)
        logger.debug("[Save Node] Diff auto-generated due to missing or invalid diff_html.")

    # 의미 기반 diff + 편집 의도 추론
    diff_json = classify_diff(original, final)
    intentions = infer_intent_from_diff(diff_json)

    state["diff_json"] = diff_json
    state["intentions"] = intentions

    # 저장
    filename = save_prompt_history(
        original,
        final,
        diff_json,
        intentions
    )
    state["saved_filename"] = filename

    logger.info(f"[Save Node] Prompt history saved to {filename}")
    logger.debug(f"[Save Node] diff_json: {diff_json}")
    logger.debug(f"[Save Node] intentions: {intentions}")

    return state
