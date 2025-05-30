from pathlib import Path

def get_diff_html(original: str, edited: str) -> str:
    from difflib import ndiff

    # 1. CSS 로드
    css_path = Path("styles/diff.css")
    custom_style = f"<style>{css_path.read_text(encoding='utf-8')}</style>"

    # 2. Diff 계산
    orig_diff = ""
    edit_diff = ""
    for d in ndiff(original.split(), edited.split()):
        if d.startswith("- "):
            orig_diff += f'<span class="diff-del">{d[2:]}</span> '
        elif d.startswith("+ "):
            edit_diff += f'<span class="diff-add">{d[2:]}</span> '
        elif d.startswith("  "):
            word = d[2:]
            orig_diff += word + " "
            edit_diff += word + " "

    # 3. HTML 조합
    html = f"""
    {custom_style}
    <div class="diff-wrapper">
      <div class="diff-pair">
        <div class="diff-column">
          <div class="diff-title">🟥 원본 (Before)</div>
          <div class="diff-block">{orig_diff.strip()}</div>
        </div>
        <div class="diff-column">
          <div class="diff-title">🟩 수정본 (After)</div>
          <div class="diff-block">{edit_diff.strip()}</div>
        </div>
      </div>
    </div>
    """
    return html
