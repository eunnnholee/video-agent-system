from agent.state import VideoAgentState
from modules.runway_api import generate_video_from_image
from modules.runway_api import generate_image_from_text
import logging

logger = logging.getLogger(__name__)

def generate_video_node(state: VideoAgentState) -> VideoAgentState:
    image_prompt = state.get("image_prompt", "").strip()
    final_prompt = state.get("final_prompt", "").strip()

    if not image_prompt:
        raise ValueError("image_prompt is missing")
    if not final_prompt:
        raise ValueError("final_prompt is missing")

    logger.info("[Video Node] Runway 영상 생성 시작")
    logger.debug(f"[Video Node] 이미지 프롬프트: {image_prompt}")
    logger.debug(f"[Video Node] 영상 프롬프트: {final_prompt}")

    # 1) 이미지 생성
    image_url = generate_image_from_text(image_prompt)
    logger.info(f"[Video Node] 이미지 생성 완료: {image_url}")

    # 2) 영상 생성
    video_url = generate_video_from_image(image_url, prompt=final_prompt)
    logger.info(f"[Video Node] 영상 생성 완료: {video_url}")

    # 3) 상태에 저장
    state["video_path"] = video_url
    return state
