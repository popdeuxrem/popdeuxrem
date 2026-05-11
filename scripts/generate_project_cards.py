#!/usr/bin/env python3
"""
Deterministic project card generator.

Reads:
  - metrics/metrics.json
  - metrics/aggregate.json

Writes:
  - assets/projects/<safe-repo-name>.svg
  - assets/projects/index.json

Rules:
  - no network calls
  - deterministic output order
  - deterministic filenames
  - SVG-only generated artifacts
  - no secrets
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
METRICS_JSON = ROOT / "metrics" / "metrics.json"
AGGREGATE_JSON = ROOT / "metrics" / "aggregate.json"
PROJECTS_DIR = ROOT / "assets" / "projects"
INDEX_JSON = PROJECTS_DIR / "index.json"


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {path.relative_to(ROOT)}: {exc}") from exc


def write_text(path: Path, content: str, dry_run: bool = False) -> None:
    if dry_run:
        print(f"DRY-RUN: would write {path.relative_to(ROOT)}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"WROTE: {path.relative_to(ROOT)}")


def write_json(path: Path, payload: Any, dry_run: bool = False) -> None:
    encoded = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    write_text(path, encoded, dry_run=dry_run)


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def safe_int(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = value.replace("/", "__")
    value = re.sub(r"[^a-z0-9_.-]+", "-", value)
    value = re.sub(r"-+", "-", value)
    value = value.strip("-")
    return value or "unknown"


def truncate(value: Any, length: int) -> str:
    text = str(value or "").strip()
    if len(text) <= length:
        return text
    return text[: max(0, length - 1)].rstrip() + "…"


def normalize_repositories() -> list[dict[str, Any]]:
    metrics = load_json(METRICS_JSON, {})
    aggregate = load_json(AGGREGATE_JSON, {})

    candidates: list[Any] = []

    if isinstance(metrics, dict):
        raw = metrics.get("repositories") or metrics.get("repos") or []
        if isinstance(raw, list):
            candidates.extend(raw)

    if not candidates and isinstance(aggregate, dict):
        raw = aggregate.get("top_repos") or []
        if isinstance(raw, list):
            candidates.extend(raw)

    repos: list[dict[str, Any]] = []

    for item in candidates:
        if not isinstance(item, dict):
            continue

        full_name = str(
            item.get("full_name")
            or item.get("repo")
            or item.get("slug")
            or item.get("name")
            or "unknown"
        )

        name = str(item.get("name") or full_name.split("/")[-1] or "unknown")

        repos.append(
            {
                "full_name": full_name,
                "name": name,
                "html_url": item.get("html_url") or f"https://github.com/{full_name}",
                "description": item.get("description") or "Deterministic system artifact.",
                "language": item.get("language") or "Unknown",
                "stars": safe_int(item.get("stars") or item.get("stargazers_count")),
                "forks": safe_int(item.get("forks") or item.get("forks_count")),
                "open_issues": safe_int(item.get("open_issues") or item.get("open_issues_count")),
                "status": item.get("status") or "tracked",
                "updated_at": item.get("updated_at") or item.get("pushed_at") or None,
            }
        )

    deduped: dict[str, dict[str, Any]] = {}
    for repo in repos:
        deduped[str(repo["full_name"]).lower()] = repo

    return [deduped[key] for key in sorted(deduped.keys())]


def status_color(status: str) -> str:
    normalized = str(status or "").lower()

    if normalized in {"tracked", "ok", "healthy", "active"}:
        return "#00ff9d"

    if normalized in {"offline", "unavailable", "unknown"}:
        return "#d29922"

    if normalized in {"failed", "error", "missing"}:
        return "#ff5c8a"

    return "#8b949e"


def language_color(language: str) -> str:
    digest = hashlib.sha256(language.encode("utf-8")).hexdigest()
    palette = [
        "#00f3ff",
        "#bc8cff",
        "#00ff9d",
        "#f5d76e",
        "#ff7ab6",
        "#7aa2ff",
    ]
    return palette[int(digest[:2], 16) % len(palette)]


def svg_card(repo: dict[str, Any]) -> str:
    full_name = str(repo["full_name"])
    name = str(repo["name"])
    description = truncate(repo.get("description"), 88)
    language = str(repo.get("language") or "Unknown")
    status = str(repo.get("status") or "tracked")
    stars = safe_int(repo.get("stars"))
    forks = safe_int(repo.get("forks"))
    issues = safe_int(repo.get("open_issues"))
    updated = str(repo.get("updated_at") or "unknown")

    trace = hashlib.sha256(json.dumps(repo, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:12]
    lang_color = language_color(language)
    state_color = status_color(status)

    return f'''<svg width="760" height="240" viewBox="0 0 760 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(full_name)} project card">
  <defs>
    <linearGradient id="border" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#00f3ff"/>
      <stop offset="48%" stop-color="#bc8cff"/>
      <stop offset="100%" stop-color="#00ff9d"/>
    </linearGradient>
    <filter id="softGlow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect width="760" height="240" rx="18" fill="#0d1117"/>
  <rect x="1" y="1" width="758" height="238" rx="18" fill="none" stroke="url(#border)" stroke-width="1.5" opacity="0.8"/>

  <circle cx="42" cy="42" r="8" fill="{state_color}" filter="url(#softGlow)"/>
  <text x="62" y="47" fill="#8b949e" font-family="monospace" font-size="13">PROJECT SIGNAL</text>

  <text x="42" y="88" fill="#c9d1d9" font-family="monospace" font-size="24" font-weight="700">{esc(name[:34])}</text>
  <text x="42" y="116" fill="#8b949e" font-family="monospace" font-size="13">{esc(full_name[:64])}</text>

  <text x="42" y="150" fill="#c9d1d9" font-family="system-ui, -apple-system, Segoe UI, sans-serif" font-size="15">{esc(description)}</text>

  <rect x="42" y="176" width="118" height="28" rx="14" fill="#161b22" stroke="{lang_color}" opacity="0.95"/>
  <circle cx="60" cy="190" r="5" fill="{lang_color}"/>
  <text x="74" y="195" fill="#c9d1d9" font-family="monospace" font-size="12">{esc(language[:14])}</text>

  <text x="190" y="195" fill="#8b949e" font-family="monospace" font-size="12">stars</text>
  <text x="240" y="195" fill="#00f3ff" font-family="monospace" font-size="12">{stars}</text>

  <text x="300" y="195" fill="#8b949e" font-family="monospace" font-size="12">forks</text>
  <text x="346" y="195" fill="#bc8cff" font-family="monospace" font-size="12">{forks}</text>

  <text x="402" y="195" fill="#8b949e" font-family="monospace" font-size="12">issues</text>
  <text x="456" y="195" fill="#00ff9d" font-family="monospace" font-size="12">{issues}</text>

  <text x="42" y="222" fill="#484f58" font-family="monospace" font-size="10">trace:{trace} · status:{esc(status)} · updated:{esc(updated[:20])}</text>
</svg>
'''


def build_index(repos: list[dict[str, Any]]) -> dict[str, Any]:
    items = []

    for repo in repos:
        full_name = str(repo["full_name"])
        slug = slugify(full_name)
        filename = f"{slug}.svg"

        items.append(
            {
                "full_name": full_name,
                "name": repo["name"],
                "path": f"assets/projects/{filename}",
                "html_url": repo.get("html_url"),
                "status": repo.get("status"),
                "language": repo.get("language"),
                "stars": safe_int(repo.get("stars")),
                "forks": safe_int(repo.get("forks")),
                "open_issues": safe_int(repo.get("open_issues")),
            }
        )

    return {
        "source": "scripts/generate_project_cards.py",
        "count": len(items),
        "cards": items,
    }


def remove_stale_cards(valid_filenames: set[str], dry_run: bool = False) -> None:
    if not PROJECTS_DIR.exists():
        return

    for path in sorted(PROJECTS_DIR.glob("*.svg")):
        if path.name not in valid_filenames:
            if dry_run:
                print(f"DRY-RUN: would remove stale {path.relative_to(ROOT)}")
            else:
                path.unlink()
                print(f"REMOVED: {path.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="print planned writes without mutating files")
    parser.add_argument("--limit", type=int, default=12, help="maximum cards to generate")
    args = parser.parse_args()

    repos = normalize_repositories()

    repos = sorted(
        repos,
        key=lambda item: (
            -safe_int(item.get("stars")),
            str(item.get("full_name", "")).lower(),
        ),
    )[: args.limit]

    valid_filenames: set[str] = set()

    for repo in repos:
        slug = slugify(str(repo["full_name"]))
        filename = f"{slug}.svg"
        valid_filenames.add(filename)
        write_text(PROJECTS_DIR / filename, svg_card(repo), dry_run=args.dry_run)

    remove_stale_cards(valid_filenames, dry_run=args.dry_run)

    index_payload = build_index(repos)
    write_json(INDEX_JSON, index_payload, dry_run=args.dry_run)

    print(f"SUMMARY: generated_cards={len(repos)} index={INDEX_JSON.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
