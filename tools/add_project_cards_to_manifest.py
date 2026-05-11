#!/usr/bin/env python3
"""
Patch scripts/build_readme.py so dist/build-manifest.json includes project-card inventory.

Target behavior:
- Read assets/projects/index.json during manifest generation.
- Add project_cards_index to dist/build-manifest.json.
- Add project_cards_count to dist/build-manifest.json.
- Add project_cards to dist/build-manifest.json.
- Preserve README.base.md as canonical template.
- Preserve README.md as generated output.
- Preserve dry-run behavior.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "scripts" / "build_readme.py"


HELPER_BLOCK = '''def project_cards_manifest() -> dict[str, Any]:
    index_path = ROOT / "assets" / "projects" / "index.json"
    payload = load_json(index_path, {})

    if not isinstance(payload, dict):
        return {
            "index": "assets/projects/index.json",
            "count": 0,
            "cards": [],
        }

    cards = payload.get("cards", [])

    if not isinstance(cards, list):
        cards = []

    normalized: list[dict[str, Any]] = []

    for item in cards:
        if not isinstance(item, dict):
            continue

        path = str(item.get("path") or "").strip()
        full_name = str(item.get("full_name") or item.get("name") or "unknown").strip()
        name = str(item.get("name") or full_name.split("/")[-1] or "unknown").strip()

        if not path:
            continue

        exists = (ROOT / path).exists()

        normalized.append(
            {
                "full_name": full_name,
                "name": name,
                "path": path,
                "exists": exists,
                "html_url": str(item.get("html_url") or ""),
                "status": str(item.get("status") or "unknown"),
                "language": str(item.get("language") or "Unknown"),
                "stars": item.get("stars") or 0,
                "forks": item.get("forks") or 0,
                "open_issues": item.get("open_issues") or 0,
            }
        )

    normalized = sorted(normalized, key=lambda item: str(item.get("full_name", "")).lower())

    return {
        "index": "assets/projects/index.json",
        "count": len(normalized),
        "cards": normalized,
    }


'''


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def insert_helper(text: str) -> str:
    if "def project_cards_manifest()" in text:
        return text

    marker = "\ndef write_file("
    require(marker in text, "Could not locate write_file marker in scripts/build_readme.py")

    return text.replace(marker, "\n" + HELPER_BLOCK + "def write_file(", 1)


def patch_manifest_dict(text: str) -> str:
    if '"project_cards_index": "assets/projects/index.json"' in text:
        return text

    needle = '''        "outputs": outputs,
        "source_files": source_state,
        "status": "success",
'''

    replacement = '''        "outputs": outputs,
        "project_cards_index": "assets/projects/index.json",
        "project_cards_count": project_cards_manifest()["count"],
        "project_cards": project_cards_manifest()["cards"],
        "source_files": source_state,
        "status": "success",
'''

    require(needle in text, "Could not locate manifest insertion point in scripts/build_readme.py")

    return text.replace(needle, replacement, 1)


def main() -> int:
    require(GENERATOR.exists(), "Missing scripts/build_readme.py")

    original = GENERATOR.read_text(encoding="utf-8")
    patched = insert_helper(original)
    patched = patch_manifest_dict(patched)

    if patched == original:
        print("UNCHANGED: scripts/build_readme.py already contains project-card manifest fields")
    else:
        GENERATOR.write_text(patched, encoding="utf-8")
        print("PATCHED: scripts/build_readme.py")

    print("CHECK: project_cards_index manifest field enabled")
    print("CHECK: project_cards_count manifest field enabled")
    print("CHECK: project_cards manifest inventory enabled")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
