# from agent.state import VideoAgentState
# from modules.video_generator import generate_placeholder_video
# from agent.state import VideoAgentState

# def generate_video_node(state: VideoAgentState) -> VideoAgentState:
#     """
#     edited_prompt를 사용해 영상 파일을 생성하고 경로를 state에 저장하는 노드
#     """
#     prompt = state.get("edited_prompt", "").strip()
#     output_path = "sample_videos/sample1.mp4"

#     if not prompt:
#         raise ValueError("edited_prompt is missing")

#     generate_placeholder_video(prompt, output_path=output_path)
#     state["video_path"] = output_path

#     return state


from agent.state import VideoAgentState
from modules.runway_api import generate_video_from_text
from modules.prompt_optimizer import optimize_prompt_with_gpt

def generate_video_node(state: VideoAgentState) -> VideoAgentState:
    """
    텍스트 기반 영상 생성을 위해 프롬프트를 최적화한 후
    Runway API를 호출하여 생성된 영상 URL을 state에 저장합니다.
    """
    original_prompt = state.get("edited_prompt", "").strip()
    if not original_prompt:
        raise ValueError("edited_prompt is missing")

    # 프롬프트 최적화 (한 줄짜리 시각 중심 표현)
    optimized_prompt = optimize_prompt_with_gpt(original_prompt)
    state["optimized_prompt"] = optimized_prompt  # 기록용

    # 영상 생성
    video_url = generate_video_from_text(optimized_prompt, num_frames=250)
    state["video_path"] = video_url

    return state

