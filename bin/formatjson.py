#!/usr/bin/env python3
"""格式化 Scoop manifest JSON 文件（4 空格缩进）。

用法: python bin/formatjson.py [manifest_name]
  不指定 manifest_name 则格式化 bucket/ 下所有 .json 文件。
"""

import json
import sys
from pathlib import Path

BUCKET_DIR = Path(__file__).resolve().parent.parent / "bucket"


def format_json(path: Path) -> bool:
    """格式化单个 JSON 文件，返回是否有变更。"""
    with open(path, encoding="utf-8") as f:
        original = f.read()

    data = json.loads(original)
    formatted = json.dumps(data, indent=4, ensure_ascii=False) + "\n"

    if original == formatted:
        return False

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(formatted)
    return True


def main():
    filter_name = sys.argv[1] if len(sys.argv) > 1 else None
    manifests = sorted(BUCKET_DIR.glob("*.json"))

    if filter_name:
        manifests = [m for m in manifests if m.stem == filter_name]

    if not manifests:
        print("未找到 manifest 文件。")
        return 1

    for manifest_path in manifests:
        changed = format_json(manifest_path)
        icon = "✏️" if changed else "✅"
        status = "已格式化" if changed else "无变更"
        print(f"  {icon} {manifest_path.name}: {status}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
