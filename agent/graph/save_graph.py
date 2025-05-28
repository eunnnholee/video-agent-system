# agent/graph/save_graph.py
from langgraph.graph import StateGraph
from agent.state import VideoAgentState
from agent.node.save import save_prompt_node

save_graph = StateGraph(VideoAgentState)
save_graph.add_node("save_history", save_prompt_node)
save_graph.set_entry_point("save_history")
save_graph.set_finish_point("save_history")
save_agent_app = save_graph.compile()
