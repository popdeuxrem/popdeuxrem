#!/usr/bin/env python3
"""
Lysergic GitHub Surface Engine

Canonical deterministic README/profile surface generator.

Rules:
- README.base.md is canonical.
- README.md is generated.
- removed legacy tmp README artifact is deprecated.
- --dry-run writes nothing.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
DIST = ROOT / "dist"

README_BASE = ROOT / "README.base.md"
README_OUT = ROOT / "README.md"

AUTO_START = "<!-- AUTO-GENERATED:START -->"
AUTO_END = "<!-- AUTO-GENERATED:END -->"

SOURCE_FILES = [
    "README.base.md",
    "portfolio.json",
    "skills.json",
    "timeline.json",
    "data/quotes.json",
    "identity/repos.json",
    "health/status.json",
    "health/system_health.json",
    "health/orchestrator.json",
    "metrics/aggregate.json",
    "metrics/metrics.json",
    "metrics/popdeuxrem_popdeuxrem.json",
    "assets/projects/index.json",
]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def read_text(path: Path, default: str = "") -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return default


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit("Invalid JSON: {}: {}".format(path.relative_to(ROOT), exc)) from exc


def stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def file_sha256(path: Path) -> str:
    if not path.exists():
        return "missing"
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect_source_state() -> dict[str, str]:
    state: dict[str, str] = {}
    for rel in SOURCE_FILES:
        state[rel] = file_sha256(ROOT / rel)
    return state


def source_hash(state: dict[str, str]) -> str:
    return hashlib.sha256(stable_json(state).encode("utf-8")).hexdigest()


def validate_json_files() -> None:
    for rel in SOURCE_FILES:
        path = ROOT / rel
        if path.suffix == ".json" and path.exists():
            load_json(path, {})


def require_template() -> str:
    template = read_text(README_BASE)

    if not template:
        raise SystemExit("Missing README.base.md")

    if AUTO_START not in template or AUTO_END not in template:
        raise SystemExit(
            "README.base.md must contain:\n{}\n{}".format(AUTO_START, AUTO_END)
        )

    if template.index(AUTO_START) > template.index(AUTO_END):
        raise SystemExit("README.base.md AUTO-GENERATED markers are in the wrong order")

    return template


def replace_generated_block(template: str, generated: str) -> str:
    pattern = re.compile(
        re.escape(AUTO_START) + r".*?" + re.escape(AUTO_END),
        flags=re.DOTALL,
    )

    return pattern.sub(
        AUTO_START + "\n" + generated.rstrip() + "\n" + AUTO_END,
        template,
        count=1,
    )


def update_header_metadata(content: str, timestamp: str, short_hash: str) -> str:
    replacement = "LAST SYNC: {} | SHA: {}".format(timestamp, short_hash)

    return re.sub(
        r"LAST SYNC:\s*[0-9T:\-]+Z\s*\|\s*SHA:\s*[a-fA-F0-9]+",
        replacement,
        content,
        count=1,
    )


def load_projects() -> list[dict[str, Any]]:
    """Load canonical projects from data/projects.json."""
    projects_data = load_json(ROOT / "data/projects.json", {})
    if isinstance(projects_data, dict):
        return projects_data.get("projects", [])
    return []


def svg_panel_shell(width: int, height: int, body: str) -> str:
    """Unified SVG panel shell with consistent styling."""
    return f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img">
  <defs>
    <linearGradient id="g" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#00f3ff"/>
      <stop offset="50%" stop-color="#bc8cff"/>
      <stop offset="100%" stop-color="#00ff9d"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="100%" height="100%" rx="16" fill="#0d1117"/>
  <rect x="1" y="1" width="{width-2}" height="{height-2}" rx="16" fill="none" stroke="url(#g)" stroke-width="1.5" opacity="0.75"/>
  {body}
</svg>
"""


