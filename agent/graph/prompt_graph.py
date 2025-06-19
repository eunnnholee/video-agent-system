from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from agent.state import VideoAgentState
from agent.node.prompt import generate_prompt_node

# 메모리 저장소 설정
memory_saver = MemorySaver()

builder = StateGraph(VideoAgentState)
builder.add_node("generate_prompt", generate_prompt_node)
builder.set_entry_point("generate_prompt")
builder.set_finish_point("generate_prompt")

# 메모리 저장소 적용
graph_generate_prompt = builder.compile(checkpointer=memory_saver)
