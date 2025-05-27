# modules/video_generator.py
import ffmpeg
from pathlib import Path

def generate_placeholder_video(text: str, output_path: str = "sample_videos/sample1.mp4"):
    Path("sample_videos").mkdir(exist_ok=True)

    (
        ffmpeg
        .input("color=c=black:s=1280x720:d=10", f='lavfi')
        .output(
            output_path,
            vf=f"drawtext=text='{text}':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=(h-text_h)/2",
            vcodec='libx264',
            pix_fmt='yuv420p'
        )
        .overwrite_output()
        .run()
    )
