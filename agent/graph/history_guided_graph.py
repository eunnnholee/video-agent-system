from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from agent.state import VideoAgentState
from agent.node.history_guided import generate_history_guided_prompt

# 메모리 저장소 설정
memory_saver = MemorySaver()

builder = StateGraph(VideoAgentState)
builder.add_node("generate_history_guided_prompt", generate_history_guided_prompt)
builder.set_entry_point("generate_history_guided_prompt")
builder.set_finish_point("generate_history_guided_prompt")

# 메모리 저장소 적용
history_guided_graph = builder.compile(checkpointer=memory_saver)