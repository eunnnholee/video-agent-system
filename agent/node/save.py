from modules.history_manager import save_prompt_history
from modules.prompt_editor import get_diff
import logging
from agent.state import VideoAgentState

logger = logging.getLogger(__name__)

def save_prompt_node(state: VideoAgentState) -> VideoAgentState:
    if state.get("save_confirmed"):
        original = state.get("original_prompt", "").strip()
        edited = state.get("edited_prompt", "").strip() or original

        # diff가 없거나 잘못된 경우 자동 생성
        if "diff" not in state or not isinstance(state["diff"], list) or not state["diff"]:
            diff = get_diff(original, edited)
            state["diff"] = diff
            logger.debug("[Save Node] Diff auto-generated due to missing or invalid diff.")

        filename = save_prompt_history(
            original,
            edited,
            state["diff"]
        )
        state["saved_filename"] = filename

        logger.info(f"[Save Node] Prompt history saved to {filename}")
        logger.debug(f"[Save Node] Original: {original}")
        logger.debug(f"[Save Node] Edited: {edited}")
        logger.debug(f"[Save Node] Diff: {state['diff']}")
    else:
        logger.info("[Save Node] Save not confirmed; skipping history save.")
        state["saved_filename"] = None

    return state
