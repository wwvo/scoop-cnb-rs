#!/usr/bin/env python3
"""检查 Scoop manifest 中的下载 URL 是否可访问。

用法：python bin/checkurls.py [manifest_name]
  不指定 manifest_name 则检查 bucket/ 下所有 .json 文件。
"""

import json
import sys
import urllib.request
from pathlib import Path

BUCKET_DIR = Path(__file__).resolve().parent.parent / "bucket"


def get_urls(manifest: dict) -> list[str]:
    """从 manifest 中提取所有下载 URL。"""
    urls = []
    if "url" in manifest:
        urls.append(manifest["url"])
    if "architecture" in manifest:
        for arch_info in manifest["architecture"].values():
            if "url" in arch_info:
                urls.append(arch_info["url"])
    return urls


def check_url(url: str) -> tuple[bool, str]:
    """发送 HEAD 请求检查 URL 是否可访问。"""
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "Scoop/1.0 (checkurls.py)")
        with urllib.request.urlopen(req, timeout=15) as resp:
            return True, str(resp.status)
    except urllib.error.HTTPError as e:
        return False, str(e.code)
    except Exception as e:
        return False, str(e)


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

        urls = get_urls(data)
        if not urls:
            continue

        print(f"\n检查 {manifest_path.name}:")
        for url in urls:
            ok, status = check_url(url)
            icon = "✅" if ok else "❌"
            print(f"  {icon} [{status}] {url}")
            if not ok:
                has_error = True

    return 1 if has_error else 0


if __name__ == "__main__":
    sys.exit(main())
