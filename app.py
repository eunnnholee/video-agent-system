import streamlit as st
import requests
import streamlit.components.v1 as components
import streamlit as st

st.set_page_config(page_title="LangGraph 영상 생성 시스템", layout="wide")

with open("styles/main.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

API_URL = "http://localhost:8000/agent"

if "state" not in st.session_state:
    st.session_state.state = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("LangGraph 영상 생성 에이전트")

# 입력 섹션
with st.container():
    st.subheader("1. 자연어 프롬프트 입력")
    with st.form(key="user-input-form", clear_on_submit=True):
        user_input = st.text_input(
            "원하는 영상의 느낌을 입력하세요",
            placeholder="예: 귀여운 강아지가 공원에서 뛰노는 장면",
        )
        submitted = st.form_submit_button("프롬프트 생성")
        if submitted and user_input:
            st.session_state.state["user_input"] = user_input
            with st.spinner("프롬프트 생성 중..."):
                res = requests.post(f"{API_URL}/start", json={"user_input": user_input})
                res.raise_for_status()
                data = res.json()
                st.session_state.state.update(data)
                st.session_state.chat_history.append(
                    {"role": "user", "content": user_input}
                )
                st.session_state.chat_history.append(
                    {"role": "bot", "content": data["original_prompt"]}
                )
    if "original_prompt" in st.session_state.state:
        st.text_area(
            "생성된 프롬프트",
            value=st.session_state.state["original_prompt"],
            height=100,
        )

# 수정 및 diff 섹션
with st.container():
    st.subheader("2. 프롬프트 수정")
    with st.form(key="diff-preview-form"):
        edited_prompt = st.text_area(
            "수정할 프롬프트", height=150, placeholder="위 프롬프트를 수정해보세요..."
        )
        st.session_state.state["edited_prompt"] = edited_prompt.strip()
        diff_submitted = st.form_submit_button("수정 내용 확인")

    if diff_submitted:
        try:
            req = {
                "original_prompt": st.session_state.state.get("original_prompt", ""),
                "edited_prompt": st.session_state.state.get("edited_prompt", ""),
            }
            res = requests.post(f"{API_URL}/edit-preview", json=req)
            res.raise_for_status()
            preview = res.json()
            st.session_state.state.update(preview)
            if preview.get("diff_html"):
                components.html(preview["diff_html"], height=200, scrolling=True)
            else:
                st.info("수정된 내용이 없습니다.")
        except Exception as e:
            st.error("Diff 미리보기 실패")
            st.exception(e)

# 영상 생성 섹션
with st.container():
    st.subheader("3. 영상 생성")
    if st.button("최종 반영 및 영상 생성"):
        with st.spinner("🎬 영상 생성 중... 잠시만 기다려 주세요."):
            try:
                req = {
                    "user_input": st.session_state.state.get("user_input", ""),
                    "original_prompt": st.session_state.state.get("original_prompt", ""),
                    "edited_prompt": st.session_state.state.get("edited_prompt", ""),
                }
                res = requests.post(f"{API_URL}/edit-confirm", json=req)
                res.raise_for_status()
                data = res.json()
                st.session_state.state.update(data)
                st.session_state.chat_history.append(
                    {"role": "bot", "content": "최종 프롬프트: " + data["final_prompt"]}
                )
            except Exception as e:
                st.error("영상 생성 실패")
                st.exception(e)

    if (
        "video_path" in st.session_state.state
        and "final_prompt" in st.session_state.state
    ):
        video_url = st.session_state.state["video_path"]
        video_html = f"""
        <video width="640" height="360" controls>
            <source src="{video_url}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
        """
        st.markdown(video_html, unsafe_allow_html=True)

# 추천 프롬프트 및 질문 섹션
with st.container():
    st.subheader("4. 추천 프롬프트 및 편집 제안")
    if st.button("유사 이력 기반 프롬프트 재생성"):
        try:
            res = requests.post(
                f"{API_URL}/history-recommend",
                json={"user_input": st.session_state.state.get("user_input", "")},
            )
            res.raise_for_status()
            result = res.json()
            st.session_state.state["history_guided_prompt"] = result.get(
                "history_guided_prompt"
            )
            st.session_state.state["followup_questions"] = result.get(
                "followup_questions", []
            )
        except Exception as e:
            st.error("추천 프롬프트 생성 실패")
            st.exception(e)

    if "history_guided_prompt" in st.session_state.state:
        st.text_area(
            "추천 프롬프트",
            value=st.session_state.state["history_guided_prompt"],
            height=300,
        )

        followup_qs = st.session_state.state.get("followup_questions", [])
        if followup_qs:
            st.markdown("#### 편집 제안 질문")
            for q in followup_qs:
                st.markdown(f"- {q}")

# 대화 히스토리
with st.expander("대화 히스토리 보기"):
    for msg in st.session_state.chat_history:
        role = msg["role"]
        content = msg["content"]

        if role == "user":
            st.markdown(f"🧑 **사용자:** {content}")
        elif role == "bot":
            if content.startswith("최종 프롬프트:"):
                final_text = content.replace("최종 프롬프트:", "").strip()
                st.markdown(f"🤖 **수정된 프롬프트:** {final_text}")
            else:
                st.markdown(f"🤖 **생성 프롬프트:** {content}")
