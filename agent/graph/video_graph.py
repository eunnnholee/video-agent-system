# agent/graph/video_graph.py
from langgraph.graph import StateGraph
from agent.state import VideoAgentState
from agent.node.video import generate_video_node

video_graph = StateGraph(VideoAgentState)
video_graph.add_node("generate_video", generate_video_node)
video_graph.set_entry_point("generate_video")
video_graph.set_finish_point("generate_video")
video_agent_app = video_graph.compile()
