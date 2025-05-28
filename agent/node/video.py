from agent.state import VideoAgentState
from modules.video_generator import generate_placeholder_video

def generate_video_node(state: VideoAgentState) -> VideoAgentState:
    """
    최종 프롬프트(edited_prompt)를 기반으로 mock 영상 생성.
    생성된 영상 경로는 state["video_path"]에 저장됨.
    """
    prompt = state.get("edited_prompt", "")
    output_path = "sample_videos/sample1.mp4"

    generate_placeholder_video(prompt, output_path=output_path)

    state["video_path"] = output_path
    print(f"영상 생성 완료: {output_path}")

    return state
