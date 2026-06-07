"""
PaddleX layout_parsing 批量识别（版面分析 + OCR，适合双栏排版）。
输出 HTML table 格式，保留左右分栏结构。
"""
import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

from paddlex import create_pipeline

BASE_DIR = Path(__file__).parent.parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output" / "layout"

IMAGE_DIRS = {
    "sentences": INPUT_DIR / "sentences",
    "vocab": INPUT_DIR / "vocab",
    "syntax": INPUT_DIR / "syntax",
}


def html_table_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if not table:
        return html
    lines = []
    for tr in table.find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        if all(not c for c in cells):
            continue
        lines.append(" | ".join(cells))
    return "\n".join(lines)


def process_images(input_dir: Path, output_subdir: str):
    pipeline = create_pipeline("layout_parsing")
    out_dir = OUTPUT_DIR / output_subdir
    out_dir.mkdir(parents=True, exist_ok=True)

    images = sorted(
        [f for f in os.listdir(input_dir) if f.lower().endswith((".jpg", ".jpeg"))],
        key=lambda x: int(re.search(r"(\d+)", x).group(1)),
    )

    for img_name in images:
        img_path = input_dir / img_name
        stem = Path(img_name).stem
        txt_path = out_dir / f"{stem}.txt"
        html_path = out_dir / f"{stem}.html"

        if txt_path.exists():
            print(f"  skip {img_name}")
            continue

        print(f"  processing {img_name} ...", end=" ", flush=True)
        try:
            for r in pipeline.predict(str(img_path)):
                data = r.json
                html = data["res"]["parsing_res_list"][0]["block_content"]
                html_path.write_text(html, encoding="utf-8")
                text = html_table_to_text(html)
                txt_path.write_text(text, encoding="utf-8")
                print(f"ok ({len(text.splitlines())} lines)")
                break
        except Exception as e:
            print(f"ERROR: {e}")


def main():
    for name, dir_path in IMAGE_DIRS.items():
        if not dir_path.exists():
            continue
        print(f"\n=== Processing {name}/ ===")
        process_images(dir_path, name)
    print("\nDone.")


if __name__ == "__main__":
    main()
