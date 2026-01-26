import json
import os

def generate_panel_svg():
    # Load dynamic metrics
    try:
        with open('dist/telemetry_data.json', 'r') as f:
            metrics = json.load(f)
    except:
        metrics = {"total_issues": 0, "repo_count": 0}

    total_issues = metrics.get("total_issues", 0)
    health_status = "OPTIMAL" if total_issues < 5 else "DEGRADED" if total_issues > 20 else "STABLE"
    health_color = "#238636" if health_status == "OPTIMAL" else "#d29922"

    svg = f"""<svg width="400" height="120" viewBox="0 0 400 120" xmlns="http://www.w3.org/2000/svg">
  <style>
    .header {{ font: bold 12px 'Courier New', monospace; fill: #8b949e; }}
    .stat {{ font: bold 18px 'Courier New', monospace; fill: #58a6ff; }}
    .label {{ font: 10px 'Courier New', monospace; fill: #8b949e; }}
    .health {{ font: bold 14px 'Courier New', monospace; fill: {health_color}; }}
  </style>
  <rect width="100%" height="100%" rx="6" fill="#0d1117" stroke="#30363d"/>
  
  <text x="20" y="30" class="header">◈ SYSTEM_TELEMETRY</text>
  
  <text x="20" y="60" class="label">ACTIVE VESSELS</text>
  <text x="20" y="80" class="stat">{metrics.get("repo_count", 0)}</text>
  
  <text x="160" y="60" class="label">OPEN ISSUES</text>
  <text x="160" y="80" class="stat">{total_issues}</text>
  
  <text x="280" y="60" class="label">NET_HEALTH</text>
  <text x="280" y="80" class="health">{health_status}</text>
  
  <line x1="20" y1="100" x2="380" y2="100" stroke="#30363d" stroke-dasharray="4"/>
</svg>"""
    
    os.makedirs('assets', exist_ok=True)
    with open('assets/telemetry-panel.svg', 'w') as f:
        f.write(svg)

if __name__ == "__main__":
    generate_panel_svg()
