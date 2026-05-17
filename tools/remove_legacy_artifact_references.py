#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
ROOT = Path.cwd()
TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".py",
    ".sh",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
}
SKIP_DIRS = {
    ".git",
    ".backups",
    "logs",
    "__pycache__",
    ".kilo",
}
REPLACEMENTS = {
    "removed legacy tmp README artifact": "removed legacy tmp README artifact",
    "removed legacy README template artifact": "removed legacy README template artifact",
    "removed legacy terminalizer artifact": "removed legacy terminalizer artifact",
    "removed legacy telemetry identifier": "removed legacy telemetry identifier",
    "removed legacy quote SVG artifact": "removed legacy quote SVG artifact",
    "removed runtime lock artifact": "removed runtime lock artifact",
}
ARCHITECTURE_NOTE = (
    "Current surface contract: README.base.md is the canonical template; "
    "README.md is generated output; dist/build-manifest.json is tracked build attestation."
)
def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & SKIP_DIRS)
def patch_file(path: Path) -> bool:
    if should_skip(path):
        return False
    if path.suffix not in TEXT_EXTENSIONS:
        return False
    if not path.is_file():
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    original = text
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    text = text.replace(
        "removed legacy tmp README artifact                  removed legacy source; not a source of truth",
        "Legacy tmp/config/runtime artifacts were removed; README.base.md is the only source of truth",
    )
    text = text.replace(
        "removed legacy tmp README artifact | Removed legacy source; not used as source of truth",
        "removed legacy tmp/config/runtime artifacts | not used as source of truth",
    )
    text = text.replace(
        "`removed legacy tmp README artifact` as README source of truth. The file has been removed.",
        "`README.base.md` as the only README source of truth.",
    )
    text = text.replace(
        "`removed legacy tmp README artifact` as README source of truth.",
        "`README.base.md` as the only README source of truth.",
    )
    text = text.replace(
        "Do not use `removed legacy tmp README artifact` as a source of truth.",
        "Do not use removed tmp/config/runtime artifacts as a source of truth. "
        + ARCHITECTURE_NOTE,
    )
    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"PATCHED: {path}")
        return True
    return False
def main() -> int:
    changed = 0
    for path in sorted(ROOT.rglob("*")):
        if patch_file(path):
            changed += 1
    print(f"PATCHED_FILES={changed}")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
