from typeing import TypeDict, Optionl

class VideoAgentState(TypeDict):
    question: str
    original_prompt: Optionl[str]
    edited_prompt: Optionl[str]
    diff: Optionl[list[str]]
    video_path: Optionl[str]
    save_comfirmed: Optionl[bool]