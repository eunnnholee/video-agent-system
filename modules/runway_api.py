import os
import requests
from dotenv import load_dotenv
import time

load_dotenv()
API_KEY = os.getenv("RUNWAY_API_KEY")

RUNWAY_HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def generate_image_from_text(prompt: str) -> str:
    """
    주어진 텍스트 프롬프트를 기반으로 Runway의 gen4_image 모델을 사용해 이미지를 생성한다.

    Args:
        prompt (str): 이미지 생성에 사용할 텍스트 설명

    Returns:
        str: 생성된 이미지의 URL

    Raises:
        RuntimeError: 이미지 URL이 응답에서 누락된 경우
        HTTPError: API 호출 실패 시
    """
    url = "https://api.runwayml.com/v1/generate"
    payload = {
        "model": "gen4_image",
        "prompt": prompt,
        "output_format": "png"
    }

    res = requests.post(url, json=payload, headers=RUNWAY_HEADERS)
    res.raise_for_status()
    image_url = res.json().get("image_url")
    if not image_url:
        raise RuntimeError("이미지 생성 실패: image_url 누락됨")

    # 이미지가 CDN에 등록될 때까지 대기
    time.sleep(2)
    return image_url


def generate_video_from_image(image_url: str, num_frames: int = 250) -> str:
    """
    주어진 이미지 URL을 기반으로 Runway의 gen4_turbo 모델을 사용해 영상을 생성한다.

    Args:
        image_url (str): 영상 생성에 사용할 이미지의 URL
        num_frames (int): 생성할 프레임 수 (기본값: 250 = 약 10초 @25fps)

    Returns:
        str: 생성된 영상의 URL

    Raises:
        RuntimeError: 영상 URL이 응답에서 누락된 경우
        HTTPError: API 호출 실패 시
    """
    url = "https://api.runwayml.com/v1/generate"
    payload = {
        "model": "gen4_turbo",
        "input_image_url": image_url,
        "output_format": "mp4",
        "num_frames": num_frames
    }

    res = requests.post(url, json=payload, headers=RUNWAY_HEADERS)
    res.raise_for_status()
    video_url = res.json().get("video_url")
    if not video_url:
        raise RuntimeError("영상 생성 실패: video_url 누락됨")
    return video_url


def generate_video_from_text(prompt: str, num_frames: int = 250) -> str:
    """
    텍스트 프롬프트를 기반으로 이미지 생성 후, 해당 이미지를 활용하여 영상을 생성하는 전체 파이프라인을 실행한다.

    Args:
        prompt (str): 텍스트 기반 영상 콘텐츠 설명
        num_frames (int): 생성할 프레임 수 (기본값: 250 = 약 10초)

    Returns:
        str: 최종 생성된 영상의 URL

    Raises:
        RuntimeError: 중간 단계에서 이미지 또는 영상 URL 생성 실패 시
        HTTPError: API 호출 실패 시
    """
    print(f"[Runway] 텍스트 기반 영상 생성 시작: '{prompt}'")
    image_url = generate_image_from_text(prompt)
    print(f"[Runway] 이미지 생성 완료: {image_url}")
    video_url = generate_video_from_image(image_url, num_frames=num_frames)
    print(f"[Runway] 영상 생성 완료: {video_url}")
    return video_url
