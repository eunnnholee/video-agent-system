from fastapi import APIRouter
from pydantic import BaseModel
import asyncio
import time

# LangGraph 통합 워크플로우
from agent.graph.video_agent_graph import video_agent_app
from agent.graph.prompt_graph import graph_generate_prompt
from agent.graph.history_guided_graph import history_guided_graph

router = APIRouter()


# --- Pydantic 요청 모델 ---
class UserInputRequest(BaseModel):
    user_input: str


class EditConfirmRequest(BaseModel):
    user_input: str
    original_prompt: str
    edited_prompt: str


class HistoryRequest(BaseModel):
    user_input: str


class EditPreviewRequest(BaseModel):
    original_prompt: str
    edited_prompt: str


# --- 1. 최초 프롬프트 생성 ---
@router.post("/start")
async def start_prompt_generation(req: UserInputRequest):
    def run_prompt():
        state = {"user_input": req.user_input}
        return graph_generate_prompt.invoke(state)

    result = await asyncio.to_thread(run_prompt)
    return result


# --- 2. 수정된 프롬프트 기반 영상 생성 + 기록 ---
@router.post("/edit-confirm")
async def edit_and_save(req: EditConfirmRequest):
    start = time.time()

    def run_agents():
        state = {
            "user_input": req.user_input,
            "original_prompt": req.original_prompt,
            "edited_prompt": req.edited_prompt,
        }

        return video_agent_app.invoke(state)

    try:
        result = await asyncio.to_thread(run_agents)
        end = time.time()
        print(f"[처리 시간]: {end - start:.2f}초")
        return result
    except Exception as e:
        print("[에이전트 실행 중 오류]:", e)
        raise e


# --- 3. 이력 기반 추천 ---
@router.post("/history-recommend")
async def history_prompt(req: HistoryRequest):
    def run_history():
        state = {"user_input": req.user_input}
        return history_guided_graph.invoke(state)

    result = await asyncio.to_thread(run_history)

    return {
        "history_guided_prompt": result.get("history_guided_prompt", "최적화된 프롬프트 없음"),
        "followup_questions": result.get("followup_questions", [])
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
    return result
