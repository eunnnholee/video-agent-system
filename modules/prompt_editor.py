import difflib

def get_diff(original: str, edited: str) -> list[str]:
    """
    원본과 수정된 텍스트 간 차이를 line-by-line으로 반환합니다.
    """
    diff = difflib.unified_diff(
        original.split(), edited.split(), lineterm=""
    )
    return list(diff)
