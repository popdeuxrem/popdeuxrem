#!/usr/bin/env python3
"""
PopDeuxRem Quantum Surface v8.0 - README Auto-Generator
=======================================================
Deterministic README.md generation from JSON data sources.
Reads: portfolio.json, skills.json, timeline.json, data/quotes.json
Outputs: README.md + SVG assets

Usage:
    python scripts/build_readme.py [--dry-run] [--verbose]
"""

import os
import sys
import json
import random
import hashlib
import argparse
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"
DIST_DIR = BASE_DIR / "dist"


def load_json(filepath: Path) -> Any:
    """Load JSON file with error handling."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"◈ WARNING: {filepath} not found, using defaults")
        return {}
    except json.JSONDecodeError as e:
        print(f"◈ ERROR: Invalid JSON in {filepath}: {e}")
        return {}


def get_build_hash() -> str:
    """Generate deterministic hash based on date window."""
    today = datetime.datetime.now().strftime("%Y-%m-%d").encode()
    return hashlib.sha256(today).hexdigest()[:16]


def get_timestamp() -> str:
    """Get UTC timestamp in ISO format."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get_display_timestamp() -> str:
    """Get human-readable timestamp."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def write_svg(filename: str, content: str) -> None:
    """Write SVG to assets directory."""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    filepath = ASSETS_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"◈ Generated: assets/{filename}")


def generate_skills_svg(skills: List[Dict]) -> str:
    """Generate neon hexagonal skills grid SVG."""
    skills_data = skills if isinstance(skills, list) else skills.get("skills", [])

    hex_positions = []
    center_x, center_y = 350, 175
    radius = 120
    angles = [0, 60, 120, 180, 240, 300]

    for i, skill in enumerate(skills_data[:6]):
        angle_rad = angles[i % 6] * (3.14159 / 180)
        x = center_x + radius * (1 if i == 0 else 0.8) * (1 if i < 3 else -1) * (
            0.5 if i in [1, 4] else 1
        )
        if i == 0:
            x, y = center_x, center_y
        elif i in [1, 2]:
            x = center_x + 140
            y = center_y - 80 + (i - 1) * 100
        elif i in [3, 4]:
            x = center_x - 140
            y = center_y - 80 + (i - 3) * 100
        else:
            x = center_x
            y = center_y + 100
        hex_positions.append(
            {
                "name": skill.get("name", "UNKNOWN"),
                "score": skill.get("score", 50),
                "x": x,
                "y": y,
            }
        )

    hexes_svg = ""
    for i, pos in enumerate(hex_positions):
        color = (
            "#00f3ff"
            if pos["score"] >= 80
            else "#bc8cff"
            if pos["score"] >= 70
            else "#d29922"
        )
        hexes_svg += f'''
    <g transform="translate({pos["x"]}, {pos["y"]})" class="hex-{i}">
      <polygon points="0,-50 43,-25 43,25 0,50 -43,25 -43,-25" 
               fill="none" stroke="{color}" stroke-width="2" opacity="0.6">
        <animate attributeName="opacity" values="0.6;0.9;0.6" dur="{2 + i * 0.3}s" repeatCount="indefinite"/>
      </polygon>
      <polygon points="0,-45 38,-22 38,22 0,45 -38,22 -38,-22" 
               fill="#0d1117" opacity="0.8"/>
      <text x="0" y="-5" text-anchor="middle" font-family="monospace" font-size="11" fill="{color}" font-weight="bold">{pos["name"]}</text>
      <text x="0" y="15" text-anchor="middle" font-family="monospace" font-size="18" fill="{color}">{pos["score"]}%</text>
    </g>'''

    return f"""<svg width="700" height="350" viewBox="0 0 700 350" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="neon-glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#161b22"/>
    </linearGradient>
  </defs>
  
  <style>
    .bg {{ fill: #0d1117; }}
    .title {{ font-family: 'SF Mono', monospace; font-size: 14px; fill: #00f3ff; }}
    @keyframes float {{
      0%, 100% {{ transform: translateY(0); }}
      50% {{ transform: translateY(-5px); }}
    }}
    .hex-0, .hex-1, .hex-2, .hex-3, .hex-4, .hex-5 {{
      animation: float 4s ease-in-out infinite;
    }}
    .hex-1 {{ animation-delay: 0.5s; }}
    .hex-2 {{ animation-delay: 1s; }}
    .hex-3 {{ animation-delay: 1.5s; }}
    .hex-4 {{ animation-delay: 2s; }}
    .hex-5 {{ animation-delay: 2.5s; }}
    @media (prefers-reduced-motion: reduce) {{
      .hex-0, .hex-1, .hex-2, .hex-3, .hex-4, .hex-5 {{ animation: none; }}
    }}
  </style>
  
  <rect class="bg" width="700" height="350"/>
  
  <text class="title" x="350" y="35" text-anchor="middle">◈ SKILL_MATRIX // NEON_GRID</text>
  <line x1="100" y1="50" x2="600" y2="50" stroke="#30363d" stroke-width="1"/>
  
  <g filter="url(#neon-glow)">
    {hexes_svg}
  </g>
  
  <text x="350" y="335" text-anchor="middle" font-family="monospace" font-size="10" fill="#8b949e">
    ▲ proficiency analysis complete // hover for details
  </text>
</svg>"""


def generate_timeline_svg(timeline: List[Dict]) -> str:
    """Generate quantum tunnel timeline SVG."""
    entries = timeline if isinstance(timeline, list) else []

    timeline_items = ""
    for i, entry in enumerate(entries):
        x_pos = 80 + i * 100
        tech = entry.get("technology", "Unknown")
        year = entry.get("year", 2020)
        color = "#00f3ff" if i == len(entries) - 1 else "#3fb950"
        timeline_items += f'''
    <g class="timeline-node-{i}" opacity="0">
      <circle cx="{x_pos}" cy="120" r="12" fill="{color}" filter="url(#glow)">
        <animate attributeName="r" values="12;14;12" dur="2s" repeatCount="indefinite" begin="{i * 0.3}s"/>
      </circle>
      <line x1="{x_pos}" y1="132" x2="{x_pos}" y2="180" stroke="{color}" stroke-width="2" stroke-dasharray="4,2"/>
      <text x="{x_pos}" y="200" text-anchor="middle" font-family="monospace" font-size="12" fill="{color}">{year}</text>
      <text x="{x_pos}" y="220" text-anchor="middle" font-family="monospace" font-size="10" fill="#e6edf3">{tech}</text>
      <animate attributeName="opacity" values="0;1" dur="0.5s" fill="freeze" begin="{i * 0.2}s"/>
    </g>'''

    return f"""<svg width="800" height="280" viewBox="0 0 800 280" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <linearGradient id="tunnel-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="50%" stop-color="#161b22"/>
      <stop offset="100%" stop-color="#0d1117"/>
    </linearGradient>
  </defs>
  
  <style>
    .bg {{ fill: #0d1117; }}
    @media (prefers-reduced-motion: reduce) {{
      .timeline-node-0, .timeline-node-1, .timeline-node-2, .timeline-node-3, .timeline-node-4, .timeline-node-5 {{
        animation: none; opacity: 1;
      }}
    }}
  </style>
  
  <rect class="bg" width="800" height="280"/>
  
  <text x="400" y="40" text-anchor="middle" font-family="monospace" font-size="14" fill="#00f3ff">
    ◈ TIMELINE_EVOLUTION // QUANTUM_TUNNEL
  </text>
  <line x1="60" y1="55" x2="740" y2="55" stroke="#30363d" stroke-width="1"/>
  
  <g>
    <line x1="80" y1="120" x2="720" y2="120" stroke="#3fb950" stroke-width="3" stroke-linecap="round">
      <animate attributeName="stroke-dasharray" values="0,1000;640,0" dur="2s" fill="freeze"/>
    </line>
    
    {timeline_items}
  </g>
  
  <g opacity="0.3">
    <text x="400" y="260" text-anchor="middle" font-family="monospace" font-size="10" fill="#8b949e">
      ~~⟨ψ|t⟩~~  time evolution operator  ~~⟨ψ|t⟩~~
    </text>
  </g>
</svg>"""


def generate_quote_svg(quotes: List[Dict]) -> str:
    """Generate particle emanation quote SVG."""
    quote_data = (
        random.choice(quotes)
        if quotes
        else {"text": "Velocity is a vector.", "author": "Systems"}
    )
    text = quote_data.get("text", "Velocity is a vector.")
    author = quote_data.get("author", "Systems")

    particles = ""
    for i in range(20):
        x = random.randint(50, 750)
        delay = random.uniform(0, 3)
        dur = random.uniform(4, 8)
        particles += f'''
    <circle cx="{x}" cy="140" r="2" fill="#f0883e" opacity="0">
      <animate attributeName="cy" values="140;20" dur="{dur}s" repeatCount="indefinite" begin="{delay}s"/>
      <animate attributeName="opacity" values="0;0.8;0" dur="{dur}s" repeatCount="indefinite" begin="{delay}s"/>
    </circle>'''

    return f'''<svg width="800" height="150" viewBox="0 0 800 150" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="quote-blur">
      <feGaussianBlur stdDeviation="0.5"/>
    </filter>
  </defs>
  
  <style>
    .bg {{ fill: #0d1117; }}
    .quote {{ font-family: Georgia, serif; font-size: 18px; font-style: italic; fill: #e6edf3; }}
    .author {{ font-family: monospace; font-size: 11px; fill: #f0883e; }}
  </style>
  
  <rect class="bg" width="800" height="150"/>
  
  <g>
    {particles}
  </g>
  
  <line x1="80" y1="60" x2="80" y2="110" stroke="#f0883e" stroke-width="3"/>
  
  <text class="quote" x="100" y="85">
    <tspan>"{text}"</tspan>
  </text>
  
  <text class="author" x="700" y="120" text-anchor="end">— {author}</text>
  
  <text x="400" y="145" text-anchor="middle" font-family="monospace" font-size="9" fill="#30363d">
    ◈ QUANTUM_AXIOM // PARTICLE_EMANATION
  </text>
</svg>'''


def build_readme(dry_run: bool = False, verbose: bool = False) -> str:
    """Main build function - generates README.md from data sources."""

    print("=" * 60)
    print("◈ POPDEUXREM QUANTUM SURFACE v8.0 - README BUILDER")
    print("=" * 60)

    portfolio = load_json(BASE_DIR / "portfolio.json")
    skills = load_json(BASE_DIR / "skills.json")
    timeline = load_json(BASE_DIR / "timeline.json")
    quotes = load_json(DATA_DIR / "quotes.json")
    telemetry = load_json(DIST_DIR / "telemetry_data.json")
    security = load_json(DIST_DIR / "security-report.json")

    build_hash = get_build_hash()
    timestamp = get_timestamp()
    display_ts = get_display_timestamp()

    if verbose:
        print(f"◈ Build Hash: {build_hash}")
        print(f"◈ Timestamp: {timestamp}")
        print(
            f"◈ Portfolio Items: {len(portfolio) if isinstance(portfolio, list) else 0}"
        )
        print(f"◈ Skills: {len(skills.get('skills', []))}")
        print(
            f"◈ Timeline Entries: {len(timeline) if isinstance(timeline, list) else 0}"
        )

    print("\n◈ Generating SVG assets...")

    skills_list = skills.get("skills", skills) if isinstance(skills, dict) else skills
    timeline_list = timeline if isinstance(timeline, list) else []
    quotes_list = quotes if isinstance(quotes, list) else []

    write_svg("skills-neon.svg", generate_skills_svg(skills_list))
    write_svg("timeline-quantum.svg", generate_timeline_svg(timeline_list))
    write_svg("section_quote.svg", generate_quote_svg(quotes_list))

    readme_content = f"""<!--
  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║  POPDEUXREM // QUANTUM SURFACE v8.0                                       ║
  ║  AUTO-GENERATED BY build_readme.py                                        ║
  ║  LAST SYNC: {timestamp} | SHA: {build_hash[:16]}                ║
  ╚═══════════════════════════════════════════════════════════════════════════╝
 -->

<div align="center">

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 1: HERO BANNER
     ═══════════════════════════════════════════════════════════════════════════ -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero_banner.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/hero_banner.svg">
  <img src="assets/hero_banner.svg" width="1000" alt="PopDeuxRem Banner"/>
</picture>

<br/>

<a name="header"></a>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/section_hero.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/section_hero.svg">
  <img src="assets/section_hero.svg" width="1000" alt="PopDeuxRem Identity Surface">
</picture>

<br/>

<img src="https://readme-typing-svg.herokuapp.com?font=Playfair+Display&weight=600&size=26&duration=3000&pause=1000&color=00F3FF&center=true&vCenter=true&repeat=true&width=600&lines=Full+Stack+Engineer;Engineered+Clarity;Tech+Innovator;Open+Source+Enthusiast;Auditable+Systems;Composable+By+Design;Problem+Solver;+%F0%9D%95%B1%F0%9D%96%86%F0%9D%96%87%F0%9D%96%8A%F0%9D%96%97%F0%9D%96%86%F0%9D%96%93%F0%9D%96%99" alt="Typing"/>

<br/>

<img src="https://komarev.com/ghpvc/?username=popdeuxrem&label=VIEWS&color=00f3ff&style=flat-square&labelColor=0d1117" alt="Views"/>

<br/>

**ꛎꔪ𖣠ꚶ𖢧 𖢑𖤢**

<img src="assets/divider_quantum.svg" width="1000" alt="Divider"/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 5: ABOUT ME
     ═══════════════════════════════════════════════════════════════════════════ -->

## ꛎꔪ𖣠ꚶ𖢧 𖢑𖤢

> I design and ship systems that prioritize **determinism**, **observability**,  
> and **long-term maintainability**.  
>  
> My work lives at the intersection of **architecture**, **automation**,  
> and **interface-level control**

<img src="assets/divider_circuit.svg" width="1000" alt="Divider"/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 6: QUANTUM TERMINAL
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="terminal"></a>

### ◈ QUANTUM_TERMINAL // LIVE_SNAPSHOT

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/terminal-dynamic.svg">
  <img src="assets/terminal-dynamic.svg" width="820" alt="PopDeuxRem Dynamic Terminal">
</picture>

<br/>

```markdown
⟁ PRIMARY FOCUS

Systems Architecture - Composable, reversible designs that survive scale.
Automation Pipelines that remove human fragility.
Product Infrastructure - Complex logic made operable.
```

<img src="assets/divider_stream.svg" width="1000" alt="Divider"/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 7: PROXY MESH
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="proxy"></a>

### ◈ PROXY_MESH :: FEATURED_ARTIFACT

<div align="center">

<a href="https://github.com/popdeuxrem/shadow-scripts">
  <img src="https://img.shields.io/badge/SHADOW--SCRIPTS-SECOPS_SHIP-00f3ff?style=for-the-badge&logo=github&logoColor=00f3ff&labelColor=0d1117&color=0d1117" alt="shadow-scripts"/>
</a>
<img src="https://img.shields.io/github/stars/popdeuxrem/shadow-scripts?style=for-the-badge&color=d29922&labelColor=0d1117" alt="stars"/>
<img src="https://img.shields.io/badge/STATUS-SHIP-d29922?style=for-the-badge&labelColor=0d1117" alt="status"/>

</div>

> **Proxy meshes, DNS overlays, stealth routing, iOS Shortcuts operators, n8n/Docker pipelines.**

<a name="shadow"></a>

<details>
<summary><b>◈ SHADOW_CORE // EXPAND_OPERATIONAL_PHILOSOPHY</b></summary>

<br/>

```
    ╔══════════════════════════════════════════════════════════════╗
    ║  ▓▓▓  POPDEUXREM OPERATIONAL MANIFEST v2.0  ▓▓▓              ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  [OPERATOR_ID]     :: POPDEUXREM                             ║
    ║  [CLEARANCE]       :: PRINCIPAL // SYS_ADMIN                 ║
    ║  [OPERATIONAL_MODE]:: QUANTUM_STEALTH                        ║
    ║  [PRIMARY_DIRECTIVE]:: COMPOSABLE + REVERSIBLE + AUDITABLE   ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  CORE AXIOMS:                                                ║
    ║  ▸ Determinism first                                         ║
    ║  ▸ Observability is currency                                 ║
    ║  ▸ iOS automation (Shortcuts/Scriptable) eliminates toil     ║
    ║  ▸ Proxy meshes + shadow routing for infrastructure hardening║
    ║  ▸ Every system is reversible and auditable                  ║
    ╚══════════════════════════════════════════════════════════════╝
```

**OPERATIONAL MODE:**
> Building quantum-grade infrastructure that fails gracefully, scales infinitely, tells you when it's unhappy. Complexity is debt. Observability is currency. iOS-first automation + proxy engineering.

</details>

<img src="assets/divider_mesh.svg" width="1000" alt="Divider"/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 8: TECH STACK
     ═══════════════════════════════════════════════════════════════════════════ -->

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 28px; max-width: 1280px; margin: 40px auto 50px auto;">

  <div style="background:#0d1117; border:2px solid #00f3ff; border-radius:16px; padding:26px; box-shadow:0 0 35px rgba(0,243,255,0.18); transition:all .35s ease;">
    <h3 style="color:#00f3ff; margin:0 0 24px 0; text-align:center; letter-spacing:1.2px; text-shadow:0 0 12px #00f3ff;">🧰 ꛤ𖦪ꛈ𖢑ꛎ𖦪ꚲ 𖢧𖤢ꛕꛅꛘ𖣠ꚳ𖣠ꚽꚲ</h3>
    <div style="display:flex; flex-wrap:wrap; gap:9px; justify-content:center;">
      <img src="https://img.shields.io/badge/web3.js-F16822?style=for-the-badge&logo=web3.js&logoColor=white" alt="web3.js"/>
      <img src="https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E" alt="javascript"/>
      <img src="https://img.shields.io/badge/-TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript"/>
      <img src="https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB" alt="react"/>
      <img src="https://img.shields.io/badge/react_native-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB" alt="react native"/>
      <img src="https://img.shields.io/badge/Next-black?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js"/>
      <img src="https://img.shields.io/badge/remix-%23000.svg?style=for-the-badge&logo=remix&logoColor=white" alt="remix"/>
      <img src="https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="tailwindcss"/>
      <img src="https://img.shields.io/badge/redux-%23593d88.svg?style=for-the-badge&logo=redux&logoColor=white" alt="redux"/>
      <img src="https://img.shields.io/badge/-React%20Query-FF4154?style=for-the-badge&logo=react%20query&logoColor=white" alt="React Query"/>
      <img src="https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white" alt="vite"/>
      <img src="https://img.shields.io/badge/Swift-F05138?style=for-the-badge&logo=swift&logoColor=white" alt="Swift"/>
      <img src="https://img.shields.io/badge/iOS%20Shortcuts-000000?style=for-the-badge&logo=apple&logoColor=white" alt="iOS Shortcuts"/>
    </div>
  </div>

  <div style="background:#0d1117; border:2px solid #bc8cff; border-radius:16px; padding:26px; box-shadow:0 0 35px rgba(188,140,255,0.18); transition:all .35s ease;">
    <h3 style="color:#bc8cff; margin:0 0 24px 0; text-align:center; letter-spacing:1.2px; text-shadow:0 0 12px #bc8cff;">⚙️ ꕷ𖤢ꛕ𖣠ꛘ𖤀ꛎ𖦪ꚲ 𖢧𖤢ꛕꛅꛘ𖣠ꚳ𖣠ꚽꚲ</h3>
    <div style="display:flex; flex-wrap:wrap; gap:9px; justify-content:center;">
      <img src="https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white" alt="NodeJS"/>
      <img src="https://img.shields.io/badge/nestjs-%23E0234E.svg?style=for-the-badge&logo=nestjs&logoColor=white" alt="NestJS"/>
      <img src="https://img.shields.io/badge/fastify-%23000000.svg?style=for-the-badge&logo=fastify&logoColor=white" alt="Fastify"/>
      <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python"/>
      <img src="https://img.shields.io/badge/-GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white" alt="GraphQL"/>
      <img src="https://img.shields.io/badge/Flutter-%2302569B.svg?style=for-the-badge&logo=Flutter&logoColor=white" alt="Flutter"/>
      <img src="https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="AWS"/>
      <img src="https://img.shields.io/badge/firebase-%23039BE5.svg?style=for-the-badge&logo=firebase&logoColor=white" alt="Firebase"/>
      <img src="https://img.shields.io/badge/n8n-EA4B71?style=for-the-badge&logo=n8n&logoColor=white" alt="n8n"/>
      <img src="https://img.shields.io/badge/Pulumi-8A3391?style=for-the-badge&logo=pulumi&logoColor=white" alt="Pulumi"/>
    </div>
  </div>

  <div style="background:#0d1117; border:2px solid #00ff9d; border-radius:16px; padding:26px; box-shadow:0 0 35px rgba(0,255,157,0.18); transition:all .35s ease;">
    <h3 style="color:#00ff9d; margin:0 0 24px 0; text-align:center; letter-spacing:1.2px; text-shadow:0 0 12px #00ff9d;">🔬 𖢧𖤢𖦪𖢧ꛈꛎ𖦪ꚲ 𖢧𖤢ꛕꛅꛘ𖣠ꚳ𖣠ꚽꚲ</h3>
    <div style="display:flex; flex-wrap:wrap; gap:9px; justify-content:center;">
      <img src="https://img.shields.io/badge/-Docker-46a2f1?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
      <img src="https://img.shields.io/badge/Terraform-844FBA?style=for-the-badge&logo=terraform&logoColor=white" alt="Terraform"/>
      <img src="https://img.shields.io/badge/kubernetes-%23326CE5.svg?style=for-the-badge&logo=kubernetes&logoColor=white" alt="kubernetes"/>
      <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux"/>
      <img src="https://img.shields.io/badge/Cloudflare-F38020?style=for-the-badge&logo=Cloudflare&logoColor=white" alt="Cloudflare"/>
      <img src="https://img.shields.io/badge/-Github_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" alt="GitHub Actions"/>
      <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis"/>
      <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
      <img src="https://img.shields.io/badge/NPM-%23CB3837.svg?style=for-the-badge&logo=npm&logoColor=white" alt="NPM"/>
      <img src="https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white" alt="VS Code"/>
    </div>
  </div>

</div>

</div>

<style>
  div[style*="grid-template-columns"] > div:hover {{
    transform: translateY(-6px);
    box-shadow: 0 0 45px rgba(0,243,255,0.35) !important;
  }}
  img[src*="shields.io"] {{
    transition: all 0.25s ease;
  }}
  img[src*="shields.io"]:hover {{
    transform: scale(1.08) translateY(-2px);
    filter: brightness(1.15) drop-shadow(0 0 18px #00f3ff);
  }}
</style>

<br/><br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 9: STREAK STATS
     ═══════════════════════════════════════════════════════════════════════════ -->

<div align="center">

📈 ꚽꛈ𖢧ꛅꚶꔪ ꕷ𖢧ꛎ𖢧ꛈꕷ𖢧ꛈꛕꕷ

<br/>

<img src="https://streak-stats.demolab.com?user=popdeuxrem&theme=highcontrast&hide_border=true&background=0d1117&stroke=00f3ff&ring=00f3ff&fire=bc8cff&currStreakLabel=bc8cff" alt="Streak"/>

</div>

<img src="assets/divider_pulse.svg" width="1000" alt="Divider"/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 10: CONNECT
     ═══════════════════════════════════════════════════════════════════════════ -->

<div align="center">

🤝 ꛕ𖣠ꛘꛘ𖤢ꛕ𖢧 ꛃꛈ𖢧ꛅ 𖢑𖤢

```
╭─ Quantum Uplink Console ─╮
│ 🛰 GitHub → @popdeuxrem   │
│ ✉ DM → @d3_glitch        │
│ 📓 Lab → Quantum Lab      │
╰─ Send: context · constraints · ideal outcome ─╯
```

</div>

<img src="assets/divider_circuit.svg" width="1000" alt="Divider"/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 11: GITHUB SNAKE
     ═══════════════════════════════════════════════════════════════════════════ -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="dist/github-snake-dark.svg">
  <img src="dist/github-snake-dark.svg" width="880" alt="GitHub Snake">
</picture>

<img src="assets/divider_quantum.svg" width="1000" alt="Divider"/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 12: QUOTE
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="quote"></a>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/section_quote.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/section_quote.svg">
  <img src="assets/section_quote.svg" width="800" alt="Quantum Axiom">
</picture>

<br/>

---

<p align="center">
  🧿 Updated daily by <code>build_readme.py</code> • 🧬 Maintained by <code>𖢧ꛅ𖤢 ꚽꚳꛈ𖢧ꛕꛅ</code>
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer" alt="Footer Wave"/>
</p>

</div>
"""

    if not dry_run:
        with open(BASE_DIR / "README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        print("\n◈ README.md generated successfully")
    else:
        print("\n◈ DRY RUN - README.md not written")
        if verbose:
            print("\n" + "=" * 60)
            print("PREVIEW:")
            print("=" * 60)
            print(readme_content[:2000] + "\n... [truncated]")

    print("\n" + "=" * 60)
    print("◈ BUILD COMPLETE")
    print("=" * 60)

    return readme_content


def main():
    parser = argparse.ArgumentParser(
        description="PopDeuxRem README Auto-Generator v8.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/build_readme.py              # Generate README.md
    python scripts/build_readme.py --dry-run    # Preview without writing
    python scripts/build_readme.py --verbose    # Show detailed output
        """,
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview without writing files"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()
    build_readme(dry_run=args.dry_run, verbose=args.verbose)


if __name__ == "__main__":
    main()
