from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import logging

logger = logging.getLogger(__name__)

def generate_prompt_node(state: dict) -> dict:
    user_input = state.get("user_input", "").strip()
    if not user_input:
        raise ValueError("user_input is required")

    logger.info(f"[Prompt Node] Received user_input: {user_input}")

    # 템플릿 로드
    template_path = Path("agent/templates/video_prompt.jinja")
    template_str = template_path.read_text(encoding="utf-8")
    template = ChatPromptTemplate.from_template(template_str)

    messages = template.format_messages(concept=user_input)

    llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    response = llm.invoke(messages)
    generated_prompt = response.content.strip()

    logger.info("[Prompt Node] Generated cinematic prompt.")
    logger.debug(f"[Prompt Node] Prompt Output: {generated_prompt}")

    return {"original_prompt": generated_prompt}