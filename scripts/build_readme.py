#!/usr/bin/env python3
"""
PopDeuxRem Quantum Surface v6.0 - README Auto-Generator
========================================================
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

try:
    from jinja2 import Template, Environment, FileSystemLoader
    JINJA_AVAILABLE = True
except ImportError:
    JINJA_AVAILABLE = False


BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"
DIST_DIR = BASE_DIR / "dist"


def load_json(filepath: Path) -> Any:
    """Load JSON file with error handling."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
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
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"◈ Generated: assets/{filename}")


def generate_skills_svg(skills: List[Dict]) -> str:
    """Generate neon hexagonal skills grid SVG."""
    skills_data = skills if isinstance(skills, list) else skills.get('skills', [])
    
    hex_positions = []
    center_x, center_y = 350, 175
    radius = 120
    angles = [0, 60, 120, 180, 240, 300]
    
    for i, skill in enumerate(skills_data[:6]):
        angle_rad = angles[i % 6] * (3.14159 / 180)
        x = center_x + radius * (1 if i == 0 else 0.8) * (1 if i < 3 else -1) * (0.5 if i in [1, 4] else 1)
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
        hex_positions.append({
            'name': skill.get('name', 'UNKNOWN'),
            'score': skill.get('score', 50),
            'x': x,
            'y': y
        })
    
    hexes_svg = ""
    for i, pos in enumerate(hex_positions):
        color = '#00f3ff' if pos['score'] >= 80 else '#bc8cff' if pos['score'] >= 70 else '#d29922'
        hexes_svg += f'''
    <g transform="translate({pos['x']}, {pos['y']})" class="hex-{i}">
      <polygon points="0,-50 43,-25 43,25 0,50 -43,25 -43,-25" 
               fill="none" stroke="{color}" stroke-width="2" opacity="0.6">
        <animate attributeName="opacity" values="0.6;0.9;0.6" dur="{2 + i * 0.3}s" repeatCount="indefinite"/>
      </polygon>
      <polygon points="0,-45 38,-22 38,22 0,45 -38,22 -38,-22" 
               fill="#0d1117" opacity="0.8"/>
      <text x="0" y="-5" text-anchor="middle" font-family="monospace" font-size="11" fill="{color}" font-weight="bold">{pos['name']}</text>
      <text x="0" y="15" text-anchor="middle" font-family="monospace" font-size="18" fill="{color}">{pos['score']}%</text>
    </g>'''
    
    return f'''<svg width="700" height="350" viewBox="0 0 700 350" xmlns="http://www.w3.org/2000/svg">
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
</svg>'''


def generate_timeline_svg(timeline: List[Dict]) -> str:
    """Generate quantum tunnel timeline SVG."""
    entries = timeline if isinstance(timeline, list) else []
    
    timeline_items = ""
    for i, entry in enumerate(entries):
        x_pos = 80 + i * 100
        tech = entry.get('technology', 'Unknown')
        year = entry.get('year', 2020)
        color = '#00f3ff' if i == len(entries) - 1 else '#3fb950'
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
    
    return f'''<svg width="800" height="280" viewBox="0 0 800 280" xmlns="http://www.w3.org/2000/svg">
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
</svg>'''


