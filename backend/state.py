from typing import TypedDict, Optional

class AgentState(TypedDict):
    user_input: str
    original_prompt: Optional[str]
    edited_prompt: Optional[str]
    diff: Optional[list[str]]
    video_path: Optional[str]
    save_confirmed: Optional[bool]
    history_guided_prompt: Optional[str]