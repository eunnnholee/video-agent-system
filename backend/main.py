from fastapi import FastAPI
from backend.agent_router import router
import logging
from datetime import datetime
from pathlib import Path

# # 로그 설정
# now = datetime.now().strftime("%m-%d_%H_%M")
# log_file = Path("logs") / f"{now}_agent.log"
# log_file.parent.mkdir(exist_ok=True)

# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
#     handlers=[
#         logging.FileHandler(log_file, encoding="utf-8"),
#         logging.StreamHandler()
#     ]
# )

app = FastAPI()
app.include_router(router, prefix="/agent")
