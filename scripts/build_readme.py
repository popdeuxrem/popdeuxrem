#!/usr/bin/env python3
"""
PopDeuxRem Quantum Surface v10.0 - README Auto-Generator
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


def generate_hero_orbital_svg() -> str:
    """Generate hero orbital identity SVG."""
    return """<svg width="1000" height="180" viewBox="0 0 1000 180" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="orbit-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f3ff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#00f3ff" stop-opacity="1"/>
      <stop offset="100%" stop-color="#bc8cff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="title-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00f3ff"/>
      <stop offset="50%" stop-color="#bc8cff"/>
      <stop offset="100%" stop-color="#00ff9d"/>
    </linearGradient>
    <filter id="glow-heavy" x="-100%" y="-100%" width="300%" height="300%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow-soft" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  
  <style>
    .bg { fill: #0d1117; }
    .grid { stroke: #30363d; stroke-width: 0.5; opacity: 0.3; }
    .matrix { font-family: monospace; font-size: 9px; fill: #00f3ff; opacity: 0.08; }
    .title-fancy { font-family: 'Playfair Display', 'Bodoni MT', 'Didot', 'Times New Roman', Georgia, serif; font-weight: 900; font-style: italic; font-size: 52px; letter-spacing: 6px; fill: url(#title-grad); filter: url(#glow-heavy); }
    .subtitle { font-family: 'SF Mono', 'Fira Code', monospace; font-size: 11px; letter-spacing: 4px; fill: #bc8cff; }
    .status { font-family: 'SF Mono', monospace; font-size: 9px; fill: #8b949e; }
    .orbit { fill: none; stroke-width: 1.5; opacity: 0.4; }
    .orbit-1 { stroke: #00f3ff; animation: spin-orbit 20s linear infinite; transform-origin: 500px 90px; }
    .orbit-2 { stroke: #bc8cff; animation: spin-orbit 15s linear infinite reverse; transform-origin: 500px 90px; }
    .orbit-3 { stroke: #00ff9d; animation: spin-orbit 25s linear infinite; transform-origin: 500px 90px; }
    @keyframes spin-orbit { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    .particle { fill: #00f3ff; animation: float 3s ease-in-out infinite; }
    .particle-m { fill: #bc8cff; animation: float 3s ease-in-out infinite reverse; }
    .particle-g { fill: #00ff9d; animation: float 3s ease-in-out infinite; }
    @keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
    .pulse-dot { animation: pulse-dot 2s ease-in-out infinite; }
    @keyframes pulse-dot { 0%,100% { r: 3; opacity: 1; } 50% { r: 5; opacity: 0.6; } }
    .scanline { fill: #00f3ff; opacity: 0.03; animation: scan 4s linear infinite; }
    @keyframes scan { 0% { transform: translateY(-180px); } 100% { transform: translateY(180px); } }
    .data-stream { font-family: monospace; font-size: 7px; fill: #00f3ff; opacity: 0.15; animation: stream 2s linear infinite; }
    @keyframes stream { 0% { opacity: 0.05; } 50% { opacity: 0.2; } 100% { opacity: 0.05; } }
    .reveal { opacity: 0; animation: reveal 1.5s ease-out forwards; }
    .reveal-1 { animation-delay: 0.3s; }
    .reveal-2 { animation-delay: 0.8s; }
    .reveal-3 { animation-delay: 1.3s; }
    @keyframes reveal { to { opacity: 1; } }
    @media (prefers-color-scheme: light) { .bg { fill: #f6f8fa; } .grid { stroke: #d0d7de; } .matrix { fill: #0969da; } .title-fancy { fill: #0969da; filter: none; } .subtitle { fill: #8250df; } }
    @media (prefers-reduced-motion: reduce) { .orbit, .particle, .pulse-dot, .scanline, .data-stream, .reveal { animation: none; opacity: 1; } }
  </style>
  
  <rect class="bg" width="1000" height="180"/>
  <g class="grid">
    <line x1="0" y1="30" x2="1000" y2="30"/><line x1="0" y1="60" x2="1000" y2="60"/>
    <line x1="0" y1="90" x2="1000" y2="90"/><line x1="0" y1="120" x2="1000" y2="120"/>
    <line x1="0" y1="150" x2="1000" y2="150"/>
    <line x1="100" y1="0" x2="100" y2="180"/><line x1="200" y1="0" x2="200" y2="180"/>
    <line x1="300" y1="0" x2="300" y2="180"/><line x1="400" y1="0" x2="400" y2="180"/>
    <line x1="500" y1="0" x2="500" y2="180"/><line x1="600" y1="0" x2="600" y2="180"/>
    <line x1="700" y1="0" x2="700" y2="180"/><line x1="800" y1="0" x2="800" y2="180"/>
    <line x1="900" y1="0" x2="900" y2="180"/>
  </g>
  <g class="matrix">
    <text x="20" y="25">01010010</text><text x="120" y="45">10110101</text><text x="220" y="35">01101001</text>
    <text x="320" y="55">11010010</text><text x="620" y="25">00101101</text><text x="720" y="45">10010110</text>
    <text x="820" y="35">01110011</text><text x="920" y="55">11001010</text>
  </g>
  <rect class="scanline" x="0" y="0" width="1000" height="3"/>
  <g transform="translate(500, 90)">
    <ellipse class="orbit orbit-1" cx="0" cy="0" rx="280" ry="60"/>
    <ellipse class="orbit orbit-2" cx="0" cy="0" rx="220" ry="45"/>
    <ellipse class="orbit orbit-3" cx="0" cy="0" rx="160" ry="30"/>
  </g>
  <g filter="url(#glow-soft)">
    <circle class="particle pulse-dot" cx="220" cy="90" r="3" style="animation-delay:0s"/>
    <circle class="particle-m pulse-dot" cx="280" cy="45" r="2" style="animation-delay:0.4s"/>
    <circle class="particle-g pulse-dot" cx="720" cy="135" r="2.5" style="animation-delay:0.8s"/>
    <circle class="particle pulse-dot" cx="780" cy="90" r="3" style="animation-delay:1.2s"/>
    <circle class="particle-m pulse-dot" cx="340" cy="135" r="2" style="animation-delay:1.6s"/>
    <circle class="particle-g pulse-dot" cx="660" cy="45" r="2.5" style="animation-delay:2s"/>
  </g>
  <g class="data-stream">
    <text x="50" y="100">⟁ INIT QUANTUM_FLUX</text>
    <text x="750" y="80">◉ SYNC_COMPLETE</text>
    <text x="400" y="165">⬡ PROTOCOL_STACK::LOADED</text>
  </g>
  <g class="reveal reveal-1" filter="url(#glow-heavy)">
    <text class="title-fancy" x="500" y="100" text-anchor="middle">𝓟𝓸𝓹𝓓𝓮𝓾𝔁𝓡𝓮𝓶</text>
  </g>
  <g class="reveal reveal-2">
    <text class="subtitle" x="500" y="125" text-anchor="middle">PRINCIPAL SYSTEMS ARCHITECT</text>
  </g>
  <g class="reveal reveal-3">
    <rect x="50" y="145" width="140" height="22" rx="4" fill="#0d1117" stroke="#00f3ff" stroke-width="1" opacity="0.8"/>
    <text class="status" x="60" y="160">◉ STATUS: ONLINE</text>
    <rect x="200" y="145" width="130" height="22" rx="4" fill="#0d1117" stroke="#bc8cff" stroke-width="1" opacity="0.8"/>
    <text class="status" x="210" y="160">◈ SYNC: ACTIVE</text>
    <rect x="340" y="145" width="150" height="22" rx="4" fill="#0d1117" stroke="#00ff9d" stroke-width="1" opacity="0.8"/>
    <text class="status" x="350" y="160">⬡ MODE: QUANTUM</text>
  </g>
  <g class="reveal reveal-3" transform="translate(850, 150)">
    <rect x="0" y="0" width="120" height="22" rx="4" fill="#0d1117" stroke="#30363d" stroke-width="1"/>
    <text class="status" x="10" y="15">v10.0 // surface</text>
  </g>
  <line x1="0" y1="178" x2="1000" y2="178" stroke="#30363d" stroke-width="2"/>
  <rect x="0" y="177" width="400" height="3" fill="url(#orbit-grad)">
    <animate attributeName="width" values="0;1000;0" dur="6s" repeatCount="indefinite"/>
  </rect>
</svg>"""


def generate_flow_line_svg() -> str:
    """Generate flow line divider SVG."""
    return """<svg width="1000" height="20" viewBox="0 0 1000 20" xmlns="http://www.w3.org/2000/svg">
  <style>
    .flow-line { stroke: #00f3ff; stroke-width: 1; stroke-dasharray: 8 4; animation: flow 2s linear infinite; }
    @keyframes flow { to { stroke-dashoffset: -24; } }
    @media (prefers-color-scheme: light) { .flow-line { stroke: #0969da; } }
  </style>
  <line class="flow-line" x1="0" y1="10" x2="1000" y2="10"/>
</svg>"""


def generate_uplink_console_svg() -> str:
    """Generate uplink console SVG."""
    return """<svg width="700" height="200" viewBox="0 0 700 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="uplink-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00f3ff" stop-opacity="0.3"/>
      <stop offset="50%" stop-color="#bc8cff" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#00ff9d" stop-opacity="0.3"/>
    </linearGradient>
    <filter id="uplink-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <style>
    .uplink-bg { fill: #0d1117; }
    .uplink-border { fill: none; stroke: #00f3ff; stroke-width: 2; stroke-opacity: 0.5; }
    .uplink-header { font-family: 'SF Mono', monospace; font-size: 11px; fill: #00f3ff; letter-spacing: 2px; }
    .uplink-label { font-family: 'SF Mono', monospace; font-size: 10px; fill: #8b949e; }
    .uplink-value { font-family: 'SF Mono', monospace; font-size: 12px; fill: #c9d1d9; }
    .uplink-accent { font-family: 'SF Mono', monospace; font-size: 10px; fill: #bc8cff; }
    .uplink-footer { font-family: 'SF Mono', monospace; font-size: 9px; fill: #484f58; }
    .signal { fill: #00ff9d; animation: signal-pulse 2s ease-in-out infinite; }
    @keyframes signal-pulse { 0%,100% { opacity: 0.6; r: 3; } 50% { opacity: 1; r: 4; } }
    .orbit-ring { fill: none; stroke: #00f3ff; stroke-width: 0.5; stroke-dasharray: 4 4; animation: orbit-spin 10s linear infinite; transform-origin: 350px 80px; }
    @keyframes orbit-spin { to { transform: rotate(360deg); } }
    .data-packet { fill: #00f3ff; animation: packet 3s ease-in-out infinite; }
    @keyframes packet { 0%,100% { opacity: 0.3; } 50% { opacity: 0.8; } }
    .corner-decor { fill: none; stroke: #bc8cff; stroke-width: 1; stroke-opacity: 0.4; }
    @media (prefers-color-scheme: light) { .uplink-bg { fill: #f6f8fa; } .uplink-border { stroke: #0969da; } .uplink-header { fill: #0969da; } .uplink-value { fill: #24292f; } }
    @media (prefers-reduced-motion: reduce) { .signal, .orbit-ring, .data-packet { animation: none; opacity: 0.7; } }
  </style>
  <rect class="uplink-bg" x="0" y="0" width="700" height="200" rx="8"/>
  <rect class="uplink-border" x="1" y="1" width="698" height="198" rx="8"/>
  <path class="corner-decor" d="M10,30 L10,10 L30,10"/>
  <path class="corner-decor" d="M670,10 L690,10 L690,30"/>
  <path class="corner-decor" d="M690,170 L690,190 L670,190"/>
  <path class="corner-decor" d="M30,190 L10,190 L10,170"/>
  <g transform="translate(350, 80)">
    <ellipse class="orbit-ring" cx="0" cy="0" rx="60" ry="20"/>
  </g>
  <circle class="data-packet" cx="290" cy="80" r="2" style="animation-delay:0s"/>
  <circle class="data-packet" cx="410" cy="80" r="2" style="animation-delay:1s"/>
  <circle class="data-packet" cx="350" cy="60" r="2" style="animation-delay:2s"/>
  <g filter="url(#uplink-glow)">
    <text class="uplink-header" x="350" y="30" text-anchor="middle">◈ UPLINK CONSOLE v10.0 ◈</text>
  </g>
  <g transform="translate(30, 60)">
    <circle class="signal" cx="0" cy="5" r="3"/>
    <text class="uplink-label" x="15" y="3">GITHUB</text>
    <text class="uplink-value" x="15" y="18">@popdeuxrem</text>
    <circle class="signal" cx="0" cy="45" r="3" style="animation-delay:0.5s"/>
    <text class="uplink-label" x="15" y="43">EMAIL</text>
    <text class="uplink-value" x="15" y="58">popdeuxrem@gateway.net</text>
  </g>
  <g transform="translate(350, 60)">
    <circle class="signal" cx="0" cy="5" r="3" style="animation-delay:1s"/>
    <text class="uplink-label" x="15" y="3">PROTOCOL</text>
    <text class="uplink-value" x="15" y="18">context · constraints</text>
    <circle class="signal" cx="0" cy="45" r="3" style="animation-delay:1.5s"/>
    <text class="uplink-label" x="15" y="43">IDEAL OUTCOME</text>
    <text class="uplink-accent" x="15" y="58">specify for engagement</text>
  </g>
  <line x1="30" y1="140" x2="670" y2="140" stroke="#30363d" stroke-width="1" stroke-dasharray="2 4"/>
  <g transform="translate(350, 165)">
    <text class="uplink-footer" x="0" y="0" text-anchor="middle">ꛕ𖣠ꛘꛘ𖤢ꛕ𖢧 ꛃꛈ𖢧ꛅ 𖢑𖤢 ∙ 𖢧ꛅ𖤢 ꚽꚳꛈ𖢧ꛕꛅ ∙ 🛰 CHANNEL ACTIVE</text>
  </g>
  <g transform="translate(350, 185)">
    <text class="uplink-footer" x="0" y="0" text-anchor="middle">Send transmission → await entanglement</text>
  </g>
</svg>"""


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
    """Generate quantum axiom quote SVG v10.0."""
    quote_data = (
        random.choice(quotes)
        if quotes
        else {
            "text": "Complexity is debt; simplicity is the ultimate sophistication.",
            "author": "Operator Axiom",
        }
    )
    text = quote_data.get(
        "text", "Complexity is debt; simplicity is the ultimate sophistication."
    )
    author = quote_data.get("author", "Operator Axiom")

    return f'''<svg width="800" height="140" viewBox="0 0 800 140" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="quote-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00f3ff" stop-opacity="0.1"/>
      <stop offset="50%" stop-color="#bc8cff" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#00ff9d" stop-opacity="0.1"/>
    </linearGradient>
    <filter id="quote-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  
  <style>
    .quote-bg {{ fill: #0d1117; }}
    .quote-border {{ fill: none; stroke: #30363d; stroke-width: 1; }}
    .quote-mark {{ font-family: Georgia, serif; font-size: 64px; fill: #00f3ff; opacity: 0.15; }}
    .quote-text {{ font-family: 'Playfair Display', Georgia, serif; font-size: 18px; font-style: italic; fill: #c9d1d9; }}
    .quote-accent {{ fill: #bc8cff; }}
    .quote-author {{ font-family: 'SF Mono', monospace; font-size: 11px; fill: #8b949e; letter-spacing: 2px; }}
    .quote-glyph {{ font-family: monospace; font-size: 10px; fill: #00ff9d; opacity: 0.6; }}
    
    .pulse-line {{ stroke: #00f3ff; stroke-width: 1; stroke-dasharray: 4 2; animation: pulse-line 2s ease-in-out infinite; }}
    @keyframes pulse-line {{ 0%,100% {{ opacity: 0.3; }} 50% {{ opacity: 0.7; }} }}
    
    .corner {{ fill: none; stroke: #bc8cff; stroke-width: 1; stroke-opacity: 0.3; }}
    
    @media (prefers-color-scheme: light) {{
      .quote-bg {{ fill: #f6f8fa; }}
      .quote-border {{ stroke: #d0d7de; }}
      .quote-mark {{ fill: #0969da; }}
      .quote-text {{ fill: #24292f; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .pulse-line {{ animation: none; opacity: 0.5; }}
    }}
  </style>
  
  <rect class="quote-bg" x="0" y="0" width="800" height="140" rx="8"/>
  <rect class="quote-border" x="0.5" y="0.5" width="799" height="139" rx="8"/>
  
  <path class="corner" d="M15,35 L15,15 L35,15"/>
  <path class="corner" d="M765,15 L785,15 L785,35"/>
  <path class="corner" d="M785,105 L785,125 L765,125"/>
  <path class="corner" d="M35,125 L15,125 L15,105"/>
  
  <text class="quote-mark" x="30" y="70">"</text>
  
  <g filter="url(#quote-glow)">
    <text class="quote-text" x="400" y="60" text-anchor="middle">
      <tspan>"{text}"</tspan>
    </text>
  </g>
  
  <line class="pulse-line" x1="300" y1="80" x2="500" y2="80"/>
  
  <text class="quote-author" x="400" y="100" text-anchor="middle">— 𖢧ꛅ𖤢 ꚽꚳꛈ𖢧ꛕꛅ ∙ {author}</text>
  
  <text class="quote-glyph" x="400" y="125" text-anchor="middle">ꛎꔪ𖣠ꚶ𖢧 𖢑𖤢 ∙ ◈ ∙ AXIOM v10.0</text>
  
  <text class="quote-mark" x="750" y="100">"</text>
</svg>'''


def build_readme(dry_run: bool = False, verbose: bool = False) -> str:
    """Main build function - generates README.md from data sources."""

    print("=" * 60)
    print("◈ POPDEUXREM QUANTUM SURFACE v10.0 - README BUILDER")
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

    # Generate all SVG assets
    write_svg("hero_orbital.svg", generate_hero_orbital_svg())
    write_svg("flow-line.svg", generate_flow_line_svg())
    write_svg("uplink-console.svg", generate_uplink_console_svg())
    write_svg("skills-neon.svg", generate_skills_svg(skills_list))
    write_svg("timeline-quantum.svg", generate_timeline_svg(timeline_list))
    write_svg("section_quote.svg", generate_quote_svg(quotes_list))

    readme_content = f"""<!--
  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║  POPDEUXREM // QUANTUM SURFACE v10.0                                      ║
  ║  AUTO-GENERATED BY build_readme.py                                        ║
  ║  LAST SYNC: {timestamp} | SHA: {build_hash[:16]}               ║
  ╚═══════════════════════════════════════════════════════════════════════════╝
 -->

<div align="center">

<!-- ═══════════════════════════════════════════════════════════════════════════
     HERO SURFACE v10.0 // IMMERSIVE ORBITAL IDENTITY
     ═══════════════════════════════════════════════════════════════════════════ -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero_banner.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/hero_banner.svg">
  <img src="assets/hero_banner.svg" width="1000" alt="PopDeuxRem Banner"/>
</picture>

<br/>

<a name="header"></a>

<img src="assets/hero_orbital.svg" width="1000" alt="PopDeuxRem Orbital Identity"/>
      <stop offset="50%" stop-color="#00f3ff" stop-opacity="1"/>
      <stop offset="100%" stop-color="#bc8cff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="title-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00f3ff"/>
      <stop offset="50%" stop-color="#bc8cff"/>
      <stop offset="100%" stop-color="#00ff9d"/>
    </linearGradient>
    <filter id="glow-heavy" x="-100%" y="-100%" width="300%" height="300%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow-soft" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  
  <style>
    .bg {{ fill: #0d1117; }}
    .grid {{ stroke: #30363d; stroke-width: 0.5; opacity: 0.3; }}
    .matrix {{ font-family: monospace; font-size: 9px; fill: #00f3ff; opacity: 0.08; }}
    
    .title-fancy {{ 
      font-family: 'Playfair Display', 'Bodoni MT', 'Didot', 'Times New Roman', Georgia, serif; 
      font-weight: 900; 
      font-style: italic;
      font-size: 52px; 
      letter-spacing: 6px;
      fill: url(#title-grad);
      filter: url(#glow-heavy);
    }}
    
    .subtitle {{ font-family: 'SF Mono', 'Fira Code', monospace; font-size: 11px; letter-spacing: 4px; fill: #bc8cff; }}
    .status {{ font-family: 'SF Mono', monospace; font-size: 9px; fill: #8b949e; }}
    
    .orbit {{ fill: none; stroke-width: 1.5; opacity: 0.4; }}
    .orbit-1 {{ stroke: #00f3ff; animation: spin-orbit 20s linear infinite; transform-origin: 500px 90px; }}
    .orbit-2 {{ stroke: #bc8cff; animation: spin-orbit 15s linear infinite reverse; transform-origin: 500px 90px; }}
    .orbit-3 {{ stroke: #00ff9d; animation: spin-orbit 25s linear infinite; transform-origin: 500px 90px; }}
    @keyframes spin-orbit {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
    
    .particle {{ fill: #00f3ff; animation: float 3s ease-in-out infinite; }}
    .particle-m {{ fill: #bc8cff; animation: float 3s ease-in-out infinite reverse; }}
    .particle-g {{ fill: #00ff9d; animation: float 3s ease-in-out infinite; }}
    @keyframes float {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-8px); }} }}
    
    .pulse-dot {{ animation: pulse-dot 2s ease-in-out infinite; }}
    @keyframes pulse-dot {{ 0%,100% {{ r: 3; opacity: 1; }} 50% {{ r: 5; opacity: 0.6; }} }}
    
    .scanline {{ fill: #00f3ff; opacity: 0.03; animation: scan 4s linear infinite; }}
    @keyframes scan {{ 0% {{ transform: translateY(-180px); }} 100% {{ transform: translateY(180px); }} }}
    
    .data-stream {{ font-family: monospace; font-size: 7px; fill: #00f3ff; opacity: 0.15; animation: stream 2s linear infinite; }}
    @keyframes stream {{ 0% {{ opacity: 0.05; }} 50% {{ opacity: 0.2; }} 100% {{ opacity: 0.05; }} }}
    
    .reveal {{ opacity: 0; animation: reveal 1.5s ease-out forwards; }}
    .reveal-1 {{ animation-delay: 0.3s; }}
    .reveal-2 {{ animation-delay: 0.8s; }}
    .reveal-3 {{ animation-delay: 1.3s; }}
    @keyframes reveal {{ to {{ opacity: 1; }} }}
    
    @media (prefers-color-scheme: light) {{
      .bg {{ fill: #f6f8fa; }}
      .grid {{ stroke: #d0d7de; }}
      .matrix {{ fill: #0969da; }}
      .title-fancy {{ fill: #0969da; filter: none; }}
      .subtitle {{ fill: #8250df; }}
    }}
    
    @media (prefers-reduced-motion: reduce) {{
      .orbit, .particle, .pulse-dot, .scanline, .data-stream, .reveal {{ animation: none; opacity: 1; }}
    }}
  </style>
  
  <rect class="bg" width="1000" height="180"/>
  
  <g class="grid">
    <line x1="0" y1="30" x2="1000" y2="30"/><line x1="0" y1="60" x2="1000" y2="60"/>
    <line x1="0" y1="90" x2="1000" y2="90"/><line x1="0" y1="120" x2="1000" y2="120"/>
    <line x1="0" y1="150" x2="1000" y2="150"/>
    <line x1="100" y1="0" x2="100" y2="180"/><line x1="200" y1="0" x2="200" y2="180"/>
    <line x1="300" y1="0" x2="300" y2="180"/><line x1="400" y1="0" x2="400" y2="180"/>
    <line x1="500" y1="0" x2="500" y2="180"/><line x1="600" y1="0" x2="600" y2="180"/>
    <line x1="700" y1="0" x2="700" y2="180"/><line x1="800" y1="0" x2="800" y2="180"/>
    <line x1="900" y1="0" x2="900" y2="180"/>
  </g>
  
  <g class="matrix">
    <text x="20" y="25">01010010</text><text x="120" y="45">10110101</text><text x="220" y="35">01101001</text>
    <text x="320" y="55">11010010</text><text x="620" y="25">00101101</text><text x="720" y="45">10010110</text>
    <text x="820" y="35">01110011</text><text x="920" y="55">11001010</text>
  </g>
  
  <rect class="scanline" x="0" y="0" width="1000" height="3"/>
  
  <g transform="translate(500, 90)">
    <ellipse class="orbit orbit-1" cx="0" cy="0" rx="280" ry="60"/>
    <ellipse class="orbit orbit-2" cx="0" cy="0" rx="220" ry="45"/>
    <ellipse class="orbit orbit-3" cx="0" cy="0" rx="160" ry="30"/>
  </g>
  
  <g filter="url(#glow-soft)">
    <circle class="particle pulse-dot" cx="220" cy="90" r="3" style="animation-delay:0s"/>
    <circle class="particle-m pulse-dot" cx="280" cy="45" r="2" style="animation-delay:0.4s"/>
    <circle class="particle-g pulse-dot" cx="720" cy="135" r="2.5" style="animation-delay:0.8s"/>
    <circle class="particle pulse-dot" cx="780" cy="90" r="3" style="animation-delay:1.2s"/>
    <circle class="particle-m pulse-dot" cx="340" cy="135" r="2" style="animation-delay:1.6s"/>
    <circle class="particle-g pulse-dot" cx="660" cy="45" r="2.5" style="animation-delay:2s"/>
  </g>
  
  <g class="data-stream">
    <text x="50" y="100">⟁ INIT QUANTUM_FLUX</text>
    <text x="750" y="80">◉ SYNC_COMPLETE</text>
    <text x="400" y="165">⬡ PROTOCOL_STACK::LOADED</text>
  </g>
  
  <g class="reveal reveal-1" filter="url(#glow-heavy)">
    <text class="title-fancy" x="500" y="100" text-anchor="middle">𝓟𝓸𝓹𝓓𝓮𝓾𝔁𝓡𝓮𝓶</text>
  </g>
  
  <g class="reveal reveal-2">
    <text class="subtitle" x="500" y="125" text-anchor="middle">PRINCIPAL SYSTEMS ARCHITECT</text>
  </g>
  
  <g class="reveal reveal-3">
    <rect x="50" y="145" width="140" height="22" rx="4" fill="#0d1117" stroke="#00f3ff" stroke-width="1" opacity="0.8"/>
    <text class="status" x="60" y="160">◉ STATUS: ONLINE</text>
    <rect x="200" y="145" width="130" height="22" rx="4" fill="#0d1117" stroke="#bc8cff" stroke-width="1" opacity="0.8"/>
    <text class="status" x="210" y="160">◈ SYNC: ACTIVE</text>
    <rect x="340" y="145" width="150" height="22" rx="4" fill="#0d1117" stroke="#00ff9d" stroke-width="1" opacity="0.8"/>
    <text class="status" x="350" y="160">⬡ MODE: QUANTUM</text>
  </g>
  
  <g class="reveal reveal-3" transform="translate(850, 150)">
    <rect x="0" y="0" width="120" height="22" rx="4" fill="#0d1117" stroke="#30363d" stroke-width="1"/>
    <text class="status" x="10" y="15">v10.0 // surface</text>
  </g>
  
  <line x1="0" y1="178" x2="1000" y2="178" stroke="#30363d" stroke-width="2"/>
  <rect x="0" y="177" width="400" height="3" fill="url(#orbit-grad)">
    <animate attributeName="width" values="0;1000;0" dur="6s" repeatCount="indefinite"/>
  </rect>
</svg>

<br/>

<img src="https://readme-typing-svg.herokuapp.com?font=Playfair+Display&weight=700&size=28&duration=4000&pause=1500&color=BC8CFF66&center=true&vCenter=true&repeat=true&width=700&lines=Full+Stack+Engineer;Engineered+Clarity;Tech+Innovator;Open+Source+Enthusiast;Auditable+Systems;Composable+By+Design;Problem+Solver;𝕱𝖆𝖛𝖔𝖗𝖆𝖓𝖙𝖚𝖒" alt="Typing"/>

<br/>

<img src="https://komarev.com/ghpvc/?username=popdeuxrem&label=VIEWS&color=00f3ff&style=flat-square&labelColor=0d1117" alt="Views"/>

<br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     NAVIGATION
     ═══════════════════════════════════════════════════════════════════════════ -->

<code>
<a href="#about">ABOUT</a> · <a href="#terminal">TERMINAL</a> · <a href="#stack">STACK</a> · <a href="#stats">STATS</a> · <a href="#connect">CONNECT</a>
</code>

<img src="assets/divider_quantum.svg" width="1000" alt="Divider"/>

<br/><br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     OPERATOR CORE v10.0 // LIVING JAVASCRIPT OBJECT
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="about"></a>

<div align="center">

<img src="assets/flow-line.svg" width="1000" alt="Flow"/>

</div>

### ꛎꔪ𖣠ꚶ𖢧 𖢑𖤢

```javascript
/**
 * ╔═══════════════════════════════════════════════════════════════════════════╗
 * ║  POPDEUXREM :: QUANTUM OPERATOR DEFINITION v10.0                          ║
 * ║  SYNC: {timestamp} | SHA: {build_hash[:16]}                    ║
 * ╚═══════════════════════════════════════════════════════════════════════════╝
 */

const popdeuxrem = {{
  
  identity: {{
    handle: "𖢧ꛅ𖤢 ꚽꚳꛈ𖢧ꛕꛅ",
    alias: "@d3_glitch",
    designation: "PRINCIPAL SYSTEMS ARCHITECT",
    clearance: "QUANTUM_STEALTH"
  }},
  
  coreAxioms: [
    "Determinism first — every action must be traceable and reproducible",
    "Observability is currency — systems that can't speak are already broken",
    "iOS automation (Shortcuts/Scriptable/Data Jar) eliminates operational toil",
    "Proxy meshes + shadow routing for infrastructure hardening",
    "Every system is reversible, auditable, and composable by design",
    "Complexity is debt; simplicity is the ultimate sophistication"
  ],
  
  mission: {{
    primary: "Design and ship systems that prioritize determinism, observability, and long-term maintainability",
    focus: "Architecture ∙ Automation ∙ Interface-level control",
    philosophy: "Building quantum-grade infrastructure that fails gracefully, scales infinitely, and tells you when it's unhappy"
  }},
  
  specializations: [
    {{ domain: "Systems Architecture", focus: "Composable, reversible designs that survive scale" }},
    {{ domain: "Automation Pipelines", focus: "Remove human fragility from critical workflows" }},
    {{ domain: "Product Infrastructure", focus: "Complex logic made operable and observable" }},
    {{ domain: "iOS Ecosystem", focus: "Shortcuts, Scriptable, Data Jar operators" }},
    {{ domain: "Infrastructure Hardening", focus: "Proxy meshes, DNS overlays, stealth routing" }}
  ],
  
  status: {{
    operational: "ONLINE",
    sync: "ACTIVE",
    mode: "QUANTUM",
    uptime: "∞",
    lastPing: new Date().toISOString()
  }},
  
  uplink: {{
    github: "@popdeuxrem",
    email: "popdeuxrem@gateway.net",
    protocol: "Send: context · constraints · ideal outcome"
  }},
  
  directive: "ꛤ𖦪ꛈ𖢑ꛎ𖦪ꚲ 𖢧𖤢ꛕꛅꛘ𖣠ꚳ𖣠ꚽꚲ ∙ ꕷ𖤢ꛕ𖣠ꛘ𖤀ꛎ𖦪ꚲ 𖢧𖤢ꛕꛅꛘ𖣠ꚳ𖣠ꚽꚲ ∙ 𖢧𖤢𖦪𖢧ꛈꛎ𖦪ꚲ 𖢧𖤢ꛕꛅꛘ𖣠ꚳ𖣠ꚽꚲ"
  
}};

export default popdeuxrem; // ◈ Composable. Reversible. Quantum.
```

<br/><br/>

<img src="assets/divider_circuit.svg" width="1000" alt="Divider"/>

<br/><br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     TERMINAL v10.0 // DYNAMIC SVG WITH LIVE PARTICLES
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="terminal"></a>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/terminal-dynamic.svg">
  <img src="assets/terminal-dynamic.svg" width="880" alt="PopDeuxRem Dynamic Terminal">
</picture>

<br/><br/>

<img src="assets/divider_stream.svg" width="1000" alt="Divider"/>

<br/><br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     PROXY MESH :: FEATURED ARTIFACT
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

```typescript
/**
 * ╔═══════════════════════════════════════════════════════════════════════════╗
 * ║  POPDEUXREM :: OPERATIONAL MANIFEST v10.0                                 ║
 * ║  SYNC: {timestamp} | SHA: manifest.shadow.stable                 ║
 * ╚═══════════════════════════════════════════════════════════════════════════╝
 */

interface OperatorManifest {{
  operator: {{
    id: "POPDEUXREM";
    clearance: "PRINCIPAL | SYS_ADMIN";
    mode: "QUANTUM_STEALTH";
    directive: "COMPOSABLE + REVERSIBLE + AUDITABLE";
  }};
  
  coreAxioms: [
    "Determinism first",
    "Observability is currency",
    "iOS automation (Shortcuts/Scriptable) eliminates toil",
    "Proxy meshes + shadow routing for infrastructure hardening",
    "Every system is reversible and auditable"
  ];
  
  stack: {{
    primary: ["JavaScript", "TypeScript", "React", "Node.js", "Python"];
    infrastructure: ["Docker", "Kubernetes", "Terraform", "n8n", "Pulumi"];
    automation: ["iOS Shortcuts", "Scriptable", "Data Jar", "GitHub Actions"];
    observability: ["Cloudflare", "Redis", "PostgreSQL", "AWS"];
  }};
  
  philosophy: string;
}}

const manifest: OperatorManifest = {{
  operator: {{
    id: "POPDEUXREM",
    clearance: "PRINCIPAL | SYS_ADMIN",
    mode: "QUANTUM_STEALTH",
    directive: "COMPOSABLE + REVERSIBLE + AUDITABLE"
  }},
  
  coreAxioms: [
    "Determinism first",
    "Observability is currency",
    "iOS automation (Shortcuts/Scriptable) eliminates toil",
    "Proxy meshes + shadow routing for infrastructure hardening",
    "Every system is reversible and auditable"
  ],
  
  stack: {{
    primary: ["JavaScript", "TypeScript", "React", "Node.js", "Python"],
    infrastructure: ["Docker", "Kubernetes", "Terraform", "n8n", "Pulumi"],
    automation: ["iOS Shortcuts", "Scriptable", "Data Jar", "GitHub Actions"],
    observability: ["Cloudflare", "Redis", "PostgreSQL", "AWS"]
  }},
  
  philosophy: "Building quantum-grade infrastructure that fails gracefully, scales infinitely, tells you when it's unhappy. Complexity is debt. Observability is currency."
}};

export default manifest; // ◈ Reversible. Auditable. Shadow-grade.
```

</details>

<img src="assets/divider_mesh.svg" width="1000" alt="Divider"/>

<br/><br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     TECH MATRIX v10.0 // NEON CARD GRID
     ═══════════════════════════════════════════════════════════════════════════ -->
<a name="stack"></a>
<div align="center">

### ⚡ ꛤ𖦪ꛈ𖢑ꛎ𖦪ꚲ ꕷ𖢧ꛎ𖢧ꛈꕷ𖢧ꛈꛕꕷ

<br/>

<table>
<tr>
<td valign="top" width="33%">

<h3 align="center">🧰 ꛤ𖦪ꛈ𖢑ꛎ𖦪ꚲ 𖢧𖤢ꛕꛅꛘ𖣠ꚳ𖣠ꚽꚲ</h3>
<p align="center">
<img src="https://img.shields.io/badge/web3.js-F16822?style=flat-square&logo=web3.js&logoColor=white" alt="web3.js"/><br/>
<img src="https://img.shields.io/badge/javascript-%23323330.svg?style=flat-square&logo=javascript&logoColor=%23F7DF1E" alt="javascript"/>
<img src="https://img.shields.io/badge/-TypeScript-007ACC?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript"/><br/>
<img src="https://img.shields.io/badge/react-%2320232a.svg?style=flat-square&logo=react&logoColor=%2361DAFB" alt="react"/>
<img src="https://img.shields.io/badge/react_native-%2320232a.svg?style=flat-square&logo=react&logoColor=%2361DAFB" alt="react native"/><br/>
<img src="https://img.shields.io/badge/Next-black?style=flat-square&logo=next.js&logoColor=white" alt="Next.js"/>
<img src="https://img.shields.io/badge/remix-%23000.svg?style=flat-square&logo=remix&logoColor=white" alt="remix"/><br/>
<img src="https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=flat-square&logo=tailwind-css&logoColor=white" alt="tailwindcss"/>
<img src="https://img.shields.io/badge/redux-%23593d88.svg?style=flat-square&logo=redux&logoColor=white" alt="redux"/><br/>
<img src="https://img.shields.io/badge/-React%20Query-FF4154?style=flat-square&logo=react%20query&logoColor=white" alt="React Query"/>
<img src="https://img.shields.io/badge/vite-%23646CFF.svg?style=flat-square&logo=vite&logoColor=white" alt="vite"/><br/>
<img src="https://img.shields.io/badge/Swift-F05138?style=flat-square&logo=swift&logoColor=white" alt="Swift"/>
<img src="https://img.shields.io/badge/iOS%20Shortcuts-000000?style=flat-square&logo=apple&logoColor=white" alt="iOS Shortcuts"/>
</p>

</td>
<td valign="top" width="33%">

<h3 align="center">⚙️ ꕷ𖤢ꛕ𖣠ꛘ𖤀ꛎ𖦪ꚲ 𖢧𖤢ꛕꛅꛘ𖣠ꚳ𖣠ꚽꚲ</h3>
<p align="center">
<img src="https://img.shields.io/badge/node.js-6DA55F?style=flat-square&logo=node.js&logoColor=white" alt="NodeJS"/>
<img src="https://img.shields.io/badge/nestjs-%23E0234E.svg?style=flat-square&logo=nestjs&logoColor=white" alt="NestJS"/><br/>
<img src="https://img.shields.io/badge/fastify-%23000000.svg?style=flat-square&logo=fastify&logoColor=white" alt="Fastify"/>
<img src="https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python"/><br/>
<img src="https://img.shields.io/badge/-GraphQL-E10098?style=flat-square&logo=graphql&logoColor=white" alt="GraphQL"/>
<img src="https://img.shields.io/badge/Flutter-%2302569B.svg?style=flat-square&logo=Flutter&logoColor=white" alt="Flutter"/><br/>
<img src="https://img.shields.io/badge/AWS-%23FF9900.svg?style=flat-square&logo=amazon-aws&logoColor=white" alt="AWS"/>
<img src="https://img.shields.io/badge/firebase-%23039BE5.svg?style=flat-square&logo=firebase&logoColor=white" alt="Firebase"/><br/>
<img src="https://img.shields.io/badge/n8n-EA4B71?style=flat-square&logo=n8n&logoColor=white" alt="n8n"/>
<img src="https://img.shields.io/badge/Pulumi-8A3391?style=flat-square&logo=pulumi&logoColor=white" alt="Pulumi"/>
</p>

</td>
<td valign="top" width="33%">

<h3 align="center">🔬 𖢧𖤢𖦪𖢧ꛈꛎ𖦪ꚲ 𖢧𖤢ꛕꛅꛘ𖣠ꚳ𖣠ꚽꚲ</h3>
<p align="center">
<img src="https://img.shields.io/badge/-Docker-46a2f1?style=flat-square&logo=docker&logoColor=white" alt="Docker"/>
<img src="https://img.shields.io/badge/Terraform-844FBA?style=flat-square&logo=terraform&logoColor=white" alt="Terraform"/><br/>
<img src="https://img.shields.io/badge/kubernetes-%23326CE5.svg?style=flat-square&logo=kubernetes&logoColor=white" alt="kubernetes"/>
<img src="https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black" alt="Linux"/><br/>
<img src="https://img.shields.io/badge/Cloudflare-F38020?style=flat-square&logo=Cloudflare&logoColor=white" alt="Cloudflare"/>
<img src="https://img.shields.io/badge/-Github_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white" alt="GitHub Actions"/><br/>
<img src="https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white" alt="Redis"/>
<img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL"/><br/>
<img src="https://img.shields.io/badge/NPM-%23CB3837.svg?style=flat-square&logo=npm&logoColor=white" alt="NPM"/>
<img src="https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=flat-square&logo=visual-studio-code&logoColor=white" alt="VS Code"/>
</p>

</td>
</tr>
</table>

</div>

<br/><br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     TELEMETRY v10.0 // SNAKE CONTRIBUTION MATRIX
     ═══════════════════════════════════════════════════════════════════════════ -->
<a name="stats"></a>
<div align="center">

### 📈 ꚽꛈ𖢧ꛅꚶꔪ ꕷ𖢧ꛎ𖢧ꛈꕷ𖢧ꛈꛕꕷ

<br/>

<img src="https://streak-stats.demolab.com?user=popdeuxrem&theme=highcontrast&hide_border=true&background=0d1117&stroke=00f3ff&ring=00f3ff&fire=bc8cff&currStreakLabel=bc8cff" alt="GitHub Streak" style="border-radius:12px; box-shadow:0 0 24px rgba(188,140,255,0.22);"/>

<br/><br/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="dist/github-snake-dark.svg">
  <img src="dist/github-snake-dark.svg" width="880" alt="GitHub Snake">
</picture>

</div>

<br/><br/>

<img src="assets/divider_pulse.svg" width="1000" alt="Quantum Divider"/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     UPLINK v10.0 // IMMERSIVE CONNECT CONSOLE
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="connect"></a>

<div align="center">

<img src="assets/uplink-console.svg" width="700" alt="Uplink Console"/>

<br/><br/>

<a href="mailto:popdeuxrem@gateway.net">
  <img src="https://img.shields.io/badge/Email-popdeuxrem%40gateway.net-00f3ff?style=for-the-badge&logo=gmail&logoColor=white&labelColor=0d1117" alt="Email"/>
</a>
<a href="https://github.com/popdeuxrem">
  <img src="https://img.shields.io/badge/GitHub-@popdeuxrem-181717?style=for-the-badge&logo=github&logoColor=white&labelColor=0d1117" alt="GitHub"/>
</a>

</div>

<br/><br/>

<img src="assets/divider_circuit.svg" width="1000" alt="Divider"/>

<br/><br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     AXIOM v10.0 // QUANTUM QUOTE SURFACE
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="quote"></a>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/section_quote.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/section_quote.svg">
  <img src="assets/section_quote.svg" width="800" alt="Quantum Axiom">
</picture>

<br/><br/>

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
        description="PopDeuxRem README Auto-Generator v10.0",
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
