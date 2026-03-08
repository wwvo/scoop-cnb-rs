#!/usr/bin/env python3
"""验证 Scoop manifest 中的文件 hash 是否正确。

用法：python bin/checkhashes.py [manifest_name]
  不指定 manifest_name 则检查 bucket/ 下所有 .json 文件。
"""

import hashlib
import json
import sys
import urllib.request
from pathlib import Path

BUCKET_DIR = Path(__file__).resolve().parent.parent / "bucket"


def get_urls_and_hashes(manifest: dict) -> list[tuple[str, str]]:
    """从 manifest 中提取所有 (url, hash) 对。"""
    pairs = []
    if "url" in manifest and "hash" in manifest:
        pairs.append((manifest["url"], manifest["hash"]))
    if "architecture" in manifest:
        for arch_info in manifest["architecture"].values():
            if "url" in arch_info and "hash" in arch_info:
                pairs.append((arch_info["url"], arch_info["hash"]))
    return pairs


def check_hash(url: str, expected_hash: str) -> tuple[bool, str]:
    """下载文件并计算 SHA256，返回 (是否匹配，实际 hash)。"""
    try:
        req = urllib.request.Request(url, method="GET")
        req.add_header("User-Agent", "Scoop/1.0 (checkhashes.py)")
        with urllib.request.urlopen(req, timeout=30) as resp:
            sha256 = hashlib.sha256()
            while True:
                chunk = resp.read(8192)
                if not chunk:
                    break
                sha256.update(chunk)
            actual = sha256.hexdigest()
            return actual == expected_hash, actual
    except Exception as e:
        return False, f"下载失败：{e}"


def main():
    filter_name = sys.argv[1] if len(sys.argv) > 1 else None
    manifests = sorted(BUCKET_DIR.glob("*.json"))

    if filter_name:
        manifests = [m for m in manifests if m.stem == filter_name]

    if not manifests:
        print("未找到 manifest 文件。")
        return 1

    has_error = False
    for manifest_path in manifests:
        with open(manifest_path, encoding="utf-8") as f:
            data = json.load(f)

        pairs = get_urls_and_hashes(data)
        if not pairs:
            continue

        print(f"\n检查 {manifest_path.name}:")
        for url, expected in pairs:
            print(f"  URL: {url}")
            print(f"  期望：{expected}")
            ok, actual = check_hash(url, expected)
            if ok:
                print(f"  结果：✅ 匹配")
            else:
                print(f"  实际：{actual}")
                print(f"  结果：❌ 不匹配")
                has_error = True

    return 1 if has_error else 0


if __name__ == "__main__":
    sys.exit(main())
