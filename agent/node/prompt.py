from pathlib import Path
from jinja2 import Template
from langchain_openai import ChatOpenAI
import logging
from modules.recommender import find_most_similar_prompt

logger = logging.getLogger(__name__)

def generate_prompt_node(state: dict) -> dict:
    logger.info("[Prompt Node] generate_prompt_node called")  # 호출 로그 추가
    user_input = state.get("user_input", "").strip()
    if not user_input:
        raise ValueError("user_input is required")

    # 이미 생성된 경우, 재생성하지 않고 그대로 반환
    # /start/에서 프롬프트가 이미 생성된 경우, 다시 생성하지 않도록 함
    if state.get("original_prompt"):
        logger.info("[Prompt Node] original_prompt already exists. Skipping generation.")
        return state    # 그대로 다음 단계로 넘어감

    logger.info(f"[Prompt Node] Received user_input: {user_input}")
    
    # 유사 프롬프트 검색
    similar_prompt_result = find_most_similar_prompt(user_input)
    
    # 1) Jinja2 템플릿 로드 & 렌더링
    template_path = Path("agent/templates/video_prompt.jinja")
    template_str = template_path.read_text(encoding="utf-8")
    logger.debug(f'####[template_str] {template_str}####')

    jinja = Template(template_str)
    
    # 유사 프롬프트가 있으면 템플릿에 포함
    if similar_prompt_result:
        original, edited, diff_json, intentions, _ = similar_prompt_result
        rendered = jinja.render(
            concept=user_input,
            has_similar_prompt=True,
            similar_original=original,
            similar_edited=edited,
            similar_intentions=intentions
        )
        logger.info("[Prompt Node] Found similar prompt. Including in template.")
    else:
        rendered = jinja.render(
            concept=user_input,
            has_similar_prompt=False
        )
        logger.info("[Prompt Node] No similar prompt found.")
    
    logger.debug(f"@@@@[Prompt Node] Rendered prompt]@@@@\n{rendered}")

    # 2) LLM 호출
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    response = llm.invoke([{"role": "user", "content": rendered}])
    generated_prompt = response.content.strip()

    logger.info("[Prompt Node] Generated cinematic prompt.")
    logger.debug(f"[Prompt Node] Prompt Output: {generated_prompt}")

    # 이전 대화 기억 저장
    memory_data = {
        "user_input": user_input,
        "generated_prompt": generated_prompt
    }
    
    # 메모리에 저장된 대화 기록이 있으면 업데이트
    if "chat_memory" in state:
        state["chat_memory"].append(memory_data)
    else:
        state["chat_memory"] = [memory_data]

    return {
        "original_prompt": generated_prompt,
        "chat_memory": state.get("chat_memory", [memory_data])
    }
