#!/usr/bin/env python3
"""
PopDeuxRem Quantum Surface v12.0 - README Auto-Generator
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
    """Generate hero orbital identity SVG v12.0 - Quantum Orb with orbiting pillars."""
    return """<svg width="1000" height="220" viewBox="0 0 1000 220" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="orb-core" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00f3ff" stop-opacity="0.9"/>
      <stop offset="40%" stop-color="#bc8cff" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#00ff9d" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="orb-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00f3ff" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#00f3ff" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="title-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00f3ff"/>
      <stop offset="50%" stop-color="#bc8cff"/>
      <stop offset="100%" stop-color="#00ff9d"/>
    </linearGradient>
    <linearGradient id="flow-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f3ff" stop-opacity="0"/>
      <stop offset="25%" stop-color="#00f3ff" stop-opacity="1"/>
      <stop offset="75%" stop-color="#bc8cff" stop-opacity="1"/>
      <stop offset="100%" stop-color="#00ff9d" stop-opacity="0"/>
    </linearGradient>
    <filter id="glow-heavy" x="-100%" y="-100%" width="300%" height="300%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow-soft" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="orb-filter" x="-200%" y="-200%" width="500%" height="500%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  
  <style>
    .bg { fill: #0d1117; }
    .grid { stroke: #30363d; stroke-width: 0.3; opacity: 0.2; }
    .matrix { font-family: 'SF Mono', 'JetBrains Mono', monospace; font-size: 8px; fill: #00f3ff; opacity: 0.06; }
    .title-fancy { font-family: 'Playfair Display', 'Bodoni MT', 'Didot', Georgia, serif; font-weight: 900; font-style: italic; font-size: 48px; letter-spacing: 4px; fill: url(#title-grad); filter: url(#glow-heavy); }
    .subtitle { font-family: 'SF Mono', 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 3px; fill: #bc8cff; }
    .pillar { font-family: 'SF Mono', 'JetBrains Mono', monospace; font-size: 9px; letter-spacing: 2px; fill: #8b949e; font-weight: 600; }
    .pillar-value { font-family: 'SF Mono', 'JetBrains Mono', monospace; font-size: 8px; fill: #c9d1d9; }
    .status-label { font-family: 'SF Mono', 'JetBrains Mono', monospace; font-size: 8px; fill: #8b949e; }
    .status-value { font-family: 'SF Mono', 'JetBrains Mono', monospace; font-size: 9px; font-weight: 600; }
    .glyph { font-family: monospace; font-size: 14px; fill: #bc8cff; opacity: 0.4; }
    .boot-text { font-family: 'SF Mono', 'JetBrains Mono', monospace; font-size: 7px; fill: #00ff9d; opacity: 0.5; }
    .orbit-ring { fill: none; stroke-width: 1; opacity: 0.3; }
    .orbit-1 { stroke: #00f3ff; animation: spin-orbit 25s linear infinite; transform-origin: 500px 95px; }
    .orbit-2 { stroke: #bc8cff; animation: spin-orbit 20s linear infinite reverse; transform-origin: 500px 95px; }
    .orbit-3 { stroke: #00ff9d; animation: spin-orbit 30s linear infinite; transform-origin: 500px 95px; }
    .orbit-4 { stroke: #d29922; animation: spin-orbit 35s linear infinite reverse; transform-origin: 500px 95px; }
    @keyframes spin-orbit { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    .pulse { animation: pulse 2s ease-in-out infinite; }
    @keyframes pulse { 0%,100% { opacity: 0.6; } 50% { opacity: 1; } }
    .status-pulse { animation: status-pulse 2s ease-in-out infinite; }
    @keyframes status-pulse { 0%,100% { opacity: 0.7; } 50% { opacity: 1; } }
    .reveal { opacity: 0; animation: reveal 1.5s ease-out forwards; }
    .reveal-1 { animation-delay: 0.2s; }
    .reveal-2 { animation-delay: 0.5s; }
    .reveal-3 { animation-delay: 0.8s; }
    .reveal-4 { animation-delay: 1.1s; }
    .reveal-5 { animation-delay: 1.4s; }
    @keyframes reveal { to { opacity: 1; } }
    .float { animation: float 4s ease-in-out infinite; }
    @keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-6px); } }
    .data-flow { animation: data-flow 3s linear infinite; }
    @keyframes data-flow { 0% { opacity: 0.3; } 50% { opacity: 0.8; } 100% { opacity: 0.3; } }
    @media (prefers-color-scheme: light) {
      .bg { fill: #f6f8fa; }
      .grid { stroke: #d0d7de; }
      .matrix { fill: #0969da; }
      .title-fancy { fill: #0969da; filter: none; }
      .subtitle { fill: #8250df; }
      .pillar { fill: #57606a; }
      .pillar-value { fill: #24292f; }
      .glyph { fill: #8250df; }
    }
    @media (prefers-reduced-motion: reduce) {
      .orbit-ring, .pulse, .status-pulse, .reveal, .float, .data-flow { animation: none; opacity: 1; }
    }
  </style>
  
  <rect class="bg" width="1000" height="220"/>
  
  <g class="grid">
    <line x1="0" y1="20" x2="1000" y2="20"/><line x1="0" y1="40" x2="1000" y2="40"/>
    <line x1="0" y1="60" x2="1000" y2="60"/><line x1="0" y1="80" x2="1000" y2="80"/>
    <line x1="0" y1="100" x2="1000" y2="100"/><line x1="0" y1="120" x2="1000" y2="120"/>
    <line x1="0" y1="140" x2="1000" y2="140"/><line x1="0" y1="160" x2="1000" y2="160"/>
    <line x1="0" y1="180" x2="1000" y2="180"/><line x1="0" y1="200" x2="1000" y2="200"/>
    <line x1="50" y1="0" x2="50" y2="220"/><line x1="100" y1="0" x2="100" y2="220"/>
    <line x1="150" y1="0" x2="150" y2="220"/><line x1="200" y1="0" x2="200" y2="220"/>
    <line x1="250" y1="0" x2="250" y2="220"/><line x1="300" y1="0" x2="300" y2="220"/>
    <line x1="350" y1="0" x2="350" y2="220"/><line x1="400" y1="0" x2="400" y2="220"/>
    <line x1="450" y1="0" x2="450" y2="220"/><line x1="500" y1="0" x2="500" y2="220"/>
    <line x1="550" y1="0" x2="550" y2="220"/><line x1="600" y1="0" x2="600" y2="220"/>
    <line x1="650" y1="0" x2="650" y2="220"/><line x1="700" y1="0" x2="700" y2="220"/>
    <line x1="750" y1="0" x2="750" y2="220"/><line x1="800" y1="0" x2="800" y2="220"/>
    <line x1="850" y1="0" x2="850" y2="220"/><line x1="900" y1="0" x2="900" y2="220"/>
    <line x1="950" y1="0" x2="950" y2="220"/>
  </g>
  
  <g class="matrix">
    <text x="15" y="18">01001101</text><text x="95" y="38">10110100</text><text x="195" y="28">01101001</text>
    <text x="295" y="48">11010010</text><text x="395" y="18">00101101</text><text x="495" y="38">10010110</text>
    <text x="595" y="28">01110011</text><text x="695" y="48">11001010</text><text x="795" y="18">01010010</text>
    <text x="895" y="38">10110101</text><text x="65" y="58">01101001</text><text x="165" y="78">11010010</text>
    <text x="265" y="98">00101101</text><text x="365" y="118">10010110</text><text x="465" y="58">01110011</text>
    <text x="565" y="78">11001010</text><text x="665" y="98">01010010</text><text x="765" y="118">10110101</text>
    <text x="865" y="58">01101001</text><text x="45" y="138">11010010</text><text x="145" y="158">00101101</text>
    <text x="245" y="178">10010110</text><text x="345" y="138">01110011</text><text x="445" y="158">11001010</text>
    <text x="545" y="178">01010010</text><text x="645" y="138">10110101</text><text x="745" y="158">01101001</text>
    <text x="845" y="178">11010010</text><text x="945" y="138">00101101</text>
  </g>
  
  <g transform="translate(500, 95)">
    <ellipse class="orbit-ring orbit-1" cx="0" cy="0" rx="320" ry="65"/>
    <ellipse class="orbit-ring orbit-2" cx="0" cy="0" rx="260" ry="50"/>
    <ellipse class="orbit-ring orbit-3" cx="0" cy="0" rx="200" ry="38"/>
    <ellipse class="orbit-ring orbit-4" cx="0" cy="0" rx="140" ry="25"/>
  </g>
  
  <circle cx="500" cy="95" r="60" fill="url(#orb-glow)" filter="url(#orb-filter)" class="pulse"/>
  <circle cx="500" cy="95" r="35" fill="url(#orb-core)" filter="url(#glow-soft)"/>
  <circle cx="500" cy="95" r="12" fill="#00f3ff" opacity="0.9" class="pulse"/>
  
  <g class="reveal reveal-1">
    <g transform="translate(135, 85)" class="float">
      <rect x="-45" y="-18" width="90" height="36" rx="4" fill="#0d1117" stroke="#00f3ff" stroke-width="1" opacity="0.8"/>
      <text class="pillar" x="0" y="-4" text-anchor="middle" fill="#00f3ff">DETERMINISM</text>
      <text class="pillar-value" x="0" y="10" text-anchor="middle">traceable · reproducible</text>
    </g>
  </g>
  
  <g class="reveal reveal-2">
    <g transform="translate(865, 85)" class="float" style="animation-delay: 0.5s">
      <rect x="-50" y="-18" width="100" height="36" rx="4" fill="#0d1117" stroke="#bc8cff" stroke-width="1" opacity="0.8"/>
      <text class="pillar" x="0" y="-4" text-anchor="middle" fill="#bc8cff">OBSERVABILITY</text>
      <text class="pillar-value" x="0" y="10" text-anchor="middle">systems that speak</text>
    </g>
  </g>
  
  <g class="reveal reveal-3">
    <g transform="translate(135, 145)" class="float" style="animation-delay: 1s">
      <rect x="-50" y="-18" width="100" height="36" rx="4" fill="#0d1117" stroke="#00ff9d" stroke-width="1" opacity="0.8"/>
      <text class="pillar" x="0" y="-4" text-anchor="middle" fill="#00ff9d">iOS AUTOMATION</text>
      <text class="pillar-value" x="0" y="10" text-anchor="middle">Shortcuts · Scriptable</text>
    </g>
  </g>
  
  <g class="reveal reveal-4">
    <g transform="translate(865, 145)" class="float" style="animation-delay: 1.5s">
      <rect x="-45" y="-18" width="90" height="36" rx="4" fill="#0d1117" stroke="#d29922" stroke-width="1" opacity="0.8"/>
      <text class="pillar" x="0" y="-4" text-anchor="middle" fill="#d29922">PROXY MESH</text>
      <text class="pillar-value" x="0" y="10" text-anchor="middle">shadow routing</text>
    </g>
  </g>
  
  <text class="glyph float" x="420" y="65">𖢧ꛅ𖤢</text>
  <text class="glyph float" x="565" y="130" style="animation-delay: 1s">ꚽꚳꛈ𖢧ꛕꛅ</text>
  
  <g class="reveal reveal-3" filter="url(#glow-heavy)">
    <text class="title-fancy" x="500" y="100" text-anchor="middle">𝒫𝑜𝓅𝒟𝑒𝓊𝓍𝑅𝑒𝓂</text>
  </g>
  
  <g class="reveal reveal-4">
    <text class="subtitle" x="500" y="125" text-anchor="middle">PRINCIPAL SYSTEMS ARCHITECT</text>
  </g>
  
  <g class="reveal reveal-5">
    <g transform="translate(180, 195)">
      <circle cx="0" cy="0" r="4" fill="#00f3ff" class="status-pulse"/>
      <text class="status-label" x="10" y="-3">STATUS</text>
      <text class="status-value" x="10" y="8" fill="#00f3ff">ONLINE</text>
    </g>
    <g transform="translate(350, 195)">
      <circle cx="0" cy="0" r="4" fill="#bc8cff" class="status-pulse" style="animation-delay: 0.3s"/>
      <text class="status-label" x="10" y="-3">SYNC</text>
      <text class="status-value" x="10" y="8" fill="#bc8cff">ACTIVE</text>
    </g>
    <g transform="translate(520, 195)">
      <circle cx="0" cy="0" r="4" fill="#00ff9d" class="status-pulse" style="animation-delay: 0.6s"/>
      <text class="status-label" x="10" y="-3">MODE</text>
      <text class="status-value" x="10" y="8" fill="#00ff9d">QUANTUM</text>
    </g>
    <g transform="translate(690, 195)">
      <circle cx="0" cy="0" r="4" fill="#d29922" class="status-pulse" style="animation-delay: 0.9s"/>
      <text class="status-label" x="10" y="-3">UPTIME</text>
      <text class="status-value" x="10" y="8" fill="#d29922">∞</text>
    </g>
    <g transform="translate(850, 195)">
      <circle cx="0" cy="0" r="4" fill="#8b949e" class="status-pulse" style="animation-delay: 1.2s"/>
      <text class="status-label" x="10" y="-3">CHANNEL</text>
      <text class="status-value" x="10" y="8" fill="#8b949e">OPEN</text>
    </g>
  </g>
  
  <line x1="0" y1="218" x2="1000" y2="218" stroke="#30363d" stroke-width="2"/>
  <rect x="0" y="217" width="300" height="3" fill="url(#flow-grad)" class="data-flow">
    <animate attributeName="x" values="0;700;0" dur="4s" repeatCount="indefinite"/>
  </rect>
  
  <g class="boot-text" opacity="0">
    <text x="30" y="10">◈ BOOT: iOS Shortcuts + Scriptable operators loaded</text>
    <text x="600" y="10">◈ PROXY: Shadow mesh routing active</text>
    <animate attributeName="opacity" values="0;0.5;0" dur="3s" repeatCount="indefinite"/>
  </g>
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
    """Generate uplink console SVG v12.0 - Polished connect card."""
    return """<svg width="800" height="240" viewBox="0 0 800 240" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="uplink-bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#161b22"/>
      <stop offset="100%" stop-color="#0d1117"/>
    </linearGradient>
    <linearGradient id="uplink-border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00f3ff" stop-opacity="0.6"/>
      <stop offset="50%" stop-color="#bc8cff" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#00ff9d" stop-opacity="0.6"/>
    </linearGradient>
    <filter id="uplink-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  
  <style>
    .card-bg { fill: url(#uplink-bg-grad); }
    .card-border { fill: none; stroke: url(#uplink-border-grad); stroke-width: 2; }
    .card-inner-border { fill: none; stroke: #30363d; stroke-width: 0.5; stroke-dasharray: 4 2; }
    .header-text { font-family: 'SF Mono', 'JetBrains Mono', monospace; font-size: 12px; fill: #00f3ff; letter-spacing: 3px; font-weight: 600; }
    .channel-label { font-family: 'SF Mono', 'JetBrains Mono', monospace; font-size: 9px; fill: #8b949e; letter-spacing: 1px; }
    .channel-value { font-family: 'SF Mono', 'JetBrains Mono', monospace; font-size: 13px; fill: #c9d1d9; font-weight: 500; }
    .channel-handle { font-family: 'SF Mono', 'JetBrains Mono', monospace; font-size: 11px; fill: #58a6ff; }
    .footer-text { font-family: 'SF Mono', 'JetBrains Mono', monospace; font-size: 8px; fill: #484f58; letter-spacing: 2px; }
    .glyph { font-family: monospace; font-size: 10px; fill: #bc8cff; opacity: 0.5; }
    .signal-dot { animation: signal-pulse 2s ease-in-out infinite; }
    @keyframes signal-pulse { 0%,100% { opacity: 0.5; r: 3; } 50% { opacity: 1; r: 4; } }
    .corner-bracket { fill: none; stroke: #00f3ff; stroke-width: 1.5; stroke-opacity: 0.4; }
    .data-line { stroke: #00f3ff; stroke-width: 0.5; stroke-dasharray: 2 4; opacity: 0.3; animation: data-flow 3s linear infinite; }
    @keyframes data-flow { to { stroke-dashoffset: -24; } }
    @media (prefers-color-scheme: light) {
      .card-bg { fill: #f6f8fa; }
      .card-border { stroke: url(#uplink-border-grad); }
      .card-inner-border { stroke: #d0d7de; }
      .header-text { fill: #0969da; }
      .channel-label { fill: #57606a; }
      .channel-value { fill: #24292f; }
      .channel-handle { fill: #0969da; }
      .corner-bracket { stroke: #0969da; }
    }
    @media (prefers-reduced-motion: reduce) {
      .signal-dot, .data-line { animation: none; opacity: 0.7; }
    }
  </style>
  
  <rect class="card-bg" x="0" y="0" width="800" height="240" rx="12"/>
  <rect class="card-border" x="1" y="1" width="798" height="238" rx="12"/>
  <rect class="card-inner-border" x="8" y="8" width="784" height="224" rx="8"/>
  
  <path class="corner-bracket" d="M20,40 L20,20 L40,20"/>
  <path class="corner-bracket" d="M760,20 L780,20 L780,40"/>
  <path class="corner-bracket" d="M780,200 L780,220 L760,220"/>
  <path class="corner-bracket" d="M40,220 L20,220 L20,200"/>
  
  <g filter="url(#uplink-glow)">
    <text class="header-text" x="400" y="45" text-anchor="middle">◈ UPLINK CONSOLE ◈</text>
  </g>
  
  <line class="data-line" x1="50" y1="60" x2="750" y2="60"/>
  
  <g transform="translate(100, 90)">
    <circle class="signal-dot" cx="0" cy="0" r="3" fill="#00f3ff"/>
    <text class="channel-label" x="15" y="-8">GITHUB</text>
    <text class="channel-value" x="15" y="8">@popdeuxrem</text>
    <text class="glyph" x="15" y="22">◈ primary</text>
  </g>
  
  <g transform="translate(300, 90)">
    <circle class="signal-dot" cx="0" cy="0" r="3" fill="#8b949e" style="animation-delay: 0.3s"/>
    <text class="channel-label" x="15" y="-8">X / TWITTER</text>
    <text class="channel-value" x="15" y="8">@d3_glitch</text>
    <text class="glyph" x="15" y="22">◈ alias</text>
  </g>
  
  <g transform="translate(500, 90)">
    <circle class="signal-dot" cx="0" cy="0" r="3" fill="#bc8cff" style="animation-delay: 0.6s"/>
    <text class="channel-label" x="15" y="-8">MATRIX</text>
    <text class="channel-value" x="15" y="8">@popdeuxrem:matrix.org</text>
    <text class="glyph" x="15" y="22">◈ encrypted</text>
  </g>
  
  <g transform="translate(700, 90)">
    <circle class="signal-dot" cx="0" cy="0" r="3" fill="#00ff9d" style="animation-delay: 0.9s"/>
    <text class="channel-label" x="15" y="-8">EMAIL</text>
    <text class="channel-value" x="15" y="8">@gateway.net</text>
    <text class="glyph" x="15" y="22">◈ async</text>
  </g>
  
  <line x1="50" y1="140" x2="750" y2="140" stroke="#30363d" stroke-width="0.5"/>
  
  <g transform="translate(400, 165)">
    <text class="footer-text" x="0" y="0" text-anchor="middle">PROTOCOL: context · constraints · ideal outcome</text>
  </g>
  
  <g transform="translate(400, 185)">
    <text class="footer-text" x="0" y="0" text-anchor="middle" fill="#00f3ff" opacity="0.7">ꛕ𖣠ꛘꛘ𖤢ꛕ𖢧 ꛃꛈ𖢧ꛅ 𖢑𖤢 ∙ 🛰 CHANNEL ACTIVE</text>
  </g>
  
  <g transform="translate(400, 215)">
    <text class="footer-text" x="0" y="0" text-anchor="middle">Send transmission → await entanglement</text>
  </g>
  
  <g opacity="0.15">
    <text x="30" y="230" font-family="monospace" font-size="8" fill="#00f3ff">𖢧ꛅ𖤢</text>
    <text x="750" y="230" font-family="monospace" font-size="8" fill="#bc8cff">ꚽꚳꛈ𖢧ꛕꛅ</text>
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
    """Generate quantum axiom quote SVG v12.0."""
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
    .quote-author {{ font-family: 'SF Mono', 'JetBrains Mono', monospace; font-size: 11px; fill: #8b949e; letter-spacing: 2px; }}
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
  
  <text class="quote-glyph" x="400" y="125" text-anchor="middle">ꚽꛈ𖢧ꛅꚶꔪ ꕷ𖢧ꛎ𖢧ꛈꕷ𖢧ꛈꛕꕷ ∙ ◈ ∙ AXIOM</text>
  
  <text class="quote-mark" x="750" y="100">"</text>
</svg>'''


def build_readme(dry_run: bool = False, verbose: bool = False) -> str:
    """Main build function - generates README.md from data sources."""

    print("=" * 60)
    print("◈ POPDEUXREM QUANTUM SURFACE v12.0 - README BUILDER")
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
  ║  POPDEUXREM // QUANTUM SURFACE v12.0                                      ║
  ║  AUTO-GENERATED BY build_readme.py                                        ║
  ║  LAST SYNC: {timestamp} | SHA: {build_hash[:16]}               ║
  ╚═══════════════════════════════════════════════════════════════════════════╝
 -->

<div align="center">

<!-- ═══════════════════════════════════════════════════════════════════════════
     HERO SURFACE v12.0 // IMMERSIVE ORBITAL IDENTITY
     ═══════════════════════════════════════════════════════════════════════════ -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero_banner.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/hero_banner.svg">
  <img src="assets/hero_banner.svg" width="1000" alt="PopDeuxRem Banner"/>
</picture>

<br/><br/>

<img src="assets/hero_particle_banner.svg" width="1200" alt="Chris Particle Banner"/>

<br/><br/>

<a name="header"></a>

<img src="assets/hero_orbital.svg" width="1000" alt="PopDeuxRem Orbital Identity"/>

<br/><br/>

<img src="https://readme-typing-svg.herokuapp.com?font=Playfair+Display&weight=700&size=28&duration=4000&pause=1500&color=BC8CFF66&center=true&vCenter=true&repeat=true&width=700&lines=Full+Stack+Engineer;Engineered+Clarity;Tech+Innovator;Open+Source+Enthusiast;Auditable+Systems;Composable+By+Design;Problem+Solver;Quantum+Architect" alt="Typing"/>

<br/><br/>

<img src="https://komarev.com/ghpvc/?username=popdeuxrem&label=VIEWS&color=00f3ff&style=flat-square&labelColor=0d1117" alt="Views"/>

<br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     NAVIGATION
     ═══════════════════════════════════════════════════════════════════════════ -->

<code>
<a href="#about">ABOUT</a> · <a href="#terminal">TERMINAL</a> · <a href="#stack">STACK</a> · <a href="#stats">STATS</a> · <a href="#connect">CONNECT</a>
</code>

<br/>

<img src="assets/divider_quantum.svg" width="1000" alt="Divider"/>

<br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     OPERATOR CORE v12.0 // LIVING JAVASCRIPT OBJECT
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="about"></a>

<div align="center">

<img src="assets/flow-line.svg" width="1000" alt="Flow"/>

</div>

<br/>

### ◈ ꛎꔪ𖣠ꚶ𖢧 𖢑𖤢 ◈

```javascript
/**
 * ╔═══════════════════════════════════════════════════════════════════════════╗
 * ║  POPDEUXREM :: QUANTUM OPERATOR DEFINITION v12.0                          ║
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
    twitter: "@d3_glitch",
    matrix: "@popdeuxrem:matrix.org",
    email: "popdeuxrem@gateway.net",
    protocol: "Send: context · constraints · ideal outcome"
  }},
  
  directive: "ꛤ𖦪ꛈ𖢑ꛎ𖦪ꚲ 𖢧𖤢ꛕꛅꛘ𖣠ꚳ𖣠ꚽꚲ ∙ ꕷ𖤢ꛕ𖣠ꛘ𖤀ꛎ𖦪ꚲ 𖢧𖤢ꛕꛅꛘ𖣠ꚳ𖣠ꚽꚲ ∙ 𖢧𖤢𖦪𖢧ꛈꛎ𖦪ꚲ 𖢧𖤢ꛕꛅꛘ𖣠ꚳ𖣠ꚽꚲ"
  
}};

export default popdeuxrem; // ◈ Composable. Reversible. Quantum.
```

<br/>

<img src="assets/divider_circuit.svg" width="1000" alt="Divider"/>

<br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     TERMINAL v12.0 // DYNAMIC SVG WITH LIVE PARTICLES
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="terminal"></a>

### ◈ 𖢧𖤢𖦪𖢑ꛈꛘꛎꚳ ◈

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/terminal-dynamic.svg">
  <img src="assets/terminal-dynamic.svg" width="880" alt="PopDeuxRem Dynamic Terminal">
</picture>

<br/>

<img src="assets/divider_stream.svg" width="1000" alt="Divider"/>

<br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     PROXY MESH :: FEATURED ARTIFACT
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="proxy"></a>

### ◈ ꛤ𖦪ꛣ𖤗ꚲ 𖢑𖤢ꕷꛅ ◈

<div align="center">

<a href="https://github.com/popdeuxrem/shadow-scripts">
  <img src="https://img.shields.io/badge/SHADOW--SCRIPTS-SECOPS_SHIP-00f3ff?style=for-the-badge&logo=github&logoColor=00f3ff&labelColor=0d1117&color=0d1117" alt="shadow-scripts"/>
</a>
<img src="https://img.shields.io/github/stars/popdeuxrem/shadow-scripts?style=for-the-badge&color=d29922&labelColor=0d1117" alt="stars"/>
<img src="https://img.shields.io/badge/STATUS-SHIP-d29922?style=for-the-badge&labelColor=0d1117" alt="status"/>

</div>

<br/>

> **Proxy meshes, DNS overlays, stealth routing, iOS Shortcuts operators, n8n/Docker pipelines.**

<a name="shadow"></a>

<details>
<summary><b>◈ ꕷꛅꛎ𖤀𖣠ꛃ_ꛕ𖣠𖦪𖤢 ◈</b></summary>

<br/>

```typescript
/**
 * ╔═══════════════════════════════════════════════════════════════════════════╗
 * ║  POPDEUXREM :: OPERATIONAL MANIFEST v12.0                                 ║
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

<br/>

<img src="assets/divider_mesh.svg" width="1000" alt="Divider"/>

<br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     TECH MATRIX v12.0 // NEON CARD GRID
     ═══════════════════════════════════════════════════════════════════════════ -->
<a name="stack"></a>
<div align="center">

### ◈ 𖢧𖤢ꛕꛅ ꕷ𖢧ꛎꛕ𖢉 ◈

<br/>

<table>
<tr>
<td valign="top" width="33%">

<h3 align="center">🧰 ꘘ𖦪𖣠ꛘ𖢧𖤢ꛘ𖤀</h3>
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

<h3 align="center">⚙️ ꔪꛎꛕ𖢉𖤢ꛘ𖤀</h3>
<p align="center">
<img src="https://img.shields.io/badge/node.js-6DA55G?style=flat-square&logo=node.js&logoColor=white" alt="NodeJS"/>
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

<h3 align="center">🔬 ꛈꛘꘘ𖦪ꛎ</h3>
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

<br/>

<img src="assets/divider_pulse.svg" width="1000" alt="Quantum Divider"/>

<br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     TELEMETRY v12.0 // SNAKE CONTRIBUTION MATRIX
     ═══════════════════════════════════════════════════════════════════════════ -->
<a name="stats"></a>
<div align="center">

### ◈ 𖢧𖤢ꚳ𖤢𖢑𖤢𖢧𖦪ꚲ ◈

<br/>

<img src="https://streak-stats.demolab.com?user=popdeuxrem&theme=highcontrast&hide_border=true&background=0d1117&stroke=00f3ff&ring=00f3ff&fire=bc8cff&currStreakLabel=bc8cff" alt="GitHub Streak" style="border-radius:12px; box-shadow:0 0 24px rgba(188,140,255,0.22);"/>

<br/><br/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="dist/github-snake-dark.svg">
  <img src="dist/github-snake-dark.svg" width="880" alt="GitHub Snake">
</picture>

</div>

<br/>

<img src="assets/divider_quantum.svg" width="1000" alt="Divider"/>

<br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     UPLINK v12.0 // IMMERSIVE CONNECT CONSOLE
     ═══════════════════════════════════════════════════════════════════════════ -->

<a name="connect"></a>

### 🤝 ꛕ𖣠ꛘꛘ𖤢ꛕ𖢧 ꛃꛈ𖢧ꛅ 𖢑𖤢

<div align="center">

```
⟁ ORBIT // UPLINK

╭────────────────────────────────────────────────────────────╮
│ 🛰 GitHub → https://github.com/Popdeuxrem                  │
│ ✉ DM (X) → https://x.com/d3_glitch                        │
│                                                            │
│ 📓 Quantum Lab → https://github.com/Popdeuxrem/quantum-lab │
│ 📧 Email → mailto:contact@popdeuxrem@email                 │
╰────────────────────────────────────────────────────────────╯

Transmission Schema
context · constraints · ideal_outcome
```

</div>

<br/>

<img src="assets/divider_circuit.svg" width="1000" alt="Divider"/>

<br/>

<!-- ═══════════════════════════════════════════════════════════════════════════
     AXIOM v12.0 // QUANTUM QUOTE SURFACE
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
        description="PopDeuxRem README Auto-Generator v12.0",
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
