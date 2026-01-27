#!/usr/bin/env python3
import os

def generate_panel_svg():
    # Mock data - in production, these are passed from discovery.py
    stats = [
        {"val": "12", "label": "ACTIVE VESSELS", "color": "#00f3ff"},
        {"val": "3", "label": "OPEN ISSUES", "color": "#4ade80"},
        {"val": "OPTIMAL", "label": "NET_HEALTH", "color": "#fbbf24"},
        {"val": "100%", "label": "UPTIME", "color": "#ffffff"}
    ]
    
    svg = f"""<svg width="800" height="120" viewBox="0 0 800 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="120" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1"/>
  
  <line x1="200" y1="20" x2="200" y2="100" stroke="#30363d" />
  <line x1="400" y1="20" x2="400" y2="100" stroke="#30363d" />
  <line x1="600" y1="20" x2="600" y2="100" stroke="#30363d" />

  <g font-family="monospace" text-anchor="middle">
    <text x="100" y="65" font-size="28" font-weight="bold" fill="{stats[0]['color']}">
      <animate attributeName="opacity" values="0;1" dur="1s" />
      {stats[0]['val']}
    </text>
    <text x="100" y="90" font-size="10" fill="#8b949e" letter-spacing="1">{stats[0]['label']}</text>
    
    <text x="300" y="65" font-size="28" font-weight="bold" fill="{stats[1]['color']}">{stats[1]['val']}</text>
    <text x="300" y="90" font-size="10" fill="#8b949e" letter-spacing="1">{stats[1]['label']}</text>
    
    <text x="500" y="65" font-size="24" font-weight="bold" fill="{stats[2]['color']}">{stats[2]['val']}</text>
    <text x="500" y="90" font-size="10" fill="#8b949e" letter-spacing="1">{stats[2]['label']}</text>
    
    <text x="700" y="65" font-size="28" font-weight="bold" fill="{stats[3]['color']}">{stats[3]['val']}</text>
    <text x="700" y="90" font-size="10" fill="#8b949e" letter-spacing="1">{stats[3]['label']}</text>
  </g>
  
  <rect x="20" y="108" width="760" height="4" rx="2" fill="#161b22"/>
  <rect x="20" y="108" width="700" height="4" rx="2" fill="url(#grad_telemetry)">
    <animate attributeName="width" from="0" to="700" dur="1.5s" fill="freeze" />
  </rect>
  <defs>
    <linearGradient id="grad_telemetry" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00f3ff" />
      <stop offset="100%" stop-color="#9d00ff" />
    </linearGradient>
  </defs>
</svg>"""
    
    os.makedirs('assets', exist_ok=True)
    with open('assets/telemetry-panel.svg', 'w') as f:
        f.write(svg)
    print("◈ Telemetry Dashboard refactored to 4-column spec.")

if __name__ == "__main__":
    generate_panel_svg()
