from pathlib import Path
import logging
from jinja2 import Template
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from modules.recommender import find_most_similar_prompt
from modules.question_generator import suggest_followup_questions

logger = logging.getLogger(__name__)

# 전역 설정
TEMPLATE_PATH = Path("agent/templates/history_guided_prompt.jinja")
LLM = ChatOpenAI(model="gpt-4", temperature=0.7, max_tokens=800)

def load_template(path: Path) -> Template:
    return Template(path.read_text(encoding="utf-8"))

JINJA_TEMPLATE = load_template(TEMPLATE_PATH)

def handle_empty_input() -> dict:
    return {"history_guided_prompt": "❗ 사용자 입력이 비어 있습니다."}

def handle_no_similar_prompt() -> dict:
    logger.warning("유사한 과거 프롬프트를 찾지 못했습니다.")
    fallback_intents = ["단순한 표현 수정 또는 문법 변경"]
    questions = suggest_followup_questions(fallback_intents)
    return {
        "history_guided_prompt": "\n".join([
            "❌ 유사한 과거 프롬프트가 없어 최적화된 추천이 어렵습니다.",
            "💡 아래와 같은 방식으로 프롬프트를 편집해보는 건 어떠세요?",
            *[f"- {q}" for q in questions]
        ])
    }

def render_prompt(original: str, edited: str, diff_json: dict, intentions: list, user_input: str) -> str:
    return JINJA_TEMPLATE.render(
        original=original,
        edited=edited,
        diff_json=diff_json,
        intentions=intentions,
        user_input=user_input
    )

def generate_history_guided_prompt(state: dict) -> dict:
    user_input = state.get("user_input", "").strip()
    if not user_input:
        return handle_empty_input()

    result = find_most_similar_prompt(user_input)
    if result is None:
        return handle_no_similar_prompt()

    original, edited, diff_json, intentions, _ = result

    rendered_prompt = render_prompt(original, edited, diff_json, intentions, user_input)
    logger.debug(f"🧾 Rendered prompt for LLM:\n{rendered_prompt}")

    response = LLM.invoke([{"role": "user", "content": rendered_prompt}])
    return {"history_guided_prompt": response.content}

