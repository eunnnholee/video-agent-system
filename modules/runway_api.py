import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("RUNWAY_API_KEY")

RUNWAY_HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "X-Runway-Version": "2024-11-06",
}

API_BASE_URL = "https://api.dev.runwayml.com/v1"


def get_task_result(
    task_id: str, task_type: str, max_retries: int = 20, wait_time: int = 2
) -> str:
    """Runway API의 task 결과에서 이미지/영상 URL 추출."""
    for attempt in range(max_retries):
        res = requests.get(f"{API_BASE_URL}/tasks/{task_id}", headers=RUNWAY_HEADERS)
        res.raise_for_status()
        data = res.json()
        status = data.get("status")
        print(f"[Runway] Task {task_type} 상태 확인: {status}")

        if status == "SUCCEEDED":
            output = data.get("output")

            # case 1: 문자열
            if isinstance(output, str):
                return output

            # case 2: 리스트
            elif isinstance(output, list):
                if len(output) > 0:
                    if isinstance(output[0], str):
                        return output[0]
                    elif isinstance(output[0], dict):
                        return output[0].get(
                            "imageUrl" if task_type == "image" else "videoUrl"
                        )

            # case 3: 딕셔너리
            elif isinstance(output, dict):
                return output.get("imageUrl" if task_type == "image" else "videoUrl")

            # 그 외는 에러
            raise RuntimeError(f"지원되지 않는 output 형식: {output}")

        elif status in ("FAILED", "CANCELLED"):
            raise RuntimeError(f"{task_type} 생성 실패: {status}")

        time.sleep(wait_time)

    raise TimeoutError(f"{task_type} 생성이 너무 오래 걸립니다. task_id: {task_id}")


def generate_image_from_text(prompt: str) -> str:
    url = f"{API_BASE_URL}/text_to_image"
    payload = {"promptText": prompt, "model": "gen4_image", "ratio": "1920:1080"}

    print("🚨 이미지 생성 요청 페이로드:", payload)

    res = requests.post(url, json=payload, headers=RUNWAY_HEADERS)
    print("📡 응답:", res.status_code, res.text)
    res.raise_for_status()

    task_id = res.json().get("id")
    if not task_id:
        raise RuntimeError("이미지 생성 실패: task_id 누락됨")

    return get_task_result(task_id, task_type="image")


def generate_video_from_image(image_url: str, prompt: str, duration: int = 10) -> str:
    url = f"{API_BASE_URL}/image_to_video"
    payload = {
        "promptImage": image_url,
        "model": "gen4_turbo",
        "promptText": prompt,
        "duration": duration,
        "ratio": "1280:720",
    }

    print("🚨 영상 생성 요청 페이로드:", payload)

    res = requests.post(url, json=payload, headers=RUNWAY_HEADERS)
    print("📡 응답:", res.status_code, res.text)
    res.raise_for_status()

    task_id = res.json().get("id")
    if not task_id:
        raise RuntimeError("영상 생성 실패: task_id 누락됨")

    return get_task_result(task_id, task_type="video")


def generate_video_from_text(prompt: str, num_frames: int = 250) -> str:
    print(f"[Runway] 텍스트 기반 영상 생성 시작: '{prompt}'")
    image_url = generate_image_from_text(prompt)
    print(f"[Runway] 이미지 생성 완료: {image_url}")

    # 프레임 수를 25fps 기준으로 초 단위 duration으로 변환
    duration = num_frames // 25

    video_url = generate_video_from_image(image_url, prompt, duration=duration)
    print(f"[Runway] 영상 생성 완료: {video_url}")
    return video_url

