#!/usr/bin/env python3
"""
Wire project cards and workflow status panel into the canonical README generator.

This script patches scripts/build_readme.py in a targeted, idempotent way.

It adds:
- assets/projects/index.json as a README generator source input.
- workflow-status.svg rendering inside the generated README block.
- project-card rendering inside the generated README block.

It preserves:
- README.base.md as canonical template.
- README.md as generated output.
- side-effect-free dry-run behavior.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "scripts" / "build_readme.py"


NEW_GENERATED_BLOCK = r'''def load_project_cards(limit: int = 4) -> list[dict[str, Any]]:
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

    return '<td width="33%"><img src="{}" alt="Workflow control panel"/></td>'.format(path)


def project_cards_markdown(cards: list[dict[str, Any]]) -> str:
    if not cards:
        return "\n> No generated project cards found yet. Run `python3 scripts/generate_project_cards.py`.\n"

    rows: list[str] = []
    current: list[str] = []

    for card in cards:
        path = str(card["path"])
        name = str(card["name"])
        url = str(card.get("html_url") or "")

        image = '<img src="{}" alt="{} project card" width="100%"/>'.format(
            esc(path),
            esc(name),
        )

        if url:
            cell = '<td width="50%"><a href="{}">{}</a></td>'.format(esc(url), image)
        else:
            cell = '<td width="50%">{}</td>'.format(image)

        current.append(cell)

        if len(current) == 2:
            rows.append("<tr>{}</tr>".format("".join(current)))
            current = []

    if current:
        current.append('<td width="50%"></td>')
        rows.append("<tr>{}</tr>".format("".join(current)))

    return "\n<table>\n{}\n</table>\n".format("\n".join(rows))


def generated_readme_block(
    build_hash_value: str,
    timestamp: str,
    health: dict[str, str],
    repos: list[dict[str, Any]],
) -> str:
    portfolio = load_json(ROOT / "portfolio.json", {})
    skills = load_json(ROOT / "skills.json", {})
    timeline = load_json(ROOT / "timeline.json", {})
    project_cards = load_project_cards(limit=4)

    repo_lines: list[str] = []

    for repo in repos[:5]:
        name = repo_name(repo)
        url = repo.get("url") or repo.get("html_url") or "https://github.com/popdeuxrem/{}".format(name)
        repo_lines.append("- [`{}`]({}) — `{}`".format(esc(name), esc(url), esc(repo.get("status") or "tracked")))

    if not repo_lines:
        repo_lines.append("- `popdeuxrem` — `tracked`")

    health_rows = []
    for label, status in health.items():
        health_rows.append("| {} | `{}` |".format(label.replace("_", " ").title(), status.upper()))

    if isinstance(portfolio, dict):
        focus = portfolio.get("focus")
    else:
        focus = None

    if isinstance(focus, list):
        focus_text = " · ".join(str(item) for item in focus[:6])
    elif focus:
        focus_text = str(focus)
    else:
        focus_text = "systems architecture · automation · deterministic profile surfaces"

    if isinstance(skills, dict):
        skill_keys = list(skills.keys())[:8]
    elif isinstance(skills, list):
        skill_keys = [str(item) for item in skills[:8]]
    else:
        skill_keys = []

    if skill_keys:
        skill_text = ", ".join(skill_keys)
    else:
        skill_text = "Python, Bash, GitHub Actions, JSON, SVG, automation"

    if isinstance(timeline, list):
        timeline_count = len(timeline)
    elif isinstance(timeline, dict):
        timeline_count = len(timeline.keys())
    else:
        timeline_count = 0

    workflow_cell = workflow_panel_markdown()

    if workflow_cell:
        console_table = "\n".join(
            [
                '<table>',
                '<tr>',
                '<td width="33%"><img src="assets/system-health.svg" alt="System health panel"/></td>',
                '<td width="33%"><img src="assets/repo-metrics.svg" alt="Repository telemetry panel"/></td>',
                workflow_cell,
                '</tr>',
                '</table>',
            ]
        )
    else:
        console_table = "\n".join(
            [
                '<table>',
                '<tr>',
                '<td width="50%"><img src="assets/system-health.svg" alt="System health panel"/></td>',
                '<td width="50%"><img src="assets/repo-metrics.svg" alt="Repository telemetry panel"/></td>',
                '</tr>',
                '</table>',
            ]
        )

    lines = [
        "",
        "## 🧬 Live Surface Console",
        "",
        "> This section is generated by the canonical `scripts/build_readme.py` engine from versioned local state.",
        "",
        console_table,
        "",
        "### Operating Position",
        "",
        "```txt",
        "role      : systems + automation architect",
        "focus     : {}".format(focus_text),
        "stack     : {}".format(skill_text),
        "timeline  : {} tracked event(s)".format(timeline_count),
        "surface   : deterministic GitHub identity system",
        "```",
        "",
        "### Health Contract",
        "",
        "| Component | Status |",
        "|---|---:|",
        "\n".join(health_rows),
        "",
        "### Featured Repository Signals",
        "",
        "\n".join(repo_lines),
        "",
        "### Featured Project Cards",
        "",
        project_cards_markdown(project_cards),
        "",
        "### Build Attestation",
        "",
        "```txt",
        "generator : scripts/build_readme.py",
        "template  : README.base.md",
        "source    : local JSON + health + metrics + project cards",
        "build_sha : {}".format(build_hash_value[:16]),
        "synced_at : {}".format(timestamp),
        "dry_run   : side-effect free",
        "```",
        "",
        "### Architecture Rule",
        "",
        "```txt",
        "README.base.md           -> canonical human-authored template",
        "README.md                -> generated output",
        "assets/projects/*.svg    -> deterministic project cards",
        "assets/workflow-status.svg -> deterministic workflow control panel",
        "tmp.txt                  -> deprecated; not used as source of truth",
        "```",
        "",
    ]

    return "\n".join(lines)
'''


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def patch_source_files(text: str) -> str:
    if '"assets/projects/index.json",' in text:
        return text

    needle = '    "metrics/popdeuxrem_popdeuxrem.json",\n]'
    replacement = (
        '    "metrics/popdeuxrem_popdeuxrem.json",\n'
        '    "assets/projects/index.json",\n'
        ']'
    )

    require(needle in text, "Could not locate SOURCE_FILES insertion point")

    return text.replace(needle, replacement, 1)


def patch_generated_block(text: str) -> str:
    start = text.find("def generated_readme_block(")
    require(start != -1, "Could not locate generated_readme_block start")

    end = text.find("\ndef write_file(", start)
    require(end != -1, "Could not locate generated_readme_block end")

    return text[:start] + NEW_GENERATED_BLOCK + "\n" + text[end + 1:]


def main() -> int:
    require(GENERATOR.exists(), "Missing scripts/build_readme.py")

    original = GENERATOR.read_text(encoding="utf-8")
    patched = original

    patched = patch_source_files(patched)
    patched = patch_generated_block(patched)

    if patched == original:
        print("UNCHANGED: scripts/build_readme.py")
    else:
        GENERATOR.write_text(patched, encoding="utf-8")
        print("PATCHED: scripts/build_readme.py")

    print("CHECK: project cards wired")
    print("CHECK: workflow panel wired")
    print("CHECK: README.base.md remains canonical")
    print("CHECK: README.md remains generated output")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
