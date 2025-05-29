from pathlib import Path
from jinja2 import Template
from langchain_openai import ChatOpenAI
import logging

logger = logging.getLogger(__name__)

def generate_prompt_node(state: dict) -> dict:
    logger.info("[Prompt Node] generate_prompt_node called")  # 호출 로그 추가
    user_input = state.get("user_input", "").strip()
    if not user_input:
        raise ValueError("user_input is required")

    # 이이미 생성된 경우, 재생성하지 않고 그대로 반환
    if state.get("original_prompt"):
        logger.info("[Prompt Node] original_prompt already exists. Skipping generation.")
        return state    # 그대로 다음 단계로 넘어감

    logger.info(f"[Prompt Node] Received user_input: {user_input}")

    # 1) Jinja2 템플릿 로드 & 렌더링
    template_path = Path("agent/templates/video_prompt.jinja")
    template_str = template_path.read_text(encoding="utf-8")
    logger.debug(f'####[template_str] {template_str}####')

    jinja = Template(template_str)
    rendered = jinja.render(concept=user_input)
    logger.debug(f"@@@@[Prompt Node] Rendered prompt]@@@@\n{rendered}")

    # 2) LLM 호출
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    response = llm.invoke([{"role": "user", "content": rendered}])
    generated_prompt = response.content.strip()

    logger.info("[Prompt Node] Generated cinematic prompt.")
    logger.debug(f"[Prompt Node] Prompt Output: {generated_prompt}")

    return {"original_prompt": generated_prompt}
