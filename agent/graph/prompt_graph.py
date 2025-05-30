from langgraph.graph import StateGraph
# from langgraph.checkpoint.sqlite import SqliteSaver
from agent.state import VideoAgentState
from agent.node.prompt import generate_prompt_node

# saver = SqliteSaver.from_conn_string("sqlite:///memory")

builder = StateGraph(VideoAgentState)
builder.add_node("generate_prompt", generate_prompt_node)
builder.set_entry_point("generate_prompt")
builder.set_finish_point("generate_prompt")

graph_generate_prompt = builder.compile()
