from agent.state import VideoAgentState
from modules.prompt_editor import get_diff

def compare_diff_node(state: VideoAgentState) -> VideoAgentState:
    """
    수정 전/후 프롬프트의 차이를 계산하여 state["diff"]에 저장하는 노드.
    Diff 결과는 리스트 형식이며, difflib.unified_diff 기반.
    """
    original = state.get("original_prompt", "")
    edited = state.get("edited_prompt", "")

    diff_result = get_diff(original, edited)
    state["diff"] = diff_result

    return state
