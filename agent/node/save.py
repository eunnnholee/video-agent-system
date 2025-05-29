from modules.history_manager import save_prompt_history
from modules.prompt_editor import get_diff
import logging
from agent.state import VideoAgentState

logger = logging.getLogger(__name__)

def save_prompt_node(state: VideoAgentState) -> VideoAgentState:
    original = state.get("original_prompt", "").strip()
    edited = state.get("edited_prompt", "").strip()

    # 저장 여부에 따라 final_prompt 설정
    if state.get("save_confirmed"):
        final = edited or original  # 수정한 프롬프트가 없으면 original 사용
        state["final_prompt"] = final

        # diff가 없거나 잘못된 경우 자동 생성
        if "diff" not in state or not isinstance(state["diff"], list) or not state["diff"]:
            diff = get_diff(original, final)
            state["diff"] = diff
            logger.debug("[Save Node] Diff auto-generated due to missing or invalid diff.")

        filename = save_prompt_history(
            original,
            final,
            state["diff"]
        )
        state["saved_filename"] = filename

        logger.info(f"[Save Node] Prompt history saved to {filename}")
        logger.debug(f"[Save Node] Original: {original}")
        logger.debug(f"[Save Node] Final: {final}")
        logger.debug(f"[Save Node] Diff: {state['diff']}")
    else:
        # 저장 거부 시에도 final_prompt는 original_prompt로 설정
        state["final_prompt"] = original
        state["saved_filename"] = None
        logger.info("[Save Node] Save not confirmed; skipping history save.")

    return state