def status_color(status: str) -> str:
    """Return color for status."""
    status = status.lower()
    if status in {"ok", "online", "healthy", "active", "ship", "success"}:
        return "#00ff9d"
    if status in {"warn", "warning", "degraded", "build", "design"}:
        return "#d29922"
    if status in {"fail", "failed", "error", "critical"}:
        return "#ff5c8a"
    return "#8b949e"


def normalize_status(value: Any) -> str:
    text = str(value or "unknown").lower()

    if text in {"ok", "online", "healthy", "active", "success", "passing"}:
        return "ok"

    if text in {"warn", "warning", "degraded", "partial"}:
        return "warn"

    if text in {"fail", "failed", "error", "missing", "critical"}:
        return "fail"

    return "unknown"


def load_health_summary() -> dict[str, str]:
    system = load_json(ROOT / "health/system_health.json", {})
    status = load_json(ROOT / "health/status.json", {})
    orchestrator = load_json(ROOT / "health/orchestrator.json", {})

    components = {}
    if isinstance(system, dict) and isinstance(system.get("components"), dict):
        components = system["components"]

    def component(name: str) -> str:
        item = components.get(name, {})
        if isinstance(item, dict):
            return normalize_status(item.get("status"))
        return normalize_status(item)

    if isinstance(orchestrator, dict):
        orchestrator_status = normalize_status(orchestrator.get("status"))
    else:
        orchestrator_status = component("orchestrator")

    if isinstance(status, dict):
        metrics_status = normalize_status(status.get("metrics", "ok"))
        readme_status = normalize_status(status.get("readme_sync", "ok"))
    else:
        metrics_status = "ok"
        readme_status = "ok"

    return {
        "automation": component("automation"),
        "orchestrator": orchestrator_status,
        "metrics": metrics_status,
        "readme_sync": readme_status,
    }


def overall_health(health: dict[str, str]) -> str:
    values = set(health.values())

    if "fail" in values:
        return "degraded"

    if "warn" in values or "unknown" in values:
        return "watch"

    return "healthy"


def load_repo_metrics() -> list[dict[str, Any]]:
    repos_raw = load_json(ROOT / "identity/repos.json", [])
    metrics = load_json(ROOT / "metrics/metrics.json", {})
    aggregate = load_json(ROOT / "metrics/aggregate.json", {})

    repos: list[dict[str, Any]] = []

    if isinstance(repos_raw, dict):
        repos_iter = repos_raw.get("repos", [])
    else:
        repos_iter = repos_raw

    if isinstance(repos_iter, list):
        for item in repos_iter:
            if isinstance(item, str):
                repos.append({"name": item})
            elif isinstance(item, dict):
                repos.append(item)

    if not repos and isinstance(aggregate, dict):
        for key in ("repos", "repositories"):
            values = aggregate.get(key)
            if isinstance(values, list):
                for item in values:
                    if isinstance(item, dict):
                        repos.append(item)

    if isinstance(metrics, dict):
        values = metrics.get("repos") or metrics.get("repositories")
        if isinstance(values, list):
            for item in values:
                if isinstance(item, dict) and item not in repos:
                    repos.append(item)

    return repos[:8]


def repo_name(repo: dict[str, Any]) -> str:
    return str(
        repo.get("name")
        or repo.get("repo")
        or repo.get("full_name")
        or repo.get("slug")
        or "unknown"
    )


def load_quotes() -> list[str]:
    raw = load_json(ROOT / "data/quotes.json", [])
    quotes: list[str] = []

    def add_quote(item: Any) -> None:
        if isinstance(item, str):
            quotes.append(item)
        elif isinstance(item, dict):
            quote = item.get("quote") or item.get("text") or item.get("content")
            author = item.get("author")

            if quote and author:
                quotes.append("{} -- {}".format(quote, author))
            elif quote:
                quotes.append(str(quote))

    if isinstance(raw, list):
        for item in raw:
            add_quote(item)

    if isinstance(raw, dict):
        values = raw.get("quotes") or raw.get("items") or []
        if isinstance(values, list):
            for item in values:
                add_quote(item)

    if not quotes:
        quotes = [
            "Determinism over convenience.",
            "Observability over opacity.",
            "Rollback over regret.",
            "Artifacts over sketches.",
        ]

    return quotes


