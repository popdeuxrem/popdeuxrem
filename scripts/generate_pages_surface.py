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
        seed = deterministic_seed(project)
        anim_delay = 0.05 + (i * 0.05)

        bg_color, text_color = STATUS_COLORS.get(project.get("status", "DESIGN"), ("rgba(148, 163, 184, 0.15)", "#94a3b8"))

        t = telemetry_map.get(project.get("id", ""), {})
        live_stars = t.get("stars", project.get("stars", 0))

        card = f'''      <article class="card">
        <div class="card-header">
          <span class="card-name">{project.get("name", "Unknown")}</span>
          <span class="badge {generate_badge_class(project.get("status", "DESIGN"))}">{project.get("status", "DESIGN")}</span>
        </div>
        <span class="domain">{project.get("domain", "Unknown")}</span>
        <p class="stars">✦ {live_stars}</p>
        <p class="description">{project.get("description", "")}</p>
        <a href="{project.get("repo", "#")}" class="link">Repository →</a>
      </article>'''
        cards_html.append(card)

    cards_joined = "\n".join(cards_html)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>◆ Deployed Systems | Lysergic Infrastructure</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #0a0a0f;
      color: #e2e8f0;
      min-height: 100vh;
      position: relative;
      overflow-x: hidden;
      letter-spacing: -0.01em;
      line-height: 1.6;
    }}

    .bg-effects {{
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 0;
    }}

    .bg-effects::before {{
      content: "";
      position: absolute;
      top: -20%;
      left: -10%;
      width: 120%;
      height: 140%;
      background: radial-gradient(ellipse at center, rgba(34, 211, 238, 0.03) 0%, transparent 50%);
      filter: blur(100px);
    }}

    .bg-effects::after {{
      content: "";
      position: absolute;
      bottom: -30%;
      right: -10%;
      width: 100%;
      height: 120%;
      background: radial-gradient(ellipse at center, rgba(168, 85, 247, 0.02) 0%, transparent 40%);
      filter: blur(120px);
    }}

    .noise {{
      position: fixed;
      inset: 0;
      background: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' fill='%23000' opacity='0.02'/%3E%3C/svg%3E");
      pointer-events: none;
      z-index: 1;
      opacity: 0.3;
    }}

    main {{
      position: relative;
      z-index: 2;
      max-width: 1400px;
      margin: 0 auto;
      padding: 80px 24px 120px;
    }}

    header {{
      text-align: center;
      margin-bottom: 48px;
    }}

    h1 {{
      font-size: 2.25rem;
      font-weight: 600;
      color: #e2e8f0;
      margin-bottom: 8px;
      letter-spacing: -0.02em;
    }}

    .subtitle {{
      font-size: 1rem;
      color: #94a3b8;
      margin-bottom: 24px;
    }}

    .divider {{
      width: 100%;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
      margin: 0 auto 48px;
      max-width: 400px;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 24px;
      width: 100%;
    }}

    .card {{
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 16px;
      padding: 24px;
      backdrop-filter: blur(16px);
      transition: all 0.25s ease;
      animation: fadeUp 0.6s ease both;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    .card:hover {{
      transform: translateY(-4px);
      border-color: rgba(255, 255, 255, 0.15);
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(34, 211, 238, 0.1);
    }}

    @keyframes fadeUp {{
      from {{ opacity: 0; transform: translateY(20px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    .card:nth-child(1) {{ animation-delay: 0.05s; }}
    .card:nth-child(2) {{ animation-delay: 0.1s; }}
    .card:nth-child(3) {{ animation-delay: 0.15s; }}
    .card:nth-child(4) {{ animation-delay: 0.2s; }}
    .card:nth-child(5) {{ animation-delay: 0.25s; }}

    .card-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }}

    .card-name {{
      font-size: 1.25rem;
      font-weight: 600;
      color: #e2e8f0;
    }}

    .badge {{
      padding: 4px 12px;
      border-radius: 9999px;
      font-family: monospace;
      font-size: 0.75rem;
      font-weight: 500;
    }}

    .badge-ship {{ background: rgba(74, 222, 128, 0.15); color: #4ade80; }}
    .badge-build {{ background: rgba(245, 158, 11, 0.15); color: #f59e0b; }}
    .badge-design {{ background: rgba(168, 85, 247, 0.15); color: #a855f7; }}
    .badge-archive {{ background: rgba(148, 163, 184, 0.15); color: #94a3b8; }}
    .badge-experimental {{ background: rgba(34, 211, 238, 0.15); color: #22d3ee; }}

    .domain {{
      font-family: monospace;
      font-size: 0.75rem;
      color: #94a3b8;
      background: rgba(255, 255, 255, 0.04);
      padding: 4px 10px;
      border-radius: 4px;
      display: inline-block;
    }}

    .stars {{
      font-size: 0.875rem;
      color: #94a3b8;
      margin-bottom: 4px;
    }}

    .description {{
      font-size: 0.875rem;
      color: #94a3b8;
      line-height: 1.6;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}

    .link {{
      margin-top: auto;
      text-decoration: none;
      color: #22d3ee;
      font-size: 0.875rem;
      font-weight: 500;
      position: relative;
      transition: color 0.2s ease;
    }}

    .link::after {{
      content: "";
      position: absolute;
      bottom: -2px;
      left: 0;
      width: 0;
      height: 1px;
      background: #22d3ee;
      transition: width 0.2s ease;
    }}

    .link:hover {{
      color: #67e8f9;
    }}

    .link:hover::after {{
      width: 100%;
    }}

    @media (max-width: 640px) {{
      main {{ padding: 48px 16px 80px; }}
      h1 {{ font-size: 1.75rem; }}
      .card {{ padding: 20px; }}
      .card-name {{ font-size: 1.125rem; }}
    }}

    @media (max-width: 480px) {{
      .grid {{ grid-template-columns: 1fr; }}
    }}

    @media (prefers-color-scheme: light) {{
      body {{ background: #f8fafc; color: #0f172a; }}
      .card {{ background: rgba(0, 0, 0, 0.04); border-color: rgba(0, 0, 0, 0.08); }}
      .card-name {{ color: #0f172a; }}
      .description, .subtitle, .domain, .stars {{ color: #475569; }}
      .badge {{ filter: brightness(0.95); }}
    }}
  </style>
</head>
<body>
  <div class="bg-effects"></div>
  <div class="noise"></div>

  <main>
    <header>
      <h1>◆ Deployed Systems</h1>
      <p class="subtitle">Operational repositories and active build pipelines</p>
      <div class="divider"></div>
    </header>

    <section class="grid">
{cards_joined}
    </section>
  </main>
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