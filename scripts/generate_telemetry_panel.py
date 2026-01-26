import os
from fetch_telemetry import get_architect_metrics

def generate_panel_svg():
    metrics = get_architect_metrics()
    
    svg = f"""<svg width="800" height="150" viewBox="0 0 800 150" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .base {{ font-family: 'JetBrains Mono', monospace; font-size: 14px; fill: #8b949e; }}
    .label {{ fill: #58a6ff; font-weight: bold; }}
    .value {{ fill: #c9d1d9; }}
    .border {{ stroke: #30363d; }}
    @media (prefers-color-scheme: light) {{
      .value {{ fill: #24292f; }}
      .label {{ fill: #0969da; }}
      .border {{ stroke: #d0d7de; }}
    }}
  </style>
  <rect x="0.5" y="0.5" width="799" height="149" rx="5" class="border" fill="transparent"/>
  
  <text x="20" y="35" class="label">SYSTEM TELEMETRY [v3.0]</text>
  <path d="M20 50H780" stroke="#30363d" />

  <text x="20" y="80" class="base">REPO_VELOCITY:</text>
  <text x="160" y="80" class="value">{metrics['velocity']}</text>
  
  <text x="400" y="80" class="base">SIGNAL_RATIO:</text>
  <text x="540" y="80" class="value">{metrics['signal']}</text>

  <text x="20" y="115" class="base">DEPLOY_CADENCE:</text>
  <text x="160" y="115" class="value">LAST_RUN {metrics['cadence']}</text>
  
  <rect x="540" y="102" width="80" height="18" rx="3" fill="#238636"/>
  <text x="548" y="115" style="fill:white; font-size:11px; font-weight:bold;">NOMINAL</text>
</svg>"""

    with open('assets/telemetry-panel.svg', 'w') as f:
        f.write(svg)

if __name__ == "__main__":
    generate_panel_svg()
