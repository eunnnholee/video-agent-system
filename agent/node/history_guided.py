from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from agent.state import VideoAgentState
from modules.recommender import get_most_similar_history
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def history_guided_prompt_node(state: VideoAgentState) -> VideoAgentState:
    user_input = state.get("user_input", "").strip()
    if not user_input:
        raise ValueError("user_input is required")

    logger.info(f"[History Node] Received user_input: {user_input}")

    history = get_most_similar_history(user_input)
    if not history:
        logger.warning("[History Node] No similar prompt history found.")
        raise ValueError("No similar prompt history found.")

    logger.info(f"[History Node] Found similar history ID: {history.get('id', 'unknown')}")
    logger.debug(f"[History Node] Matched Original: {history['original']}")
    logger.debug(f"[History Node] Matched Edited: {history['edited']}")

    template_path = Path("agent/templates/history_guided_prompt.jinja")
    template_str = template_path.read_text(encoding="utf-8")
    template = ChatPromptTemplate.from_template(template_str)

    messages = template.format_messages(
        previous_concept=history["original"],
        previous_edited=history["edited"],
        current_concept=user_input
    )

    llm = ChatOpenAI(model="gpt-4", temperature=0.5)
    response = llm.invoke(messages)
    prompt = response.content.strip()

    state["history_guided_prompt"] = prompt

    logger.info("[History Node] Generated history-guided prompt.")
    logger.debug(f"[History Node] Prompt Output: {prompt}")

    return state
