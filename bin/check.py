#!/usr/bin/env python3
"""验证 Scoop manifest 中的下载 URL 和文件 hash。

用法：python bin/check.py [manifest_name] [--url-only] [--hash-only]
  不指定 manifest_name 则检查 bucket/ 下所有 .json 文件。
  --url-only   仅检查 URL 可访问性（HEAD 请求）
  --hash-only  仅验证 hash（下载文件并计算 SHA256）
  默认同时检查 URL 和 hash。
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


def check_url(url: str) -> tuple[bool, str]:
    """发送 HEAD 请求检查 URL 是否可访问。"""
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "Scoop/1.0 (check.py)")
        with urllib.request.urlopen(req, timeout=15) as resp:
            return True, str(resp.status)
    except urllib.error.HTTPError as e:
        return False, str(e.code)
    except Exception as e:
        return False, str(e)


def check_hash(url: str, expected_hash: str) -> tuple[bool, str]:
    """下载文件并计算 SHA256，返回 (是否匹配，实际 hash)。"""
    try:
        req = urllib.request.Request(url, method="GET")
        req.add_header("User-Agent", "Scoop/1.0 (check.py)")
        with urllib.request.urlopen(req, timeout=60) as resp:
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
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    flags = {a for a in sys.argv[1:] if a.startswith("-")}

    filter_name = args[0] if args else None
    url_only = "--url-only" in flags
    hash_only = "--hash-only" in flags
    check_both = not url_only and not hash_only

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

        print(f"\n{'=' * 60}")
        print(f"📦 {manifest_path.name}")
        print(f"{'=' * 60}")

        for url, expected in pairs:
            filename = url.rsplit("/", 1)[-1]
            print(f"\n  📄 {filename}")
            print(f"  URL：{url}")

            # 检查 URL
            if url_only or check_both:
                ok, status = check_url(url)
                icon = "✅" if ok else "❌"
                print(f"  URL 检查：{icon} [{status}]")
                if not ok:
                    has_error = True

            # 检查 hash
            if hash_only or check_both:
                print(f"  期望 hash：{expected}")
                ok, actual = check_hash(url, expected)
                if ok:
                    print(f"  Hash 检查：✅ 匹配")
                else:
                    print(f"  实际 hash：{actual}")
                    print(f"  Hash 检查：❌ 不匹配")
                    has_error = True

    print()
    if has_error:
        print("⚠️  存在错误，请检查上述输出。")
    else:
        print("✅ 全部通过！")

    return 1 if has_error else 0


if __name__ == "__main__":
    sys.exit(main())
