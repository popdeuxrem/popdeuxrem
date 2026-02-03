#!/usr/bin/env python3
"""Simple utility to find external images in README.md, download them to assets/
and replace the README links with local paths. Run in repository root.
"""
import os
import re
import hashlib
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

with open(README, 'r', encoding='utf-8') as f:
    content = f.read()

urls = set(IMAGE_REGEX_MD.findall(content) + IMAGE_REGEX_HTML.findall(content))
if not urls:
    print('No external image URLs found in README.md')
    exit(0)

replacements = {}
for url in urls:
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        # derive a safe filename from the url
        parsed = urlparse(url)
        base = os.path.basename(parsed.path)
        if not base:
            base = hashlib.sha1(url.encode()).hexdigest()[:10] + '.png'
        local_name = f"{hashlib.sha1(url.encode()).hexdigest()[:8]}_{base}"
        local_path = os.path.join(ASSETS_DIR, local_name)
        with open(local_path, 'wb') as out:
            out.write(r.content)
        replacements[url] = local_path
        print(f"Downloaded: {url} -> {local_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

if not replacements:
    print('No images downloaded.')
    exit(0)

new_content = content
for remote, local in replacements.items():
    new_content = new_content.replace(f"({remote})", f"({local})")
    new_content = new_content.replace(f'"{remote}"', f'"{local}"')

# Backup README
with open(README + '.bak', 'w', encoding='utf-8') as f:
    f.write(content)

with open(README, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('README.md updated with local asset references. Backup saved to README.md.bak')
