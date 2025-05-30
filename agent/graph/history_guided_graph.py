from langgraph.graph import StateGraph
from agent.state import VideoAgentState
from agent.node.history_guided import generate_history_guided_prompt

builder = StateGraph(VideoAgentState)
builder.add_node("generate_history_guided_prompt", generate_history_guided_prompt)
builder.set_entry_point("generate_history_guided_prompt")
builder.set_finish_point("generate_history_guided_prompt")

history_guided_graph = builder.compile()