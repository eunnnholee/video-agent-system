# agent/graph/edit_graph.py

from langgraph.graph import StateGraph
from agent.state import VideoAgentState
from agent.node.edit import edit_prompt_node  # ✅ diff는 제거됨

# 그래프 초기화
edit_graph = StateGraph(VideoAgentState)

# 단일 노드만 추가 (수정 + diff 계산 포함)
edit_graph.add_node("edit_prompt", edit_prompt_node)

# 시작 및 종료 지점을 동일 노드로 설정
edit_graph.set_entry_point("edit_prompt")
edit_graph.set_finish_point("edit_prompt")

# 그래프 컴파일
edit_agent_app = edit_graph.compile()
