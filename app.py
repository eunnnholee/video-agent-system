import streamlit as st
from modules.prompt_generator import generate_prompt
from modules.prompt_editor import get_diff
from modules.history_manager import save_prompt_history
from modules.video_generator import generate_placeholder_video

st.title("🎬 영상 생성 에이전트 시스템")

# 1. 사용자 입력
user_input = st.text_input("1. 영상 콘셉트를 자연어로 입력하세요:")

# 2. 프롬프트 생성 버튼
if st.button("프롬프트 생성") and user_input:
    st.session_state.original_prompt = generate_prompt(user_input)
    st.success("✅ 프롬프트가 생성되었습니다.")

# 3. 프롬프트 수정 및 Diff 보기
if "original_prompt" in st.session_state:
    prompt = st.session_state.original_prompt

    edited_prompt = st.text_area("2. 프롬프트 수정", value=prompt)

    if st.button("Diff 보기"):
        diff_result = get_diff(prompt, edited_prompt)
        st.subheader("🧾 수정된 부분 (Diff):")
        st.code("\n".join(diff_result))

        # 추후 저장을 위해 세션에 저장해둠
        st.session_state.edited_prompt = edited_prompt
        st.session_state.diff = diff_result

    if st.button("프롬프트 저장"):
        if "diff" in st.session_state and "edited_prompt" in st.session_state:
            filename = save_prompt_history(prompt, st.session_state.edited_prompt, st.session_state.diff)
            st.success(f"💾 프롬프트가 {filename} 파일로 저장되었습니다.")
        else:
            st.error("⚠️ 먼저 'Diff 보기' 버튼을 클릭해주세요.")

# 4. 영상 생성 버튼
if "edited_prompt" in st.session_state and st.button("🎬 영상 생성"):
    generate_placeholder_video(st.session_state.edited_prompt)
    st.subheader("🎥 생성된 영상 (Mock)")
    st.video("sample_videos/sample1.mp4")
