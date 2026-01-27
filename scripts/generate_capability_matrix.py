#!/usr/bin/env python3
import os

def generate_matrix():
    skills = [
        {"name": "Rust", "icon": "🦀", "desc": "Systems, Performance", "color": "#00f3ff"},
        {"name": "TypeScript", "icon": "TS", "desc": "Full-stack, Type-safe", "color": "#3178c6"},
        {"name": "Python", "icon": "PY", "desc": "Automation, Data Ops", "color": "#4ade80"},
        {"name": "Go", "icon": "GO", "desc": "Cloud, Concurrency", "color": "#00add8"},
        {"name": "Terraform", "icon": "TF", "desc": "IaC, Provisioning", "color": "#9d00ff"},
        {"name": "Solidity", "icon": "SOL", "desc": "Smart Contracts", "color": "#fbbf24"}
    ]
    
    svg_header = """<svg width="800" height="220" viewBox="0 0 800 220" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="flicker">
      <feMerge>
        <feMergeNode in="SourceGraphic" />
      </feMerge>
      <animate attributeName="opacity" values="1;0.7;1;0.8;1" dur="0.15s" repeatCount="indefinite" />
    </filter>
  </defs>"""
    
    cards = ""
    for i, skill in enumerate(skills):
        row, col = i // 3, i % 3
        x, y = col * 260 + 10, row * 105 + 10
        
        # Apply the flicker filter to a subset of cards for a "random corruption" feel
        filter_str = 'filter="url(#flicker)"' if i % 2 == 0 else ""
        
        cards += f"""
    <g transform="translate({x},{y})" {filter_str}>
      <rect width="250" height="95" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1" />
      <rect x="10" y="10" width="40" height="40" rx="8" fill="{skill['color']}" fill-opacity="0.1" />
      <text x="30" y="36" text-anchor="middle" font-family="monospace" font-size="14" font-weight="bold" fill="{skill['color']}">{skill['icon']}</text>
      <text x="60" y="30" font-family="sans-serif" font-size="16" font-weight="bold" fill="#ffffff">{skill['name']}</text>
      <text x="60" y="50" font-family="sans-serif" font-size="11" fill="#8b949e">{skill['desc']}</text>
      <rect x="60" y="65" width="170" height="4" rx="2" fill="#161b22" />
      <rect x="60" y="65" width="150" height="4" rx="2" fill="{skill['color']}" opacity="0.6">
        <animate attributeName="width" values="150;130;150;145;150" dur="0.2s" repeatCount="indefinite" />
      </rect>
    </g>"""

    svg_footer = '</svg>'
    os.makedirs('assets', exist_ok=True)
    with open('assets/capability-matrix.svg', 'w') as f:
        f.write(svg_header + cards + svg_footer)
    print("◈ Corrupted Capability Matrix deployed.")

if __name__ == "__main__":
    generate_matrix()
