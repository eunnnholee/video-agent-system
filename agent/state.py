from typing import TypedDict, Optional

class VideoAgentState(TypedDict):
    user_input: str                               # 사용자가 입력한 자연어
    original_prompt: Optional[str]                # GPT가 생성한 시네마틱 영상 프롬프트
    edited_prompt: Optional[str]                  # 사용자가 수정한 프롬프트 (UI에서)
    diff: Optional[list[str]]                     # original_prompt와 edited_prompt 간 차이
    image_prompt: Optional[str]                   # 이미지 생성을 위한 시각적 최적화 프롬프트 (= optimized_prompt)
    final_prompt: Optional[str]                   # 영상 생성에 실제 사용된 프롬프트 (edited or original)
    video_path: Optional[str]                     # 생성된 영상 URL or 파일 경로
    save_confirmed: Optional[bool]                # 수정 내용을 저장할지 여부
    saved_filename: Optional[str]                 # 프롬프트 저장 파일 이름
    history_guided_prompt: Optional[str]          # 과거 이력 기반 GPT 재추천 프롬프트
