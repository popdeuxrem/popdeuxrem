#!/usr/bin/env python3
"""
Deterministic GitHub Pages surface generator.
Generates index.html from canonical data/projects.json.
No external dependencies. Pure stdlib.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
PROJECTS_JSON = ROOT / "data" / "projects.json"
METRICS_JSON = ROOT / "metrics" / "github_telemetry.json"
OUTPUT_HTML = ROOT / "index.html"

STATUS_COLORS = {
    "SHIP": ("rgba(74, 222, 128, 0.15)", "#4ade80"),
    "BUILD": ("rgba(245, 158, 11, 0.15)", "#f59e0b"),
    "DESIGN": ("rgba(168, 85, 247, 0.15)", "#a855f7"),
    "ARCHIVE": ("rgba(148, 163, 184, 0.15)", "#94a3b8"),
    "EXPERIMENTAL": ("rgba(34, 211, 238, 0.15)", "#22d3ee"),
}


def load_projects() -> list[dict[str, Any]]:
    if not PROJECTS_JSON.exists():
        return []
    data = json.loads(PROJECTS_JSON.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return data.get("projects", [])
    if isinstance(data, list):
        return data
    return []


def load_telemetry() -> dict[str, Any]:
    if not METRICS_JSON.exists():
        return {}
    return json.loads(METRICS_JSON.read_text(encoding="utf-8"))


def deterministic_seed(project: dict[str, Any]) -> int:
    """Generate deterministic animation delay from project data."""
    seed = hashlib.sha256(json.dumps(project, sort_keys=True).encode()).hexdigest()[:8]
    return int(seed, 16) % 256


def generate_badge_class(status: str) -> str:
    return f"badge-{status.lower()}"


def generate_html(projects: list[dict[str, Any]], telemetry: dict[str, Any]) -> str:
    # Sort projects alphabetically for deterministic output
    projects = sorted(projects, key=lambda p: str(p.get("id", "")).lower())
    
    telemetry_map = {t["id"]: t for t in telemetry.get("projects", []) if isinstance(t, dict)}

    cards_html = []
    for i, project in enumerate(projects):
        t = telemetry_map.get(project.get("id", ""), {})
        live_stars = t.get("stars", project.get("stars", 0))

        card = f'''      <a class="sys-card" data-id="{project.get("id", "")}" href="{project.get("repo", "#")}" target="_blank" rel="noopener noreferrer">
        <div class="sys-card-top">
          <p class="sys-name">{project.get("name", "Unknown")}</p>
          <span class="sys-status status-{project.get("status", "DESIGN")}">{project.get("status", "DESIGN")}</span>
        </div>
        <div class="sys-domain">{project.get("domain", "Unknown")}</div>
        <p class="sys-desc">{project.get("description", "")}</p>
        <div class="sys-footer">
          <span class="sys-stars"><span>★</span> {live_stars}</span>
          <span class="sys-link">Repository →</span>
        </div>
      </a>'''
        cards_html.append(card)

    cards_joined = "\n".join(cards_html)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>◆ Deployed Systems | Lysergic Infrastructure</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      background: #0a0a0f;
      font-family: 'JetBrains Mono', monospace;
      color: #999;
      min-height: 100vh;
      padding: 3rem 1rem;
    }}
    #deployed-systems {{
      max-width: 900px;
      margin: 0 auto;
    }}
    .sys-header {{
      text-align: center;
      margin-bottom: 2.5rem;
    }}
    .sys-header h2 {{
      letter-spacing: 0.35em;
      color: #fff;
      font-size: 1.1rem;
      font-weight: normal;
    }}
    .sys-header p {{
      color: #666;
      font-size: 0.75rem;
      letter-spacing: 0.2em;
      margin-top: 0.5rem;
    }}
    .sys-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 1.25rem;
    }}
    .sys-card {{
      position: relative;
      background: #0d0d0f;
      border: 1px solid #1f1f2e;
      border-radius: 6px;
      padding: 1.5rem;
      overflow: hidden;
      opacity: 0;
      transform: translateY(24px);
      animation: cardEntrance 0.6s ease forwards;
      transition: border-color 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease;
      text-decoration: none;
      display: block;
      color: inherit;
    }}
    .sys-card:nth-child(1) {{ animation-delay: 0.05s; }}
    .sys-card:nth-child(2) {{ animation-delay: 0.15s; }}
    .sys-card:nth-child(3) {{ animation-delay: 0.25s; }}
    @keyframes cardEntrance {{ to {{ opacity:1; transform:translateY(0); }} }}
    .sys-card::before {{
      content:''; position:absolute; inset:0;
      background: var(--card-glow); opacity:0;
      transition: opacity 0.4s ease; pointer-events:none; border-radius:6px;
    }}
    .sys-card:hover::before {{ opacity:1; }}
    .sys-card:hover {{
      transform: translateY(-3px);
      border-color: var(--accent);
      box-shadow: 0 0 20px -6px var(--accent);
    }}
    .sys-card[data-id="popdeuxrem"]     {{ --accent:#b44fff; --card-glow: radial-gradient(ellipse at top left, rgba(180,79,255,0.08) 0%, transparent 70%); }}
    .sys-card[data-id="shadow-scripts"] {{ --accent:#00ffe0; --card-glow: radial-gradient(ellipse at top left, rgba(0,255,224,0.07) 0%, transparent 70%); }}
    .sys-card[data-id="lysergic-systems"]{{ --accent:#ff3cac; --card-glow: radial-gradient(ellipse at top left, rgba(255,60,172,0.08) 0%, transparent 70%); }}
    .sys-card-top {{ display:flex; align-items:center; justify-content:space-between; margin-bottom:0.75rem; }}
    .sys-name {{ font-size:0.9rem; font-weight:700; color:var(--accent); letter-spacing:0.05em; margin:0; }}
    .sys-status {{ font-size:0.6rem; font-weight:700; letter-spacing:0.15em; padding:2px 8px; border-radius:3px; text-transform:uppercase; }}
    .status-SHIP  {{ background:rgba(0,255,100,0.12); color:#00ff64; border:1px solid #00ff6440; }}
    .status-BUILD {{ background:rgba(255,160,0,0.12);  color:#ffa000; border:1px solid #ffa00040; }}
    .sys-domain {{ font-size:0.65rem; color:#444; letter-spacing:0.15em; text-transform:uppercase; margin-bottom:0.75rem; }}
    .sys-desc   {{ font-size:0.72rem; color:#888; line-height:1.65; margin:0 0 1.1rem; }}
    .sys-footer {{ display:flex; align-items:center; justify-content:space-between; border-top:1px solid #1a1a2a; padding-top:0.75rem; }}
    .sys-stars  {{ font-size:0.65rem; color:#555; letter-spacing:0.1em; }}
    .sys-stars span {{ color:#ffd700; margin-right:4px; }}
    .sys-link   {{ font-size:0.65rem; color:var(--accent); letter-spacing:0.1em; text-decoration:none; opacity:0.7; transition:opacity 0.2s; }}
    .sys-link:hover {{ opacity:1; }}
  </style>
</head>
<body>
  <!-- DEPLOYED SYSTEMS -->
  <section id="deployed-systems">
    <div class="sys-header">
      <h2>◆ Deployed Systems</h2>
      <p>Operational repositories and active build pipelines</p>
    </div>
    <div class="sys-grid">
{cards_joined}
    </div>
  </section>
</body>
</html>
'''


def main() -> int:
    projects = load_projects()
    telemetry = load_telemetry()
    html = generate_html(projects, telemetry)
    OUTPUT_HTML.write_text(html, encoding="utf-8")
    print(f"WROTE: {OUTPUT_HTML.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())