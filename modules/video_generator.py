import ffmpeg
from pathlib import Path
import streamlit as st

import re

def sanitize_text(text: str) -> str:
    # 줄바꿈 제거
    text = text.replace("\n", " ")

    # ffmpeg에서 문제되는 특수문자 제거 또는 대체
    text = text.replace(":", "-")         # 콜론 → 대시
    text = text.replace("'", "")          # 작은 따옴표 제거
    text = text.replace("\\", "")         # 역슬래시 제거
    text = re.sub(r"[^\w\s.,!?-]", "", text)  # 그 외 특수문자 제거

    # 길이 제한
    if len(text) > 80:
        text = text[:80] + "..."

    return text

def generate_placeholder_video(text: str, output_path: str = "sample_videos/sample1.mp4"):
    Path("sample_videos").mkdir(exist_ok=True)

    # 텍스트 정리
    safe_text = sanitize_text(text)

    try:
        (
            ffmpeg
            .input("color=c=black:s=1280x720:d=10", f='lavfi')
            .output(
                output_path,
                vf=f"drawtext=text='{safe_text}':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=(h-text_h)/2",
                vcodec='libx264',
                pix_fmt='yuv420p'
            )
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        st.error("❌ ffmpeg 실행 중 오류 발생!")
        st.code("STDOUT:\n" + e.stdout.decode("utf-8", errors="ignore"))
        st.code("STDERR:\n" + e.stderr.decode("utf-8", errors="ignore"))
        raise
