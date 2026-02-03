#!/usr/bin/env python3
"""Utility to find external images in README.md, download them to assets/ and
replace the README links with local paths. Provides a programmatic API for tests
and supports a `--max-size-kb` guard to avoid downloading very large files.

Usage:
  python3 scripts/fetch_external_images.py [--max-size-kb 1024] [--dry-run]

Notes:
  - Not intended for CI (may download remote content). Use locally and review
    `README.md.bak` before committing.
"""
import os
import re
import hashlib
import argparse
from urllib.parse import urlparse

try:
    import requests
except Exception:
    print("Required dependency 'requests' missing. Install with 'pip install requests'")
    raise

README = 'README.md'
ASSETS_DIR = 'assets'
IMAGE_REGEX_MD = re.compile(r"!\[[^\]]*\]\((https?://[^)]+)\)")
IMAGE_REGEX_HTML = re.compile(r"<img[^>]+src=[\"'](https?://[^\"']+)[\"'][^>]*>")

os.makedirs(ASSETS_DIR, exist_ok=True)


def process_readme(max_size_bytes=None, dry_run=False):
    """Find external images, download them if they are below max_size_bytes
    (if provided), and return a dict of {remote_url: local_path}. If dry_run
    is True, simulate downloads but don't write files or modify README.
    """
    with open(README, 'r', encoding='utf-8') as f:
        content = f.read()

    urls = set(IMAGE_REGEX_MD.findall(content) + IMAGE_REGEX_HTML.findall(content))
    if not urls:
        print('No external image URLs found in README.md')
        return {}

    replacements = {}
    for url in urls:
        try:
            head = requests.head(url, timeout=10)
            head.raise_for_status()
            content_length = head.headers.get('Content-Length')
            if content_length and max_size_bytes and int(content_length) > max_size_bytes:
                print(f"Skipping {url}: Content-Length {content_length} exceeds max {max_size_bytes}")
                continue

            # If HEAD didn't provide length or was acceptable, do GET
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            if max_size_bytes and len(r.content) > max_size_bytes:
                print(f"Skipping {url}: downloaded size {len(r.content)} exceeds max {max_size_bytes}")
                continue

            # derive a safe filename from the url
            parsed = urlparse(url)
            base = os.path.basename(parsed.path)
            if not base:
                base = hashlib.sha1(url.encode()).hexdigest()[:10] + '.png'
            local_name = f"{hashlib.sha1(url.encode()).hexdigest()[:8]}_{base}"
            local_path = os.path.join(ASSETS_DIR, local_name)

            if dry_run:
                replacements[url] = local_path
                print(f"[DRY-RUN] Would download: {url} -> {local_path}")
            else:
                with open(local_path, 'wb') as out:
                    out.write(r.content)
                replacements[url] = local_path
                print(f"Downloaded: {url} -> {local_path}")

        except Exception as e:
            print(f"Failed to download {url}: {e}")

    if not replacements:
        print('No images downloaded.')
        return {}

    if dry_run:
        return replacements

    # Backup README
    with open(README + '.bak', 'w', encoding='utf-8') as f:
        f.write(content)

    new_content = content
    for remote, local in replacements.items():
        new_content = new_content.replace(f"({remote})", f"({local})")
        new_content = new_content.replace(f'"{remote}"', f'"{local}"')

    with open(README, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print('README.md updated with local asset references. Backup saved to README.md.bak')
    return replacements


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--max-size-kb', type=int, default=0, help='Maximum download size in kilobytes (0 = no limit)')
    p.add_argument('--dry-run', action='store_true', help='Do not write files; show what would be done')
    args = p.parse_args()

    max_size = args.max_size_kb * 1024 if args.max_size_kb else None
    process_readme(max_size_bytes=max_size, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