def deterministic_quote(quotes: list[str], seed: str) -> str:
    index = int(hashlib.sha256(seed.encode("utf-8")).hexdigest(), 16) % len(quotes)
    return quotes[index]


def seed_int(seed: str, namespace: str, modulo: int, offset: int = 0) -> int:
    digest = hashlib.sha256("{}::{}".format(seed, namespace).encode("utf-8")).hexdigest()
    return (int(digest[:12], 16) % modulo) + offset


def svg_shell(width: int, height: int, body: str) -> str:
    return """<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img">
  <defs>
    <linearGradient id="g" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#00f3ff"/>
      <stop offset="50%" stop-color="#bc8cff"/>
      <stop offset="100%" stop-color="#00ff9d"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="100%" height="100%" rx="16" fill="#0d1117"/>
  <rect x="1" y="1" width="{stroke_width}" height="{stroke_height}" rx="16" fill="none" stroke="url(#g)" stroke-width="1.5" opacity="0.75"/>
  {body}
</svg>
""".format(
        width=width,
        height=height,
        stroke_width=width - 2,
        stroke_height=height - 2,
        body=body,
    )


def generate_flow_line_svg(seed: str) -> str:
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12]

    body = """
  <path d="M30 50 C180 10, 280 90, 430 50 S680 10, 830 50" fill="none" stroke="url(#g)" stroke-width="3" filter="url(#glow)"/>
  <circle cx="30" cy="50" r="5" fill="#00f3ff"/>
  <circle cx="430" cy="50" r="5" fill="#bc8cff"/>
  <circle cx="830" cy="50" r="5" fill="#00ff9d"/>
  <text x="450" y="82" fill="#8b949e" font-family="monospace" font-size="11" text-anchor="middle">SURFACE ENGINE · TRACE {}</text>
""".format(esc(digest))

    return svg_shell(860, 100, body)


def generate_quote_svg(quote: str) -> str:
    q = quote.strip()

    if len(q) > 120:
        q = q[:117] + "..."

    body = """
  <text x="400" y="44" fill="#00f3ff" font-family="monospace" font-size="12" text-anchor="middle">QUANTUM AXIOM</text>
  <text x="400" y="86" fill="#c9d1d9" font-family="Georgia,serif" font-size="21" font-style="italic" text-anchor="middle">{}</text>
  <text x="400" y="126" fill="#8b949e" font-family="monospace" font-size="11" text-anchor="middle">deterministic quote selection · no random build drift</text>
""".format(esc(q))

    return svg_shell(800, 150, body)


def generate_health_svg(health: dict[str, str]) -> str:
    rows = [
        ("AUTOMATION", health.get("automation", "unknown")),
        ("ORCHESTRATOR", health.get("orchestrator", "unknown")),
        ("METRICS", health.get("metrics", "unknown")),
        ("README SYNC", health.get("readme_sync", "unknown")),
    ]

    row_svg: list[str] = []
    y = 64

    for label, status in rows:
        color = {
            "ok": "#00ff9d",
            "warn": "#d29922",
            "fail": "#ff5c8a",
        }.get(status, "#8b949e")

        row_svg.append(
            '<text x="52" y="{y}" fill="#8b949e" font-family="monospace" font-size="13">{label}</text>'
            '<circle cx="310" cy="{dot_y}" r="5" fill="{color}"/>'
            '<text x="328" y="{y}" fill="{color}" font-family="monospace" font-size="13">{status}</text>'.format(
                y=y,
                dot_y=y - 4,
                color=color,
                label=esc(label),
                status=esc(status.upper()),
            )
        )

        y += 34

    body = """
  <text x="52" y="34" fill="#00f3ff" font-family="monospace" font-size="14" font-weight="700">SYSTEM HEALTH</text>
  {}
  <text x="52" y="214" fill="#8b949e" font-family="monospace" font-size="11">overall · {}</text>
""".format(
        "".join(row_svg),
        esc(overall_health(health).upper()),
    )

    return svg_shell(430, 240, body)


