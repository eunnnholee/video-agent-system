import streamlit as st
import requests
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="LangGraph 영상 생성 시스템", layout="wide")

with open("styles/main.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

API_URL = "http://localhost:8000/agent"

if "state" not in st.session_state:
    st.session_state.state = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("""
<div class="title-area">
    🎬 <span>LangGraph 영상 생성 에이전트</span>
</div>
""", unsafe_allow_html=True)

# 사용자 입력 박스
st.markdown("<div class='edit-section'>", unsafe_allow_html=True)
with st.form(key="user-input-form", clear_on_submit=True):
    user_input = st.text_input("입력창", label_visibility="collapsed", placeholder="예: 귀여운 강아지가 공원에서 뛰노는 장면")
    submitted = st.form_submit_button("➕ 프롬프트 추가")
    if submitted and user_input:
        st.session_state.state["user_input"] = user_input
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("LangBot이 생각 중..."):
            time.sleep(1.2)
            res = requests.post(f"{API_URL}/start", json={"user_input": user_input})
            res.raise_for_status()
            data = res.json()
            st.session_state.state.update(data)
            st.session_state.chat_history.append({"role": "bot", "content": data["original_prompt"]})
st.markdown("</div>", unsafe_allow_html=True)

# 대화 히스토리 출력
st.markdown('<div class="chat-box">', unsafe_allow_html=True)
for msg in st.session_state.chat_history:
    role = msg["role"]
    content = msg["content"]
    if role == "user":
        st.markdown(f"<div class='user-bubble'><span>🧑‍💻</span> {content}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-bubble typing-dots'><span>🤖</span> {content}</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 추천 프롬프트 블록
if "history_guided_prompt" in st.session_state.state:
    st.markdown("<div class='recommend-box'>", unsafe_allow_html=True)
    st.markdown("#### 🧠 LangBot의 추천 프롬프트")
    st.success(st.session_state.state["history_guided_prompt"])
    if st.button("✅ 추천 프롬프트 적용"):
        st.session_state.state["edited_prompt"] = st.session_state.state["history_guided_prompt"]
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# 수정 입력 및 Diff 박스
st.markdown("<div class='edit-section'>", unsafe_allow_html=True)
with st.form(key="diff-preview-form"):
    edited_prompt = st.text_area("✏️ 수정할 프롬프트 입력", height=120, placeholder="위 프롬프트를 수정해보세요...", key="edited_prompt_box")
    st.session_state.state["edited_prompt"] = edited_prompt.strip()
    diff_submitted = st.form_submit_button("➕ 프롬프트 수정")
st.markdown("</div>", unsafe_allow_html=True)

# Diff 결과 출력
if diff_submitted:
    try:
        req = {
            "original_prompt": st.session_state.state.get("original_prompt", ""),
            "edited_prompt": st.session_state.state.get("edited_prompt", "")
        }
        res = requests.post(f"{API_URL}/edit-preview", json=req)
        res.raise_for_status()
        preview = res.json()
        st.session_state.state.update(preview)
        if preview.get("diff_html"):
            st.markdown("<div class='edit-section'>", unsafe_allow_html=True)
            components.html(preview["diff_html"], height=180, scrolling=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("수정된 내용이 없습니다.")
    except Exception as e:
        st.error("❌ Diff 미리보기 실패")
        st.exception(e)

# 최종 반영 및 영상 생성
if st.button("📦 최종 반영 및 영상 생성"):
    try:
        req = {
            "user_input": st.session_state.state.get("user_input", ""),
            "original_prompt": st.session_state.state.get("original_prompt", ""),
            "edited_prompt": st.session_state.state.get("edited_prompt", "")
        }
        res = requests.post(f"{API_URL}/edit-confirm", json=req)
        res.raise_for_status()
        data = res.json()
        st.session_state.state.update(data)
        st.session_state.chat_history.append({"role": "bot", "content": "🎬 최종 프롬프트: " + data["final_prompt"]})
        st.video(data["video_path"])
    except Exception as e:
        st.error("처리 중 오류 발생")
        st.exception(e)

# 📚 유사 이력 기반 프롬프트 재생성
if st.button("📚 유사 이력 기반 프롬프트 재생성"):
    try:
        existing_video = st.session_state.state.get("video_path")
        existing_final = st.session_state.state.get("final_prompt")

        res = requests.post(f"{API_URL}/history-recommend", json={
            "user_input": st.session_state.state.get("user_input", "")
        })
        res.raise_for_status()
        result = res.json()

        st.session_state.state["history_guided_prompt"] = result.get("history_guided_prompt")
        st.session_state.state["followup_questions"] = result.get("followup_questions", [])

        # 복구는 여기서
        if existing_video:
            st.session_state.state["video_path"] = existing_video
        if existing_final:
            st.session_state.state["final_prompt"] = existing_final

        st.session_state.chat_history.append({
            "role": "bot",
            "content": "🧠 LangBot 추천: " + result["history_guided_prompt"]
        })

    except Exception as e:
        st.error("추천 프롬프트 생성 실패")
        st.exception(e)

# ✅ 추천 프롬프트 UI 출력
if "history_guided_prompt" in st.session_state.state:
    st.markdown("<div class='recommend-box'>", unsafe_allow_html=True)
    st.markdown("#### 🧠 LangBot의 추천 프롬프트")
    st.success(st.session_state.state["history_guided_prompt"])
    if st.button("✅ 추천 프롬프트 적용"):
        st.session_state.state["edited_prompt"] = st.session_state.state["history_guided_prompt"]
        st.experimental_rerun()

    followup_qs = st.session_state.state.get("followup_questions", [])
    if followup_qs:
        st.markdown("#### 💡 프롬프트 개선을 위한 질문 제안")
        for q in followup_qs:
            st.markdown(f"<div class='question'>👉 {q}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ✅ 영상 출력은 항상 아래에 고정
if "video_path" in st.session_state.state and "final_prompt" in st.session_state.state:
    st.markdown("#### 🎬 생성된 영상")
    st.video(st.session_state.state["video_path"])
    st.success("📝 최종 프롬프트: " + st.session_state.state["final_prompt"])