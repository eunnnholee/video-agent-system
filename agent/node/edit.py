from agent.state import VideoAgentState

def edit_prompt_node(state: VideoAgentState) -> VideoAgentState:
    """
    사용자에 의해 수정된 프롬프트를 처리하는 LangGraph 노드.
    - 수정이 없다면 original_prompt를 그대로 복사하여 edited_prompt에 저장한다.
    - 이미 edited_prompt가 있다면 그대로 유지한다.
    """

    if not state.get("edited_prompt"):
        state["edited_prompt"] = state["original_prompt"]

    return state
