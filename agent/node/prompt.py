from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from agent.state import VideoAgentState
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()


def generate_prompt_node(state: VideoAgentState) -> VideoAgentState:
    user_input = state["user_input"]
    
    # 프롬프트 템플릿 로드
    TEMPLATE_PATH = Path("agent/templates/video_prompt.txt")
    template_str = TEMPLATE_PATH.read_text(encoding="utf-8")
    
    template = ChatPromptTemplate.from_template(template_str)
    messages = template.format_messages(concept=user_input)

    # OpenAI 모델 호출
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    response = llm.invoke(messages)
    generated_prompt = response.content.strip()

    # 상태에 저장 후 반환
    state["original_prompt"] = generated_prompt
    return state
