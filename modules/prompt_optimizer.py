# modules/prompt_optimizer.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def optimize_prompt_with_gpt(edited_prompt: str) -> str:
    """
    영상 생성용 프롬프트를 텍스트-투-이미지 모델에 적합하도록
    시각적이고 간결한 단일 문장으로 최적화합니다.

    Args:
        edited_prompt (str): 사용자가 수정한 상세 영상 프롬프트

    Returns:
        str: Runway의 gen4_image 모델에 입력 가능한 최적화 프롬프트
    """

    try:
        template = ChatPromptTemplate.from_messages([
            ("system", "You are an expert prompt engineer for text-to-image AI."),
            ("user", (
                "Rewrite the following video description into a single-line visual prompt suitable for a text-to-image generation model.\n"
                "- Avoid markdown or bullet formatting\n"
                "- Use vivid, cinematic, natural language\n"
                "- Keep it under 300 characters\n\n"
                "Video Description:\n{prompt}"
            ))
        ])
        prompt = template.format_messages(prompt=edited_prompt)
        llm = ChatOpenAI(model="gpt-4", temperature=0.5)
        response = llm.invoke(prompt)
        return response.content.strip()

    except Exception as e:
        print("[❌ GPT 최적화 실패]", e)
        raise e