from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from agent.state import VideoAgentState
from agent.node.prompt import generate_prompt_node
from agent.node.editor import edit_prompt_node
from agent.node.optimizer import optimize_prompt_node
from agent.node.save import save_prompt_node      
from agent.node.video import generate_video_node

# 메모리 저장소 설정
memory_saver = MemorySaver()

builder = StateGraph(VideoAgentState)

# 1. 사용자 입력 기반 프롬프트 생성
builder.add_node("generate_prompt", generate_prompt_node)
builder.set_entry_point("generate_prompt")

# 2. 프롬프트 수정 (diff_html 생성)
builder.add_node("edit_prompt", edit_prompt_node)
builder.add_edge("generate_prompt", "edit_prompt")

# 3. 프롬프트 저장 확정 (final_prompt 반영)
builder.add_node("save_prompt", save_prompt_node) 
builder.add_edge("edit_prompt", "save_prompt")     

# 4. 이미지 생성용 프롬프트 최적화
builder.add_node("optimize_prompt", optimize_prompt_node)
builder.add_edge("save_prompt", "optimize_prompt") 
# 5. 영상 생성
builder.add_node("generate_video", generate_video_node)
builder.add_edge("optimize_prompt", "generate_video")

# 종료 지점 설정
builder.set_finish_point("generate_video")

# 메모리 저장소 적용
video_agent_app = builder.compile(checkpointer=memory_saver)
