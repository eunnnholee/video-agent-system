from agent.state import VideoAgentState
from modules.history_manager import save_prompt_history

def save_history_node(state: VideoAgentState) -> VideoAgentState:
    """
    프롬프트 히스토리(JSON)를 저장하는 노드.
    state["save_confirmed"]가 True일 경우에만 저장 수행.
    """
    if state.get("save_confirmed"):
        filename = save_prompt_history(
            state.get("original_prompt", ""),
            state.get("edited_prompt", ""),
            state.get("diff", [])
        )
        print(f"프롬프트 히스토리 저장됨: {filename}")
    else:
        print("저장 생략됨 (save_confirmed=False)")

    return state
