def generate_prompt(user_input: str) -> str:
    # 템플릿 방식 (추후 LLM 기반으로 확장 가능)
    return f"A bright video of {user_input}"