def generate_system_matrix_svg(seed: str) -> str:
    cpu = seed_int(seed, "system-matrix.cpu", 72, 8)
    ram = seed_int(seed, "system-matrix.ram", 58, 24)
    io = seed_int(seed, "system-matrix.io", 82, 7)
    latency = seed_int(seed, "system-matrix.latency", 34, 9)
    packets = seed_int(seed, "system-matrix.packets", 900, 100)
    trace = hashlib.sha256(("system-matrix::" + seed).encode("utf-8")).hexdigest()[:12]

    cpu_width = max(12, int(cpu * 2.35))
    ram_width = max(12, int(ram * 2.35))
    io_width = max(12, int(io * 2.35))

    net_state = "SECURE"
    drift_state = "LOCKED"
    policy_state = "STRICT"

    body = """
  <text x="42" y="34" fill="#00f3ff" font-family="monospace" font-size="14" font-weight="700">SYSTEM STATUS MATRIX</text>
  <text x="328" y="34" fill="#8b949e" font-family="monospace" font-size="10">TRACE {trace}</text>

  <text x="42" y="70" fill="#8b949e" font-family="monospace" font-size="12">CPU</text>
  <rect x="104" y="58" width="235" height="12" rx="6" fill="#161b22"/>
  <rect x="104" y="58" width="{cpu_width}" height="12" rx="6" fill="#00f3ff" opacity="0.92" filter="url(#glow)"/>
  <text x="366" y="70" fill="#00f3ff" font-family="monospace" font-size="12">{cpu}%</text>

  <text x="42" y="104" fill="#8b949e" font-family="monospace" font-size="12">RAM</text>
  <rect x="104" y="92" width="235" height="12" rx="6" fill="#161b22"/>
  <rect x="104" y="92" width="{ram_width}" height="12" rx="6" fill="#bc8cff" opacity="0.92" filter="url(#glow)"/>
  <text x="366" y="104" fill="#bc8cff" font-family="monospace" font-size="12">{ram}%</text>

  <text x="42" y="138" fill="#8b949e" font-family="monospace" font-size="12">I/O</text>
  <rect x="104" y="126" width="235" height="12" rx="6" fill="#161b22"/>
  <rect x="104" y="126" width="{io_width}" height="12" rx="6" fill="#00ff9d" opacity="0.92" filter="url(#glow)"/>
  <text x="366" y="138" fill="#00ff9d" font-family="monospace" font-size="12">{io}%</text>

  <line x1="42" y1="160" x2="440" y2="160" stroke="#30363d" stroke-width="1"/>

  <text x="42" y="188" fill="#8b949e" font-family="monospace" font-size="12">NET</text>
  <circle cx="106" cy="184" r="5" fill="#00ff9d" filter="url(#glow)"/>
  <text x="122" y="188" fill="#00ff9d" font-family="monospace" font-size="12">{net_state}</text>

  <text x="230" y="188" fill="#8b949e" font-family="monospace" font-size="12">RTT</text>
  <text x="278" y="188" fill="#00f3ff" font-family="monospace" font-size="12">{latency}ms</text>

  <text x="42" y="218" fill="#8b949e" font-family="monospace" font-size="12">POLICY</text>
  <text x="122" y="218" fill="#bc8cff" font-family="monospace" font-size="12">{policy_state}</text>

  <text x="230" y="218" fill="#8b949e" font-family="monospace" font-size="12">DRIFT</text>
  <text x="292" y="218" fill="#00ff9d" font-family="monospace" font-size="12">{drift_state}</text>

  <text x="42" y="246" fill="#8b949e" font-family="monospace" font-size="10">packets:{packets}/s · deterministic mock telemetry from source hash</text>
""".format(
        trace=esc(trace),
        cpu_width=cpu_width,
        ram_width=ram_width,
        io_width=io_width,
        cpu=cpu,
        ram=ram,
        io=io,
        net_state=esc(net_state),
        latency=latency,
        policy_state=esc(policy_state),
        drift_state=esc(drift_state),
        packets=packets,
    )

    return svg_shell(480, 270, body)


