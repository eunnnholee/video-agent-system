from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from agent.state import VideoAgentState
import logging

logger = logging.getLogger(__name__)

def optimize_prompt_node(state: VideoAgentState) -> VideoAgentState:
    logger.info("[Optimizer Node] optimize_prompt_node called")
    final_prompt = state.get("final_prompt", "").strip()
    if not final_prompt:
        raise ValueError("final_prompt is required")

    logger.info("[Optimizer Node] 최종 프롬프트 기반 이미지 프롬프트 최적화 시작")
    logger.debug(f"[Optimizer Node] 입력: {final_prompt}")

    messages = [
        SystemMessage(content=(
            "You are an expert prompt engineer for text-to-image AI. "
            "Always respond in English regardless of the input language."
        )),
        HumanMessage(content=(
            "Rewrite the following video description into a single-line visual prompt suitable for a text-to-image generation model.\n"
            "- Avoid markdown or bullet formatting\n"
            "- Use vivid, cinematic, natural language\n"
            "- Keep it under 300 characters\n\n"
            f"Video Description:\n{final_prompt}"
        ))
    ]


    llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    response = llm.invoke(messages)
    image_prompt = response.content.strip()

    logger.info("[Optimizer Node] 이미지 프롬프트 생성 완료")
    logger.debug(f"[Optimizer Node] 출력: {image_prompt}")

    return {
        "image_prompt": image_prompt
    }