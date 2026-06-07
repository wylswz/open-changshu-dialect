"""
使用 GPT-5.5 Vision 批量 OCR 图片（4线程并发）。
syntax → 语法长文，词汇 → 词汇表。
"""
import base64
import io
import os
import re
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from PIL import Image
from openai import OpenAI

BASE_DIR = Path(__file__).parent.parent
INPUT_DIR = BASE_DIR / "input"
DATASET_DIR = BASE_DIR / "dataset"

MAX_IMAGE_SIZE = 2048
JPEG_QUALITY = 85
MODEL = "gpt-5.5"
MAX_COMPLETION_TOKENS = 16384
WORKERS = 4

PROMPTS = {
    "vocab": "逐字提取这张书页上的所有文字。这是常熟方言词汇参考页，格式为'词条：释义'。每条词汇单独成行，保留原文格式和括号内注释，不要添加解释。",
    "syntax": "逐字提取这张书页上的所有文字。这是常熟方言语法特点介绍。保留原文的所有层级结构（章节标题、词汇条目等），不要添加解释。",
}


def encode_image(img_path: Path) -> str:
    img = Image.open(img_path)
    img.thumbnail((MAX_IMAGE_SIZE, MAX_IMAGE_SIZE), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=JPEG_QUALITY)
    return base64.b64encode(buf.getvalue()).decode()


def ocr_page(img_path: Path, prompt: str) -> tuple[str, str]:
    stem = img_path.stem
    img_b64 = encode_image(img_path)
    client = OpenAI()
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{img_b64}",
                        "detail": "high",
                    },
                },
            ],
        }],
        max_completion_tokens=MAX_COMPLETION_TOKENS,
    )
    content = resp.choices[0].message.content or ""
    return stem, content


def process_folder(folder_name: str):
    input_dir = INPUT_DIR / folder_name
    out_dir = BASE_DIR / "output" / folder_name
    out_dir.mkdir(parents=True, exist_ok=True)

    prompt = PROMPTS[folder_name]

    images = sorted(
        [f for f in os.listdir(input_dir) if f.lower().endswith((".jpg", ".jpeg"))],
        key=lambda x: int(re.search(r"(\d+)", x).group(1)),
    )

    pending = []
    for img_name in images:
        out_path = out_dir / f"{Path(img_name).stem}.txt"
        if out_path.exists() and out_path.stat().st_size > 0:
            print(f"  skip {img_name}")
        else:
            pending.append(input_dir / img_name)

    if not pending:
        print(f"  all done ({len(images)} images)")
        return

    print(f"  processing {len(pending)} images with {WORKERS} workers...")
    t0 = time.time()

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = {
            executor.submit(ocr_page, img_path, prompt): img_path
            for img_path in pending
        }
        for future in as_completed(futures):
            img_path = futures[future]
            try:
                stem, text = future.result()
                out_path = out_dir / f"{stem}.txt"
                out_path.write_text(text, encoding="utf-8")
                lines = text.count("\n") + 1
                print(f"  [{stem}] ok ({lines} lines)")
            except Exception as e:
                print(f"  [{img_path.stem}] ERROR: {e}")

    print(f"  done ({time.time() - t0:.1f}s)")


def main():
    for folder in ["vocab", "syntax"]:
        print(f"\n=== Processing {folder}/ ===")
        process_folder(folder)
    print("\nAll done.")


if __name__ == "__main__":
    main()