def generate_metrics_svg(repos: list[dict[str, Any]]) -> str:
    if not repos:
        repos = [{"name": "popdeuxrem", "status": "tracked"}]

    row_svg: list[str] = []
    y = 66

    for repo in repos[:6]:
        name = repo_name(repo)
        status = repo.get("status") or repo.get("state") or "tracked"
        stars = (
            repo.get("stars")
            or repo.get("stargazers_count")
            or repo.get("star_count")
            or "-"
        )

        row_svg.append(
            '<text x="42" y="{y}" fill="#c9d1d9" font-family="monospace" font-size="12">{name}</text>'
            '<text x="330" y="{y}" fill="#8b949e" font-family="monospace" font-size="12">stars:{stars}</text>'
            '<text x="430" y="{y}" fill="#00ff9d" font-family="monospace" font-size="12">{status}</text>'.format(
                y=y,
                name=esc(name[:32]),
                stars=esc(stars),
                status=esc(status),
            )
        )

        y += 28

    body = """
  <text x="42" y="34" fill="#bc8cff" font-family="monospace" font-size="14" font-weight="700">REPO TELEMETRY</text>
  {}
  <text x="42" y="232" fill="#8b949e" font-family="monospace" font-size="11">identity/repos.json · metrics/*.json</text>
""".format("".join(row_svg))

    return svg_shell(560, 260, body)


def load_project_cards(limit: int = 4) -> list[dict[str, Any]]:
    index_path = ROOT / "assets" / "projects" / "index.json"
    payload = load_json(index_path, {})

    if not isinstance(payload, dict):
        return []

    cards = payload.get("cards", [])

    if not isinstance(cards, list):
        return []

    normalized: list[dict[str, Any]] = []

    for item in cards:
        if not isinstance(item, dict):
            continue

        path = str(item.get("path") or "").strip()

        if not path:
            continue

        if not (ROOT / path).exists():
            continue

        normalized.append(
            {
                "full_name": str(item.get("full_name") or item.get("name") or "unknown"),
                "name": str(item.get("name") or item.get("full_name") or "unknown"),
                "path": path,
                "html_url": str(item.get("html_url") or ""),
                "status": str(item.get("status") or "tracked"),
                "language": str(item.get("language") or "Unknown"),
                "stars": item.get("stars") or 0,
                "forks": item.get("forks") or 0,
                "open_issues": item.get("open_issues") or 0,
            }
        )

    return normalized[:limit]


def workflow_panel_markdown() -> str:
    path = "assets/workflow-status.svg"

    if not (ROOT / path).exists():
        return ""

    return '<td width="100%"><img src="{}" alt="Workflow control panel"/></td>'.format(path)


def project_cards_markdown(cards: list[dict[str, Any]]) -> str:
    if not cards:
        return "\n> No generated project cards found yet. Run `python3 scripts/generate_project_cards.py`.\n"

    rows: list[str] = []

    for card in cards:
        path = str(card["path"])
        name = str(card["name"])
        url = str(card.get("html_url") or "")

        image = '<img src="{}" alt="{} project card" width="100%"/>'.format(
            esc(path),
            esc(name),
        )

        if url:
            rows.append('<tr><td width="100%"><a href="{}">{}</a></td></tr>'.format(esc(url), image))
        else:
            rows.append('<tr><td width="100%">{}</td></tr>'.format(image))

    return "\n<table>\n{}\n</table>\n".format("\n".join(rows))


