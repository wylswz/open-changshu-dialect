"""
PaddleOCR PP-OCRv4_mobile 批量识别（轻量方案，资源占用低）。
"""
import os
import re
from pathlib import Path

from paddleocr import PaddleOCR

BASE_DIR = Path(__file__).parent.parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output" / "paddleocr"

IMAGE_DIRS = {
    "sentences": INPUT_DIR / "sentences",
    "vocab": INPUT_DIR / "vocab",
    "syntax": INPUT_DIR / "syntax",
}


def process_images(ocr, input_dir: Path, output_subdir: str):
    out_dir = OUTPUT_DIR / output_subdir
    out_dir.mkdir(parents=True, exist_ok=True)

    images = sorted(
        [f for f in os.listdir(input_dir) if f.lower().endswith((".jpg", ".jpeg"))],
        key=lambda x: int(re.search(r"(\d+)", x).group(1)),
    )

    for img_name in images:
        img_path = input_dir / img_name
        out_path = out_dir / f"{Path(img_name).stem}.txt"
        if out_path.exists():
            print(f"  skip {img_name}")
            continue

        print(f"  processing {img_name} ...")
        try:
            result = ocr.predict(str(img_path))
            data = result[0].json
            texts = data.get("res", {}).get("rec_texts", [])
            out_path.write_text("\n".join(texts), encoding="utf-8")
            print(f"    -> {len(texts)} lines")
        except Exception as e:
            print(f"    ERROR: {e}")


def main():
    ocr = PaddleOCR(lang="ch", ocr_version="PP-OCRv4")
    print("PaddleOCR ready.\n")

    for name, dir_path in IMAGE_DIRS.items():
        if not dir_path.exists():
            continue
        print(f"=== Processing {name}/ ===")
        process_images(ocr, dir_path, name)

    print("\nDone.")


if __name__ == "__main__":
    main()
