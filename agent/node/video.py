from agent.state import VideoAgentState
from modules.video_generator import generate_placeholder_video
from agent.state import VideoAgentState

def generate_video_node(state: VideoAgentState) -> VideoAgentState:
    """
    edited_prompt를 사용해 영상 파일을 생성하고 경로를 state에 저장하는 노드
    """
    prompt = state.get("edited_prompt", "").strip()
    output_path = "sample_videos/sample1.mp4"

    if not prompt:
        raise ValueError("edited_prompt is missing")

    generate_placeholder_video(prompt, output_path=output_path)
    state["video_path"] = output_path

    return state