def generated_readme_block(
    build_hash_value: str,
    timestamp: str,
    health: dict[str, str],
    repos: list[dict[str, Any]],
) -> str:
    project_cards = load_project_cards(limit=4)

    workflow_exists = (ROOT / "assets" / "workflow-status.svg").exists()

    panel_lines = [
        "",
        "<p align=\"center\">",
        "  <img src=\"assets/system-health.svg\" width=\"92%\" alt=\"System health\"/>",
        "</p>",
        "",
        "<p align=\"center\">",
        "  <img src=\"assets/repo-metrics.svg\" width=\"92%\" alt=\"Repository metrics\"/>",
        "</p>",
        "",
        "<p align=\"center\">",
        "  <img src=\"assets/system-matrix.svg\" width=\"92%\" alt=\"System matrix\"/>",
        "</p>",
    ]

    if workflow_exists:
        panel_lines.extend([
            "",
            "<p align=\"center\">",
            "  <img src=\"assets/workflow-status.svg\" width=\"92%\" alt=\"Workflow status\"/>",
            "</p>",
        ])

    panel_lines.extend([
        "",
        "<p align=\"center\">",
        "  <code>surface=v15.1 · deterministic · operational</code>",
        "</p>",
        "",
    ])

    lines = [
        "",
        "## 🧬 Live Surface Console",
        "",
    ] + panel_lines

    return "\n".join(lines)


def project_cards_manifest() -> dict[str, Any]:
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


def write_file(path: Path, content: str, dry_run: bool, outputs: list[str]) -> None:
    rel = str(path.relative_to(ROOT))
    outputs.append(rel)

    if dry_run:
        print("DRY-RUN: would write {}".format(rel))
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print("WROTE: {}".format(rel))


def build(dry_run: bool = False, check: bool = False) -> int:
    validate_json_files()
    template = require_template()

    source_state = collect_source_state()
    shash = source_hash(source_state)
    timestamp = utc_now()

    health = load_health_summary()
    repos = load_repo_metrics()
    quotes = load_quotes()
    quote = deterministic_quote(quotes, shash)

    generated = generated_readme_block(shash, timestamp, health, repos)
    readme = replace_generated_block(template, generated)
    readme = update_header_metadata(readme, timestamp, shash[:16])

    outputs: list[str] = []

    write_file(ASSETS / "flow-line.svg", generate_flow_line_svg(shash), dry_run, outputs)
    write_file(ASSETS / "section_quote.svg", generate_quote_svg(quote), dry_run, outputs)
    write_file(ASSETS / "system-health.svg", generate_health_svg(health), dry_run, outputs)
    write_file(ASSETS / "system-matrix.svg", generate_system_matrix_svg(shash), dry_run, outputs)
    write_file(ASSETS / "repo-metrics.svg", generate_metrics_svg(repos), dry_run, outputs)
    write_file(README_OUT, readme, dry_run, outputs)

    cards_manifest = project_cards_manifest()

    manifest = {
        "engine": "Lysergic GitHub Surface Engine",
        "generator": "scripts/build_readme.py",
        "template": "README.base.md",
        "timestamp": timestamp,
        "source_hash": shash,
        "short_sha": shash[:16],
        "outputs": outputs,
        "project_cards_index": "assets/projects/index.json",
        "project_cards_count": cards_manifest["count"],
        "project_cards": cards_manifest["cards"],
        "source_files": source_state,
        "status": "success",
    }

    write_file(
        DIST / "build-manifest.json",
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        dry_run,
        outputs,
    )

    if check:
        print("CHECK: template markers valid")
        print("CHECK: JSON files valid")
        if dry_run:
            print("CHECK: dry-run side effects disabled")
        else:
            print("CHECK: generation completed")
        print("CHECK: source hash {}".format(shash[:16]))

    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="validate without mutating files")
    parser.add_argument("--check", action="store_true", help="print validation checks")
    args = parser.parse_args()

    return build(dry_run=args.dry_run, check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())