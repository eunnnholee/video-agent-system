import streamlit as st

from agent.graph.prompt_graph import graph_generate_prompt
from agent.graph.edit_graph import edit_agent_app
from agent.graph.save_graph import save_agent_app
from agent.graph.video_graph import video_agent_app

from agent.graph.history_guided_graph import history_guided_graph

import logging
from pathlib import Path
from datetime import datetime

# 현재 시간 기반 파일명 (예: 05-29_07_05_agent.log)
now = datetime.now().strftime("%m-%d_%H_%M")
log_filename = f"{now}_agent.log"

# 로그 디렉토리 설정
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# 전체 경로
LOG_FILE = LOG_DIR / log_filename

# logging 설정
logging.basicConfig(
    level=logging.DEBUG,  # 모든 로그 출력
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)


st.set_page_config(page_title="LangGraph 영상 생성 시스템", layout="centered")
st.title("🎬 LangGraph 단계별 영상 생성 에이전트")

# 세션 상태 초기화
if "state" not in st.session_state:
    st.session_state.state = {}

# 1. 사용자 입력
user_input = st.text_input("🎯 영상 콘셉트를 입력하세요")
if user_input:
    st.session_state.state["user_input"] = user_input

# 2. 저장 여부 체크박스
save_confirmed = st.checkbox("💾 프롬프트 및 수정 이력 저장", value=True)
st.session_state.state["save_confirmed"] = save_confirmed  # ✅ 오타 수정 반영

# 3. 프롬프트 생성
if st.button("✨ 프롬프트 생성"):
    try:
        result = graph_generate_prompt.invoke(st.session_state.state)
        st.session_state.state.update(result)
        st.success("✅ 프롬프트 생성 완료")
        st.code(result["original_prompt"], language="text")
    except Exception as e:
        st.error("프롬프트 생성 실패")
        st.exception(e)

# 4. 수정 입력
edited_prompt = st.text_area("✏️ 수정할 프롬프트 입력 (선택)", height=100)
if edited_prompt.strip():
    st.session_state.state["edited_prompt"] = edited_prompt.strip()

# 5. 수정 반영 및 diff
if st.button("🔍 수정 반영 및 차이 분석"):
    try:
        result = edit_agent_app.invoke(st.session_state.state)
        st.session_state.state.update(result)
        st.success("✅ 수정 반영 및 diff 완료")

        st.subheader("📌 최종 프롬프트")
        st.code(result["edited_prompt"], language="text")

        st.subheader("🧾 수정 차이")
        if result["diff"]:
            st.code("\n".join(result["diff"]), language="diff")
        else:
            st.info("수정된 내용이 없습니다.")
    except Exception as e:
        st.error("diff 처리 실패")
        st.exception(e)

# 6. 저장
if st.button("💾 프롬프트 저장"):
    try:
        result = save_agent_app.invoke(st.session_state.state)
        st.session_state.state.update(result)
        filename = result.get("saved_filename")
        st.success(f"✅ 저장 완료! ({filename})" if filename else "✅ 저장 완료")
    except Exception as e:
        st.error("저장 실패")
        st.exception(e)

# 7. 영상 생성
if st.button("🎥 영상 생성"):
    try:
        result = video_agent_app.invoke(st.session_state.state)
        st.session_state.state.update(result)
        st.success("✅ 영상 생성 완료")
        st.video(result["video_path"])
    except Exception as e:
        st.error("영상 생성 실패")
        st.exception(e)

# 8. 유사 프롬프트 기반 GPT 재생성
if st.button("📚 유사 이력 기반 프롬프트 재생성"):
    try:
        result = history_guided_graph.invoke(st.session_state.state)
        st.session_state.state.update(result)
        st.success("✅ GPT 기반 최적화 프롬프트 생성 완료")

        st.subheader("✨ 추천 프롬프트 (히스토리 기반)")
        st.code(result["history_guided_prompt"], language="text")
    except Exception as e:
        st.error("추천 프롬프트 생성 실패")
        st.exception(e)
