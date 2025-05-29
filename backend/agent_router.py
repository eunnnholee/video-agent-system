from fastapi import APIRouter
from pydantic import BaseModel
import asyncio

from agent.graph.prompt_graph import graph_generate_prompt
from agent.graph.edit_graph import edit_agent_app
from agent.graph.save_graph import save_agent_app
from agent.graph.video_graph import video_agent_app

from agent.graph.history_guided_graph import history_guided_graph

import time

router = APIRouter()


# Pydantic 입력 모델
class UserInputRequest(BaseModel):
    user_input: str


class EditConfirmRequest(BaseModel):
    original_prompt: str
    edited_prompt: str
    save_confirmed: bool = True


class HistoryRequest(BaseModel):
    user_input: str


@router.post("/start")
async def start_prompt_generation(req: UserInputRequest):
    def run_prompt():
        state = {"user_input": req.user_input}
        return graph_generate_prompt.invoke(state)

    result = await asyncio.to_thread(run_prompt)
    return result


@router.post("/edit-confirm")
async def edit_and_save(req: EditConfirmRequest):
    start = time.time()

    def run_agents():
        state = {
            "original_prompt": req.original_prompt,
            "edited_prompt": req.edited_prompt,
            "save_confirmed": req.save_confirmed,
        }

        state = edit_agent_app.invoke(state)
        state = save_agent_app.invoke(state)
        state = video_agent_app.invoke(state)

        return state

    try:
        result = await asyncio.to_thread(run_agents)
        end = time.time()
        print(f"[처리 시간]: {end - start:.2f}초")
        return result
    except Exception as e:
        print("[에이전트 실행 중 오류]:", e)
        raise e


@router.post("/history-recommend")
async def history_prompt(req: HistoryRequest):
    def run_history():
        state = {"user_input": req.user_input}
        return history_guided_graph.invoke(state)

    result = await asyncio.to_thread(run_history)
    return result
