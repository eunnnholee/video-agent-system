import streamlit as st
import requests

API_URL = "http://localhost:8000/agent"

st.set_page_config(page_title="LangGraph 영상 생성 시스템", layout="centered")
st.title("🎬 LangGraph 단계별 영상 생성 에이전트")

if "state" not in st.session_state:
    st.session_state.state = {}

# 1. 사용자 입력
user_input = st.text_input("🎯 영상 콘셉트를 입력하세요")
if user_input:
    st.session_state.state["user_input"] = user_input

# 2. 저장 여부 체크
save_confirmed = st.checkbox("💾 프롬프트 및 수정 이력 저장", value=True)
st.session_state.state["save_confirmed"] = save_confirmed

# 3. 프롬프트 생성 (API 호출)
if st.button("✨ 프롬프트 생성"):
    try:
        res = requests.post(f"{API_URL}/start", json={"user_input": user_input})
        res.raise_for_status()
        data = res.json()
        st.session_state.state.update(data)
        st.success("✅ 프롬프트 생성 완료")
        st.code(data["original_prompt"])
    except Exception as e:
        st.error("프롬프트 생성 실패")
        st.exception(e)

# 4. 수정 입력
edited_prompt = st.text_area("✏️ 수정할 프롬프트 입력 (선택)", height=100)
if edited_prompt.strip():
    st.session_state.state["edited_prompt"] = edited_prompt.strip()

# 5. 수정 반영 + 저장 + 영상 생성
if st.button("📦 최종 반영 및 영상 생성"):
    try:
        req = {
            "original_prompt": st.session_state.state.get("original_prompt", ""),
            "edited_prompt": st.session_state.state.get("edited_prompt", ""),
            "save_confirmed": st.session_state.state.get("save_confirmed", True),
        }
        res = requests.post(f"{API_URL}/edit-confirm", json=req)
        res.raise_for_status()
        data = res.json()
        st.session_state.state.update(data)

        # 결과 출력
        st.subheader("📌 최종 프롬프트")
        st.code(data["edited_prompt"])
        st.subheader("🧾 수정 차이")
        if data.get("diff"):
            st.code("\n".join(data["diff"]), language="diff")
        else:
            st.info("수정된 내용이 없습니다.")
        st.success("✅ 저장 및 영상 생성 완료")
        st.video(data["video_path"])
    except Exception as e:
        st.error("처리 중 오류 발생")
        st.exception(e)

# 6. 유사 프롬프트 기반 GPT 재생성 (FastAPI 경유)
if st.button("📚 유사 이력 기반 프롬프트 재생성"):
    try:
        res = requests.post(f"{API_URL}/history-recommend", json={"user_input": user_input})
        res.raise_for_status()
        result = res.json()
        st.session_state.state.update(result)
        st.success("✅ GPT 기반 최적화 프롬프트 생성 완료")
        st.code(result["history_guided_prompt"], language="text")
    except Exception as e:
        st.error("추천 프롬프트 생성 실패")
        st.exception(e)
