import difflib
from pathlib import Path

def get_diff_html(original: str, edited: str) -> str:
    differ = difflib.HtmlDiff()
    diff_table = differ.make_table(
        original.splitlines(), edited.splitlines(),
        fromdesc="Original Prompt", todesc="Edited Prompt",
        context=True, numlines=2
    )

    css_path = Path("styles/diff.css")
    custom_style = f"<style>{css_path.read_text(encoding='utf-8')}</style>"

    return custom_style + diff_table