def generate_quote_svg(quotes: List[Dict]) -> str:
    """Generate particle emanation quote SVG."""
    quote_data = random.choice(quotes) if quotes else {"text": "Velocity is a vector.", "author": "Systems"}
    text = quote_data.get('text', 'Velocity is a vector.')
    author = quote_data.get('author', 'Systems')
    
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
    print("◈ POPDEUXREM QUANTUM SURFACE v6.0 - README BUILDER")
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
        print(f"◈ Portfolio Items: {len(portfolio) if isinstance(portfolio, list) else 0}")
        print(f"◈ Skills: {len(skills.get('skills', []))}")
        print(f"◈ Timeline Entries: {len(timeline) if isinstance(timeline, list) else 0}")
    
    print("\n◈ Generating SVG assets...")
    
    skills_list = skills.get('skills', skills) if isinstance(skills, dict) else skills
    timeline_list = timeline if isinstance(timeline, list) else []
    quotes_list = quotes if isinstance(quotes, list) else []
    
    write_svg("skills-neon.svg", generate_skills_svg(skills_list))
    write_svg("timeline-quantum.svg", generate_timeline_svg(timeline_list))
    write_svg("section_quote.svg", generate_quote_svg(quotes_list))
    
    readme_content = f'''<!--
  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║  POPDEUXREM // QUANTUM SURFACE v6.0                                       ║
  ║  AUTO-GENERATED BY build_readme.py - DO NOT EDIT MANUALLY                 ║
  ║  LAST SYNC: {timestamp} | SHA: {build_hash[:16]}                ║
  ╚═══════════════════════════════════════════════════════════════════════════╝
-->

<div align="center">

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 1: HEADER / IDENTITY
     Design: SVG with SMIL animations, matrix rain, scanlines, boot sequence
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="header"></a>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/section_hero.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/section_hero.svg">
  <img src="assets/section_hero.svg" width="1000" alt="PopDeuxRem Identity Surface">
</picture>

<br/><br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 2: NAVIGATION INDEX
     Design: Inline code badge with neon separators
     ═══════════════════════════════════════════════════════════════════════════ -->

<code>
<a href="#uplink">UPLINK</a> · <a href="#thesis">THESIS</a> · <a href="#shadow">SHADOW</a> · <a href="#stack">STACK</a> · <a href="#skills">SKILLS</a> · <a href="#proxy">PROXY</a> · <a href="#work">WORK</a> · <a href="#telemetry">TELEMETRY</a> · <a href="#protocol">PROTOCOL</a> · <a href="#timeline">TIMELINE</a> · <a href="#security">SECURITY</a>
</code>

<br/><br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 3: UPLINK COMMS
     Design: Raw Markdown table with inline neon badges + status indicators
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="uplink"></a>

### ◈ UPLINK_ESTABLISHED

| PROTOCOL | ENDPOINT | STATUS | LATENCY |
|:--------:|:--------:|:------:|:-------:|
| <img src="https://img.shields.io/badge/SMTP-critical?style=flat-square&color=00f3ff&labelColor=0d1117" alt="SMTP"/> | `popdeuxrem@gateway.net` | ![Active](https://img.shields.io/badge/ACTIVE-00ff88?style=flat-square) | `< 24h` |
| <img src="https://img.shields.io/badge/GPG-encrypted?style=flat-square&color=bc8cff&labelColor=0d1117" alt="GPG"/> | `0xSPECTRE_KEY` | ![Verified](https://img.shields.io/badge/VERIFIED-00f3ff?style=flat-square) | `ASYNC` |
| <img src="https://img.shields.io/badge/MATRIX-realtime?style=flat-square&color=3fb950&labelColor=0d1117" alt="MATRIX"/> | `@popdeuxrem:matrix.org` | ![Online](https://img.shields.io/badge/ONLINE-00ff88?style=flat-square) | `< 1s` |

<br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 4: QUANTUM THESIS
     Design: SVG with quantum notation, wave patterns, split-panel
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="thesis"></a>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/section_thesis.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/section_thesis.svg">
  <img src="assets/section_thesis.svg" width="800" alt="Engineering Thesis">
</picture>

<br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 5: SHADOW CORE (ABOUT)
     Design: Expandable <details> with ASCII terminal, glitch text
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="shadow"></a>

<details>
<summary><b>◈ SHADOW_CORE // EXPAND_OPERATIONAL_PHILOSOPHY</b></summary>

<br/>

```
    ╔══════════════════════════════════════════════════════════════╗
    ║  ▓▓▓  POPDEUXREM OPERATIONAL MANIFEST v2.0  ▓▓▓              ║
    ╠══════════════════════════════════════════════════════════════╣
    ║                                                              ║
    ║  [OPERATOR_ID]     :: POPDEUXREM                             ║
    ║  [CLEARANCE]       :: PRINCIPAL // SYS_ADMIN                 ║
    ║  [OPERATIONAL_MODE]:: QUANTUM_STEALTH                        ║
    ║  [PRIMARY_DIRECTIVE]:: INFRASTRUCTURE_HARDENING              ║
    ║                                                              ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  CORE AXIOMS:                                                ║
    ║  ─────────────────────────────────────────────────────────── ║
    ║  ▸ Observability is non-negotiable                           ║
    ║  ▸ Fail gracefully, recover instantly                         ║
    ║  ▸ Security through transparency, not obscurity              ║
    ║  ▸ Automation eliminates toil, creates leverage              ║
    ║  ▸ Every system tells a story — make it readable             ║
    ║                                                              ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  SPECIALIZATIONS:                                            ║
    ║  ─────────────────────────────────────────────────────────── ║
    ║  ▸ Distributed Systems Architecture                           ║
    ║  ▸ Infrastructure as Code (Terraform/Pulumi)                 ║
    ║  ▸ Cloud-Native Observability Stacks                         ║
    ║  ▸ Secure CI/CD Pipeline Engineering                         ║
    ║  ▸ AI/ML Infrastructure Orchestration                        ║
    ║                                                              ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  OPERATIONAL_STATUS: ████████████████████ 100% OPERATIONAL   ║
    ╚══════════════════════════════════════════════════════════════╝
```

**OPERATIONAL MODE:**
> Building quantum-grade infrastructure that fails gracefully, scales infinitely, 
> and tells you when it's unhappy. Complexity is debt. Observability is currency.

</details>

<br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 6: TECH STACK MATRIX
     Design: Terminal window with animated progress bars
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="stack"></a>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/section_stack.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/section_stack.svg">
  <img src="assets/section_stack.svg" width="800" alt="Operational Stack Matrix">
</picture>

<br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 7: NEON SKILLS GRID
     Design: SVG hexagonal grid with radial progress + neon glow
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="skills"></a>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/skills-neon.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/skills-neon.svg">
  <img src="assets/skills-neon.svg" width="700" alt="Neon Skills Grid">
</picture>

<br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 8: PROXY MESH (SHADOW-SCRIPTS FEATURED)
     Design: Featured project spotlight card with gradient border
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="proxy"></a>

### ◈ PROXY_MESH :: FEATURED_ARTIFACT

<div align="center">

<a href="https://github.com/Thugger069/shadow-scripts">
  <img src="https://img.shields.io/badge/SHADOW--SCRIPTS-SECOPS_SHIP-00f3ff?style=for-the-badge&logo=github&logoColor=00f3ff&labelColor=0d1117&color=0d1117" alt="shadow-scripts"/>
</a>
<img src="https://img.shields.io/github/stars/Thugger069/shadow-scripts?style=for-the-badge&color=d29922&labelColor=0d1117" alt="stars"/>
<img src="https://img.shields.io/badge/STATUS-SHIP-d29922?style=for-the-badge&labelColor=0d1117" alt="status"/>

</div>

> **Proxy meshes, DNS overlays, and stealth routing rehearsals.**
> 
> A comprehensive toolkit for network obfuscation, DNS tunneling simulations,
> and secure routing infrastructure. Built for security research and infrastructure hardening.

<br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 9: WORK / REPOS SHOWCASE
     Design: Terminal ls -la themed cards
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="work"></a>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/section_work.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/section_work.svg">
  <img src="assets/section_work.svg" width="600" alt="Work Deployments">
</picture>

<br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 10: TELEMETRY DASHBOARD
     Design: SVG dashboard with live counters, status badges
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="telemetry"></a>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/section_telemetry.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/section_telemetry.svg">
  <img src="assets/section_telemetry.svg" width="800" alt="Live Telemetry Dashboard">
</picture>

<br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 11: AGENT PROTOCOL
     Design: <pre><code> block with animated cursor
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="protocol"></a>

### ◈ AGENT_PROTOCOL

<pre><code>
<span style="color: #ff7b72;">$</span> <span style="color: #e6edf3;">cat ~/.config/popdeuxrem/agent_protocol.yaml</span>

<span style="color: #8b949e;"># ═══════════════════════════════════════════════════════════</span>
<span style="color: #00f3ff;">ROLE:</span>      <span style="color: #e6edf3;">Senior Frontend Architect & Avant-Garde UI Designer</span>
<span style="color: #00f3ff;">EXPERIENCE:</span> <span style="color: #e6edf3;">15+ years // Master of visual hierarchy, whitespace, UX</span>

<span style="color: #8b949e;"># ───────────────────────────────────────────────────────────</span>
<span style="color: #d29922;">TRIGGERS:</span>
  <span style="color: #3fb950;">ULTRATHINK</span><span style="color: #e6edf3;">: Engage deep reasoning protocol</span>
  <span style="color: #3fb950;">STANDARD</span><span style="color: #e6edf3;">: Execute immediately, zero fluff</span>

<span style="color: #8b949e;"># ───────────────────────────────────────────────────────────</span>
<span style="color: #bc8cff;">PHILOSOPHY:</span>
  <span style="color: #e6edf3;">- Anti-Generic: Reject bootstrapped layouts</span>
  <span style="color: #e6edf3;">- The "Why" Factor: Calculate purpose before placement</span>
  <span style="color: #e6edf3;">- Minimalism: Reduction is the ultimate sophistication</span>

<span style="color: #8b949e;"># ═══════════════════════════════════════════════════════════</span>
<span style="color: #ff7b72;">$</span> <span style="color: #00f3ff;">_</span><span style="animation: blink 1s infinite;">▌</span>
</code></pre>

<br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 12: TIMELINE EVOLUTION
     Design: SVG timeline with quantum tunnel effect
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="timeline"></a>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/timeline-quantum.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/timeline-quantum.svg">
  <img src="assets/timeline-quantum.svg" width="800" alt="Timeline Evolution">
</picture>

<br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 13: QUOTE OF THE VOID
     Design: SVG with particle emanation, glitch text
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="quote"></a>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/section_quote.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/section_quote.svg">
  <img src="assets/section_quote.svg" width="800" alt="Quantum Axiom">
</picture>

<br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     SECTION 14: SECURITY VAULT
     Design: Terminal log entries with timestamps, secure badge
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="security"></a>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/section_security.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/section_security.svg">
  <img src="assets/section_security.svg" width="1000" alt="Security Audit Status">
</picture>

<br/>

> [!CAUTION]
> **SECURITY HYGIENE: {security.get('hygiene', 'UNKNOWN')}** — {security.get('vulnerabilities', {}).get('high', 0)} high-severity vulnerabilities detected. Review dependency audit.

<br/><br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     FOOTER SIGNATURE
     ═══════════════════════════════════════════════════════════════════════════ -->

---

<p align="center">
  <img src="https://img.shields.io/badge/BUILD-Quantum_Surface_v6-00f3ff?style=flat-square&labelColor=0d1117" alt="Build Version"/>
  <img src="https://img.shields.io/badge/SYNC-{timestamp}-bc8cff?style=flat-square&labelColor=0d1117" alt="Last Sync"/>
  <img src="https://img.shields.io/badge/SHA-{build_hash[:16]}-3fb950?style=flat-square&labelColor=0d1117" alt="Build SHA"/>
</p>

<p align="right">
  <code>BUILD: Surface/v6 · {display_ts} · QUANTUM_INVARIANT</code>
</p>

</div>

<style>
  @keyframes blink {{
    0%, 50% {{ opacity: 1; }}
    51%, 100% {{ opacity: 0; }}
  }}
</style>
'''
    
    if not dry_run:
        with open(BASE_DIR / "README.md", 'w', encoding='utf-8') as f:
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
        description="PopDeuxRem README Auto-Generator v6.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/build_readme.py              # Generate README.md
    python scripts/build_readme.py --dry-run    # Preview without writing
    python scripts/build_readme.py --verbose    # Show detailed output
        """
    )
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    build_readme(dry_run=args.dry_run, verbose=args.verbose)


if __name__ == "__main__":
    main()