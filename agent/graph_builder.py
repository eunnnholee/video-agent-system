from langgraph.graph import StateGraph
from agent.state import VideoAgentState

from agent.node.prompt import generate_prompt_node
from agent.node.edit import edit_prompt_node
from agent.node.diff import compare_diff_node
from agent.node.save import save_history_node
from agent.node.video import generate_video_node

# LangGraph 정의
graph = StateGraph(VideoAgentState)

# 노드 등록
graph.add_node("generate_prompt", generate_prompt_node)
graph.add_node("edit_prompt", edit_prompt_node)
graph.add_node("compare_diff", compare_diff_node)
graph.add_node("save_history", save_history_node)
graph.add_node("generate_video", generate_video_node)

# 노드 연결 (Edges)
graph.set_entry_point("generate_prompt")
graph.add_edge("generate_prompt", "edit_prompt")
graph.add_edge("edit_prompt", "compare_diff")
graph.add_edge("compare_diff", "save_history")
graph.add_edge("save_history", "generate_video")
graph.set_finish_point("generate_video")

# 그래프 컴파일
video_agent_app = graph.compile()
