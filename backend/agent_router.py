from fastapi import APIRouter
from pydantic import BaseModel
import asyncio
import time
import uuid

# LangGraph 통합 워크플로우
from agent.graph.video_agent_graph import video_agent_app, memory_saver
from agent.graph.prompt_graph import graph_generate_prompt, memory_saver as prompt_memory_saver
from agent.graph.history_guided_graph import history_guided_graph, memory_saver as history_memory_saver

router = APIRouter()

# 세션 ID 저장을 위한 딕셔너리
user_sessions = {}


# --- Pydantic 요청 모델 ---
class UserInputRequest(BaseModel):
    user_input: str
    session_id: str = None


class EditConfirmRequest(BaseModel):
    user_input: str
    original_prompt: str
    edited_prompt: str
    session_id: str = None


class HistoryRequest(BaseModel):
    user_input: str
    session_id: str = None


class EditPreviewRequest(BaseModel):
    original_prompt: str
    edited_prompt: str
    session_id: str = None


# --- 1. 최초 프롬프트 생성 ---
@router.post("/start")
async def start_prompt_generation(req: UserInputRequest):
    # 세션 ID 생성 또는 재사용
    session_id = req.session_id or str(uuid.uuid4())
    user_sessions[session_id] = True
    
    def run_prompt():
        state = {"user_input": req.user_input}
        
        # 이전 체크포인트가 있으면 불러오기
        try:
            thread_id = prompt_memory_saver.list_threads().get(session_id)
            if thread_id:
                config = {"configurable": {"thread_id": thread_id}}
                return graph_generate_prompt.invoke(state, config=config)
        except Exception as e:
            print(f"체크포인트 불러오기 실패: {e}")
        
        # 새 체크포인트 생성
        config = {"configurable": {"thread_id": session_id}}
        return graph_generate_prompt.invoke(state, config=config)  # 따로 프롬프트에 주입할 필요X -> config로 넣어주면 됨됨

    result = await asyncio.to_thread(run_prompt)
    result["session_id"] = session_id
    return result


# --- 2. 수정된 프롬프트 기반 영상 생성 + 기록 ---
@router.post("/edit-confirm")
async def edit_and_save(req: EditConfirmRequest):
    start = time.time()
    session_id = req.session_id or str(uuid.uuid4())

    def run_agents():
        state = {
            "user_input": req.user_input,
            "original_prompt": req.original_prompt,
            "edited_prompt": req.edited_prompt,
        }

        # 이전 체크포인트가 있으면 불러오기
        try:
            thread_id = memory_saver.list_threads().get(session_id)
            if thread_id:
                config = {"configurable": {"thread_id": thread_id}}
                return video_agent_app.invoke(state, config=config)
        except Exception as e:
            print(f"체크포인트 불러오기 실패: {e}")
            
        # 새 체크포인트 생성
        config = {"configurable": {"thread_id": session_id}}
        return video_agent_app.invoke(state, config=config)

    try:
        result = await asyncio.to_thread(run_agents)
        end = time.time()
        print(f"[처리 시간]: {end - start:.2f}초")
        result["session_id"] = session_id
        return result
    except Exception as e:
        print("[에이전트 실행 중 오류]:", e)
        raise e


# --- 3. 이력 기반 추천 ---
@router.post("/history-recommend")
async def history_prompt(req: HistoryRequest):
    session_id = req.session_id or str(uuid.uuid4())

    def run_history():
        state = {"user_input": req.user_input}
        
        # 이전 체크포인트가 있으면 불러오기
        try:
            thread_id = history_memory_saver.list_threads().get(session_id)
            if thread_id:
                config = {"configurable": {"thread_id": thread_id}}
                return history_guided_graph.invoke(state, config=config)
        except Exception as e:
            print(f"체크포인트 불러오기 실패: {e}")
            
        # 새 체크포인트 생성
        config = {"configurable": {"thread_id": session_id}}
        return history_guided_graph.invoke(state, config=config)

    result = await asyncio.to_thread(run_history)
    result["session_id"] = session_id

    return {
        "history_guided_prompt": result.get(
            "history_guided_prompt", "최적화된 프롬프트 없음"
        ),
        "followup_questions": result.get("followup_questions", []),
        "session_id": session_id
    }


# --- 4. 수정 미리보기 (diff_html 반환) ---
@router.post("/edit-preview")
async def preview_edit_diff(req: EditPreviewRequest):
    from agent.node.editor import edit_prompt_node  # 노드 직접 호출

    def run_preview():
        state = {
            "original_prompt": req.original_prompt,
            "edited_prompt": req.edited_prompt,
        }
        return edit_prompt_node(state)

    result = await asyncio.to_thread(run_preview)
    # if req.session_id:
    #     result["session_id"] = req.session_id
    return result
