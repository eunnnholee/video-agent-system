from fastapi import FastAPI
from backend.agent_router import router
import logging
from datetime import datetime
from pathlib import Path
from modules.vector_store import update_collection_from_json_files

# 로그 설정
now = datetime.now().strftime("%m-%d_%H_%M")
log_file = Path("logs") / f"{now}_agent.log"
log_file.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 라우터 등록
app = FastAPI()
app.include_router(router, prefix="/agent")

# 서버 시작 시 기존 JSON 파일들을 Chroma DB에 로드
@app.on_event("startup")
async def startup_db_client():
    logger.info("서버 시작: 기존 JSON 파일들을 Chroma DB에 로드합니다.")
    count = update_collection_from_json_files()
    logger.info(f"총 {count}개의 프롬프트를 Chroma DB에 로드했습니다.")
